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

        // Log Valid Transactions to Firestore
        if (payload.event === "charge.completed" && payload.data.status === "successful") {
            const data = payload.data;
            const transactionRef = data.tx_ref;
            const fullName = data.customer.name || "Unknown";
            const email = data.customer.email;

            await db.collection("certificate_payments").doc(String(transactionRef)).set({
                fullName: fullName,
                email: email,
                paymentReference: String(transactionRef),
                amount: data.amount,
                currency: data.currency,
                status: "paid",
                paidAt: admin.firestore.FieldValue.serverTimestamp()
            }, { merge: true });

            console.log(`Successfully logged cert payment for: ${email}`);
        }

        return res.status(200).send("Webhook received");
    } catch (error) {
        console.error("Webhook Execution Error:", error);
        return res.status(500).json({ error: error.message || "Internal Server Error" });
    }
}
