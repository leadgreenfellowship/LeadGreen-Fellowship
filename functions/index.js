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
            const fullName = data.customer.name || "Unknown";
            const email = data.customer.email;
            const amount = data.amount;
            const currency = data.currency;

            // Save to Firestore accurately from the backend
            await db.collection("certificate_payments").doc(String(transactionRef)).set({
                fullName: fullName,
                email: email,
                paymentReference: String(transactionRef),
                amount: amount,
                currency: currency,
                status: "paid",
                paidAt: admin.firestore.FieldValue.serverTimestamp()
            }, { merge: true });

            console.log(`Payment successfully logged for ${email} with ref ${transactionRef}`);
        }

        return res.status(200).send("Webhook received");
    } catch (error) {
        console.error("Webhook Error:", error);
        return res.status(500).send("Internal Server Error");
    }
});

exports.flutterwave = functions.https.onRequest(app);
