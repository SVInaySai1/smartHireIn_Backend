import random
import smtplib
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# In-memory storage for OTPs
otp_store = {}

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
            text-align: center;
        }
        .body {
            margin-top: 20px;
            text-align: left;
        }
        .footer {
            margin-top: 20px;
            text-align: center;
            font-size: 12px;
            color: #888;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>OTP Verification</h1>
        </div>
        <div class="body">
            <p>Dear {{name}},</p>
            <p>Your One-Time Password (OTP) is <strong>{{otp}}</strong>.</p>
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
    email_domains = ["gmail", "hotmail", "yahoo", "outlook"]
    email_endings = [".com", ".in", ".org", ".edu", ".co.in"]
    
    if "@" not in email:
        return False
    
    domain_part = email.split("@")[1]
    domain_check = any(domain in domain_part for domain in email_domains)
    ending_check = any(domain_part.endswith(ending) for ending in email_endings)

    return domain_check and ending_check

def send_otp(email, name, otp):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    password = "stqqwjqoocucknsx"  # Replace with your actual app password
    server.login("priyanshu25122002@gmail.com", password)
    
    body = render_template_string(otp_template, name=name, otp=otp)
    subject = "OTP Verification using Python"
    message = f"Subject: {subject}\nContent-Type: text/html\n\n{body}"
    
    server.sendmail("priyanshu25122002@gmail.com", email, message)
    server.quit()

def send_otp_route():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    
    if not email_verification(email):
        return jsonify({"error": "Invalid email address"}), 400
    
    otp = random.randint(100000, 999999)
    otp_store[email] = otp
    send_otp(email, name, otp)
    
    return jsonify({"message": f"OTP has been sent to {email}. Please check your email."})

def verify_otp_route():
    data = request.json
    email = data.get('email')
    otp_provided = data.get('otp')
    
    if email not in otp_store:
        return jsonify({"error": "Email not found"}), 400
    
    if otp_store[email] == otp_provided:
        del otp_store[email]  # OTP is used, remove it
        return jsonify({"message": "OTP verified successfully"})
    else:
        return jsonify({"error": "Invalid OTP"}), 400

if __name__ == '__main__':
    app.run(debug=True)
