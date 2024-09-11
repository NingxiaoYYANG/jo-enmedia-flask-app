import os
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from flask_mail import Mail, Message

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "http://localhost:3001"}})

# Set up the Flask-Mail
app.config.from_mapping(
    SECRET_KEY = os.urandom(24),
    MAIL_SERVER ='smtp.elasticemail.com',  # Update the SMTP server
    MAIL_PORT = 2525,  # Use the correct SMTP port (587 for TLS)
    MAIL_USE_TLS = True,  # Enable TLS encryption
    MAIL_USERNAME = 'justinycareer@gmail.com',  # Use your email address
    MAIL_PASSWORD = 'FBB87DDE9ACAF8531DD469E77E81A28D9785',  # Use your email password
    SECURITY_PASSWORD_SALT = 'jo-enmedia_security_salt'
)

mail = Mail(app)


# info@jo-enmedia.com
def send_contact_email(user_email, subject, message):
    msg = Message(subject,
                  sender="justinycareer@gmail.com",
                  recipients=['justinycareer@gmail.com'],
                  reply_to=user_email)
    msg.body = message
    try:
        mail.send(msg)
        return 'Contact email sent successfully!'
    except Exception as e:
        import traceback
        print(e,traceback.format_exc())
        return f'Error sending contact email: {str(e)}\n{traceback.format_exc()}'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/contact_us', methods=['POST'])
def contact():
    data = request.json
    name = data.get('Name')
    userEmail = data.get('Email')
    phone = data.get("contactNumber")
    print(name)
    print(userEmail)
    print(phone)
    subject = "Jo-Enmedia user enquiry"

    fullMessage = "\nUser's Contact Detail: \n\n" + "Name: " + name + "\nEmail: " + userEmail + "\nContact Number: " + phone
    
    if not all([name, userEmail, phone]):
        return jsonify({'error': 'Missing data'}), 400

    response = send_contact_email(userEmail, subject, fullMessage)
    if response[0] == 'E':
        return jsonify({'error': response}), 400
    return jsonify({'message': response}), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get('PORT', 8080)))