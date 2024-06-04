import os
import re
import random
import smtplib
import msal
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# In-memory storage for OTPs
otp_store = {}

EMAIL_ADDRESS = "visaliveru@pagoanalytics.com"  # Replace with your email address
EMAIL_PASSWORD = "Vinaysai@123"             # Replace with your email password
SMTP_SERVER = "smtp.office365.com"                      # SMTP server for Office 365
SMTP_PORT = 587     

# OAuth 2.0 credentials
CLIENT_ID = "aea4387e-aa87-4dd8-a39d-f8f910e0eaeb"
CLIENT_SECRET = "a2250dfb-4305-44a8-ab13-7ff96494c6ba"
TENANT_ID = "aa5996e2-2eac-4d32-bc0e-8615db92fef5"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://outlook.office365.com/.default"]

# HTML template string
otp_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        .container {
            width: 80%;
            margin: auto;
            padding: 20px;
            border: 1px solid #ccc;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            font-family: Arial, sans-serif;
        }
        .header {
            background-color: #4CAF50;
            color: white;
            padding: 10px;
            text-align: center.
        }
        .body {
            margin-top: 20px;
            text-align: left;
        }
        .footer {
            margin-top: 20px;
            text-align: center.
            font-size: 12px.
            color: #888.
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>OTP Verification</h1>
        </div>
        <div class="body">
            <p>Your One-Time Password (OTP) is <strong>{{ otp }}</strong>.</p>
            <p>Please use this OTP to complete your verification process. This OTP is valid for a short period.</p>
        </div>
        <div class="footer">
            <p>If you did not request this OTP, please ignore this email.</p>
        </div>
    </div>
</body>
</html>
"""

def email_verification(email):
    email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return re.match(email_regex, email) is not None

def get_access_token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET
    )
    result = app.acquire_token_for_client(scopes=SCOPES)
    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception("Could not obtain access token")

def send_otp(email, otp):
    try:
        access_token = get_access_token()
        auth_string = f"user={EMAIL_ADDRESS}\1auth=Bearer {access_token}\1\1"
        auth_string = auth_string.encode("ascii")
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.docmd("AUTH", "XOAUTH2 " + auth_string.decode("ascii"))

        body = render_template_string(otp_template, otp=otp)
        subject = "OTP Verification using Python"
        message = f"Subject: {subject}\nContent-Type: text/html\n\n{body}"
        
        server.sendmail(EMAIL_ADDRESS, email, message)
        server.quit()
    except Exception as e:
        app.logger.error(f"Failed to send email: {e}")
        raise

@app.route('/send-otp', methods=['POST'])
def send_otp_route():
    data = request.json
    email = data.get('email')
    
    if not email_verification(email):
        return jsonify({"error": "Invalid email address"}), 400
    
    otp = random.randint(100000, 999999)
    otp_store[email] = otp
    send_otp(email, otp)
    
    return jsonify({"message": f"OTP has been sent to {email}. Please check your email."})

@app.route('/verify-otp', methods=['POST'])
def verify_otp_route():
    data = request.json
    email = data.get('email')
    otp_provided = data.get('otp')
    
    if email not in otp_store:
        return jsonify({"error": "Email not found"}), 400
    
    if otp_store[email] == int(otp_provided):
        del otp_store[email]  # OTP is used, remove it
        return jsonify({"message": "OTP verified successfully"})
    else:
        return jsonify({"error": "Invalid OTP"}), 400

if __name__ == '__main__':
    app.run(debug=True)
