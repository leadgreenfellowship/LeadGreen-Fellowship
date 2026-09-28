const functions = require("firebase-functions");
const admin = require("firebase-admin");
const express = require("express");
const cors = require("cors");

admin.initializeApp();
const db = admin.firestore();
const app = express();
app.use(cors({ origin: true }));

// Flutterwave sends webhooks to this endpoint
app.post("/webhook", async (req, res) => {
    try {
        // You should configure a secret hash in your Flutterwave dashboard and set it here
        const secretHash = "YOUR_FLUTTERWAVE_SECRET_HASH"; // Change this before testing
        const signature = req.headers["verif-hash"];

        if (!signature || signature !== secretHash) {
            console.error("Unauthorized request, invalid signature");
            return res.status(401).send("Unauthorized");
        }

        const payload = req.body;
        console.log("Webhook payload received");

        // Ensure it's a successful transaction
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
                    "Authorization": `Bearer ${process.env.FLUTTERWAVE_SECRET_KEY || "YOUR_FLUTTERWAVE_SECRET_KEY"}`
                }
            });

            const fwData = await fwResponse.json();

            if (fwData.status === "success" && fwData.data.status === "successful" && fwData.data.amount >= data.amount && fwData.data.currency === data.currency) {
                // Save to Firestore accurately from the backend
                await docRef.set({
                    fullName: fwData.data.customer.name || data.customer.name || "Unknown",
                    email: fwData.data.customer.email || data.customer.email,
                    paymentReference: String(transactionRef),
                    amount: fwData.data.amount,
                    currency: fwData.data.currency,
                    status: "paid",
                    paidAt: admin.firestore.FieldValue.serverTimestamp()
                }, { merge: true });

                console.log(`Successfully verified and logged payment for ${fwData.data.customer.email} with ref ${transactionRef}`);
            } else {
                console.error("Flutterwave API verification failed or mismatched data.", fwData);
                return res.status(400).send("Verification failed");
            }
        }

        return res.status(200).send("Webhook received");
    } catch (error) {
        console.error("Webhook Error:", error);
        return res.status(500).send("Internal Server Error");
    }
});

exports.flutterwave = functions.https.onRequest(app);
