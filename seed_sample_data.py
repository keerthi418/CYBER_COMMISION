import sqlite3, datetime, random

cats = ['OTP Fraud','UPI Fraud','Lottery Scam','Phishing','Job Scam','Account Hacking']
texts = {
    'OTP Fraud':'Received OTP asking to confirm transaction',
    'UPI Fraud':'Unauthorized UPI payment',
    'Lottery Scam':'Won prize, asked to pay fee',
    'Phishing':'Email asking password reset',
    'Job Scam':'Paid registration for fake job',
    'Account Hacking':'Unable to login to account'
}

conn = sqlite3.connect('complaints.db')
c = conn.cursor()
now = datetime.datetime.now()
for i in range(12):
    cat = random.choice(cats)
    ts = (now - datetime.timedelta(days=random.randint(0,6))).strftime('%Y-%m-%d %H:%M:%S')
    text = texts[cat]
    confidence = round(random.uniform(70,99),1)
    advice = ''
    c.execute("INSERT INTO complaints (text,prediction,confidence,advice,timestamp,ip) VALUES (?,?,?,?,?,?)",
              (text, cat, confidence, advice, ts, '127.0.0.1'))

conn.commit()
conn.close()
print('Inserted sample complaints.')
