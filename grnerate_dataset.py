import random
import pandas as pd

categories = {
    "OTP Fraud": [
        "I shared OTP and money got deducted",
        "Scammer asked for OTP and withdrew money",
        "Received fake OTP verification call",
        "Someone requested OTP for refund",
        "Bank caller asked for OTP"
    ],
    "UPI Fraud": [
        "Clicked UPI link and lost money",
        "Approved UPI collect request accidentally",
        "QR code scan resulted in money loss",
        "Unknown UPI transaction occurred",
        "Fraud UPI payment request received"
    ],
    "Phishing": [
        "Fake email asking bank login details",
        "Received suspicious SMS with login link",
        "KYC update message with unknown link",
        "Bank account verification email scam",
        "Fraud website stole my credentials"
    ],
    "Account Hacking": [
        "Instagram account hacked",
        "Gmail password changed without permission",
        "Facebook account accessed by unknown person",
        "Unauthorized login alert received",
        "Lost access to my social media account"
    ],
    "Job Scam": [
        "Paid money for fake job offer",
        "Work from home scam collected fee",
        "Fake overseas job asking visa fee",
        "Fraud job consultancy took money",
        "Telegram job scam demanding payment"
    ],
    "Lottery Scam": [
        "Won lottery message asking processing fee",
        "Prize claim scam asking payment",
        "Lucky draw message demanding money",
        "International lottery email scam",
        "WhatsApp lottery winning fraud"
    ],
    "Investment Scam": [
        "Crypto investment group cheated me",
        "Ponzi scheme promised double returns",
        "Fake stock market advisor fraud",
        "Online trading app blocked withdrawal",
        "Fraud investment call promising high returns"
    ],
    "Online Shopping Scam": [
        "Fake shopping website took payment",
        "Ordered product not delivered",
        "Instagram store blocked after payment",
        "Ecommerce fraud site disappeared",
        "Online seller not responding after payment"
    ],
    "Loan App Fraud": [
        "Fake loan approval asking processing fee",
        "Loan app threatening with morphed photos",
        "Instant loan app demanding extra charges",
        "Fraud loan agent collected documents",
        "Personal loan scam through mobile app"
    ],
    "Sim Swap Fraud": [
        "SIM swapped and money transferred",
        "Duplicate SIM issued without consent",
        "Bank OTP received on new SIM",
        "Mobile network stopped and account emptied",
        "SIM cloning caused financial loss"
    ]
}

data = []

for label, sentences in categories.items():
    for _ in range(30):   # 30 variations each category (10x30 = 300 samples)
        sentence = random.choice(sentences)
        variation = sentence + " " + random.choice(["urgently", "immediately", "today", "yesterday", "suddenly"])
        data.append([variation, label])

df = pd.DataFrame(data, columns=["text", "label"])
df.to_csv("dataset.csv", index=False)

print("✅ 300 sample dataset generated successfully!")
