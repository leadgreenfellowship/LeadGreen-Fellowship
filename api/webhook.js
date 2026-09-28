const admin = require("firebase-admin");

module.exports = async function handler(req, res) {
    // Setup CORS
    res.setHeader('Access-Control-Allow-Credentials', true);
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');

    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    if (req.method !== 'POST') {
        return res.status(405).json({ message: "Method Not Allowed" });
    }

    try {
        // Initialize Firebase Admin globally to avoid re-initializing on hot starts
        if (!admin.apps.length) {
            admin.initializeApp({
                credential: admin.credential.cert({
                    projectId: process.env.FIREBASE_PROJECT_ID,
                    clientEmail: process.env.FIREBASE_CLIENT_EMAIL,
                    privateKey: process.env.FIREBASE_PRIVATE_KEY ? process.env.FIREBASE_PRIVATE_KEY.replace(/\\n/g, '\n') : '',
                })
            });
        }

        const db = admin.firestore();
        const secretHash = process.env.FLUTTERWAVE_SECRET_HASH;
        const signature = req.headers["verif-hash"];

        // Validate Security Signature
        if (!signature || signature !== secretHash) {
            console.error("Unauthorized request, invalid signature");
            return res.status(401).send("Unauthorized");
        }

        const payload = req.body;
        console.log("Verified Webhook Payload received");

        if (payload.event === "charge.completed" && payload.data.status === "successful") {
            const data = payload.data;
            const transactionRef = data.tx_ref;
            const transactionId = data.id;

            const docRef = db.collection("certificate_payments").doc(String(transactionRef));
            const docSnap = await docRef.get();

            // Idempotency check
            if (docSnap.exists && (docSnap.data().status === "paid" || docSnap.data().status === "successful")) {
                console.log(`Transaction ${transactionRef} is already paid. Skipping to prevent duplicates.`);
                return res.status(200).send("Already processed");
            }

            // Verify with Flutterwave API to prevent spoofing
            const fwResponse = await fetch(`https://api.flutterwave.com/v3/transactions/${transactionId}/verify`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${process.env.FLUTTERWAVE_SECRET_KEY}`
                }
            });

            const fwData = await fwResponse.json();

            if (fwData.status === "success" && fwData.data.status === "successful" && fwData.data.amount >= data.amount && fwData.data.currency === data.currency) {
                await docRef.set({
                    fullName: fwData.data.customer.name || data.customer.name || "Unknown",
                    email: fwData.data.customer.email || data.customer.email,
                    paymentReference: String(transactionRef),
                    amount: fwData.data.amount,
                    currency: fwData.data.currency,
                    status: "paid",
                    paidAt: admin.firestore.FieldValue.serverTimestamp()
                }, { merge: true });
                console.log(`Successfully verified and logged payment for: ${fwData.data.customer.email}`);
            } else {
                console.error("Flutterwave API verification failed or mismatched data.", fwData);
                return res.status(400).send("Verification failed");
            }
        }

        return res.status(200).send("Webhook received");
    } catch (error) {
        console.error("Webhook Execution Error:", error);
        return res.status(500).json({ error: error.message || "Internal Server Error" });
    }
}
