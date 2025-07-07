import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ---------- CONFIGURATION ----------
from_email = "adityatest408@gmail.com"         # ✅ Correct Gmail
password = "bnrhupshkpqcavkq"                   # ✅ App Password for this Gmail
smtp_server = "smtp.gmail.com"
smtp_port = 465
subject = "Regarding Your Job Application"

# Map resume filenames to email IDs
email_map = {
    "Adigencv.pdf": "adarshkumar709121@gmail.com",
    "RAVNEET SINGH GOOGLE RESUME.pdf": "adityardx001@gmail.com"   # ✅ fixed from gamil.com
}

# ---------- EMAIL FUNCTION ----------
def send_email(to_email, subject, message_body):
    try:
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message_body, 'plain'))

        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(from_email, password)
            server.send_message(msg)
            print(f"✅ Email sent to: {to_email}")
    except Exception as e:
        print(f"❌ Failed to send to {to_email}: {e}")

# ---------- MAIN ----------
try:
    df = pd.read_csv("result.csv")
    top_candidates = df.head(3)

    for index, row in top_candidates.iterrows():
        filename = row['filename']
        score = row['score']
        to_email = email_map.get(filename)

        if to_email:
            message = f"""Hi,

Your resume matched well with our job description. We're impressed with your profile and will reach out to you soon.

Match Score: {score}

Best regards,  
Aditya - Resume Sorter Bot"""
            send_email(to_email, subject, message)
        else:
            print(f"⚠️ No email found for: {filename}")

except FileNotFoundError:
    print("❌ 'result.csv' not found. Please run sorter.py first.")
