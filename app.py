from flask import Flask, render_template, request, jsonify, send_from_directory, session, redirect, url_for
from flask_mail import Mail, Message
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'tattle-tale-dev-key-change-in-production')

# Register analytics dashboard blueprint
from dashboard.dashboard_routes import dashboard_bp
app.register_blueprint(dashboard_bp)


# ── Demo Authentication ─────────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Demo admin login — accepts any email for development purposes."""
    if session.get('admin_logged_in'):
        return redirect(url_for('dashboard.dashboard_home'))

    error = None
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not email or '@' not in email:
            error = 'Please enter a valid email address.'
        elif not password:
            error = 'Please enter a password.'
        else:
            # Demo mode: accept any credentials
            session['admin_logged_in'] = True
            session['admin_email'] = email
            return redirect(url_for('dashboard.dashboard_home'))

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    """Clear session and redirect to homepage."""
    session.clear()
    return redirect(url_for('home'))

# Flask-Mail configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'localhost')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

# Recipient for feedback emails
MAIL_TO = os.environ.get('MAIL_TO', os.environ.get('MAIL_DEFAULT_SENDER'))

mail = Mail(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about-lana')
def about_lana():
    return render_template('about-lana.html')

@app.route('/community-survey')
def community_survey():
    return render_template('community-survey.html')

@app.route('/turtle-tales-story')
def tattletale_story():
    return render_template('tattletale-story.html')

@app.route('/workshop-chapters')
def workshop_chapters():
    return render_template('workshop-chapters.html')

@app.route('/event-booking')
def event_booking():
    return render_template('event-booking.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy-policy.html')

@app.route('/contact')
def contact():
    return render_template('index.html', _anchor='contact')

@app.route('/api/feedback', methods=['POST'])
def handle_feedback():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'Invalid request data.'}), 400

    # Honeypot spam check
    if data.get('honeypot'):
        return jsonify({'success': False, 'message': 'Spam detected.'}), 400

    # Validate required fields
    rating = data.get('rating')
    help_status = data.get('helpStatus')
    email = data.get('email')
    message = data.get('message', '')

    if not email or '@' not in email:
        return jsonify({'success': False, 'message': 'Please enter a valid email address.'}), 400

    if not rating or not help_status:
        return jsonify({'success': False, 'message': 'Missing rating or help status.'}), 400

    # Build email
    submitted_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    msg = Message(
        subject='New Homepage Feedback - Tatle tale',
        recipients=[MAIL_TO],
        reply_to=email
    )
    msg.body = (
        f"Rating: {rating}\n"
        f"Help Status: {help_status}\n"
        f"User Email: {email}\n"
        f"Message:\n{message}\n\n"
        f"Submitted At: {submitted_at}\n"
    )

    try:
        mail.send(msg)
        print(f"[Feedback] Sent OK — rating={rating}, email={email}, at={submitted_at}")
        return jsonify({'success': True, 'message': 'Feedback sent successfully.'})
    except Exception as e:
        print(f"Mail error: {repr(e)}")
        return jsonify({'success': False, 'message': 'Failed to send feedback. Please try again later.'}), 500

@app.route('/api/community-survey', methods=['POST'])
def handle_community_survey():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'Invalid request data.'}), 400

    # Honeypot spam check
    if data.get('honeypot'):
        return jsonify({'success': False, 'message': 'Spam detected.'}), 400

    answers = data.get('answers')
    if not answers:
        return jsonify({'success': False, 'message': 'Please provide answers.'}), 400

    # Build email
    submitted_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    body_content = "New Community Survey Response\n\n"
    body_content += f"Submitted At: {submitted_at}\n\n"
    body_content += "----------------------------------\n"
    
    for question, answer in answers.items():
        if not answer:
            answer = "Not answered"
            
        body_content += f"{question}\n"
        if isinstance(answer, list):
            if not answer or len(answer) == 0:
                body_content += "Answer: Not answered\n"
            else:
                body_content += "Answers:\n"
                for opt in answer:
                    body_content += f"- {opt}\n"
        else:
            if len(str(answer)) > 50 or "\n" in str(answer):
                body_content += f"Answer:\n{answer}\n"
            else:
                body_content += f"Answer: {answer}\n"
        body_content += "\n"
        
    body_content += "----------------------------------"

    msg = Message(
        subject='New Community Survey Response - Tatle tale',
        recipients=[MAIL_TO]
    )
    msg.body = body_content

    try:
        mail.send(msg)
        print(f"[Survey] Sent OK at {submitted_at}")
        return jsonify({'success': True, 'message': 'Survey submitted successfully.'})
    except Exception as e:
        print(f"Mail error: {repr(e)}")
        return jsonify({'success': False, 'message': 'Failed to submit survey. Please try again.'}), 500

@app.route('/api/contact', methods=['POST'])
def handle_contact():
    data = request.form
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')
    
    msg = Message(f"New Contact Form Submission from {name}",
                  recipients=[MAIL_TO])
    msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
    
    try:
        if app.config['MAIL_USERNAME']:
            mail.send(msg)
            print(f"[Contact] Sent OK from {email}")
        return "Success"
    except Exception as e:
        print(f"Mail error: {repr(e)}")
        return "Error", 500

@app.route('/<path:filename>.js')
def serve_js(filename):
    return send_from_directory('templates', f"{filename}.js")

if __name__ == "__main__":
    app.run(debug=False, port=5000)
