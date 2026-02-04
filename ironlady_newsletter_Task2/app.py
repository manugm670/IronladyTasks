cd ironlady-newsletterfrom flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import anthropic
import schedule
import threading
import time
import json

load_dotenv(.env)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'ironlady-secret-key-2026')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletter.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email Configuration (using Gmail SMTP)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

db = SQLAlchemy(app)
mail = Mail(app)

# Database Models
class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    program_interest = db.Column(db.String(100))  # LEP, 1-Crore Club, etc.
    status = db.Column(db.String(20), default='active')  # active, unsubscribed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'program_interest': self.program_interest,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M')
        }

class NewsletterTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'subject': self.subject,
            'content': self.content,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M')
        }

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('newsletter_template.id'))
    status = db.Column(db.String(20), default='draft')  # draft, scheduled, sent
    scheduled_date = db.Column(db.DateTime)
    sent_date = db.Column(db.DateTime)
    recipients_count = db.Column(db.Integer, default=0)
    opened_count = db.Column(db.Integer, default=0)
    clicked_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    template = db.relationship('NewsletterTemplate', backref='campaigns')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'template_id': self.template_id,
            'status': self.status,
            'scheduled_date': self.scheduled_date.strftime('%Y-%m-%d %H:%M') if self.scheduled_date else None,
            'sent_date': self.sent_date.strftime('%Y-%m-%d %H:%M') if self.sent_date else None,
            'recipients_count': self.recipients_count,
            'opened_count': self.opened_count,
            'clicked_count': self.clicked_count,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M')
        }

# AI Content Generation
def generate_newsletter_content(topic, program_focus=None):
    """Generate newsletter content using Claude AI"""
    try:
        client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        
        prompt = f"""Generate a professional monthly newsletter for Iron Lady, a leadership organization for women.

Topic: {topic}
Program Focus: {program_focus if program_focus else 'General leadership development'}

The newsletter should include:
1. A compelling subject line
2. Engaging introduction
3. Main content about the topic (2-3 paragraphs)
4. Information about Iron Lady programs (LEP, 1-Crore Club, 100 Board Members, MBW)
5. A call-to-action
6. Inspiring quote for women leaders

Format as HTML with proper styling. Use warm, empowering tone suitable for women professionals.
Make it professional and inspiring."""

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return message.content[0].text
    except Exception as e:
        print(f"AI Generation Error: {e}")
        return None

# Routes
@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/dashboard-stats')
def dashboard_stats():
    """Get dashboard statistics"""
    total_subscribers = Subscriber.query.filter_by(status='active').count()
    total_campaigns = Campaign.query.count()
    sent_campaigns = Campaign.query.filter_by(status='sent').count()
    scheduled_campaigns = Campaign.query.filter_by(status='scheduled').count()
    
    recent_campaigns = Campaign.query.order_by(Campaign.created_at.desc()).limit(5).all()
    
    return jsonify({
        'total_subscribers': total_subscribers,
        'total_campaigns': total_campaigns,
        'sent_campaigns': sent_campaigns,
        'scheduled_campaigns': scheduled_campaigns,
        'recent_campaigns': [c.to_dict() for c in recent_campaigns]
    })

# CRUD - Subscribers
@app.route('/subscribers')
def subscribers():
    return render_template('subscribers.html')

@app.route('/api/subscribers', methods=['GET'])
def get_subscribers():
    subscribers = Subscriber.query.all()
    return jsonify([s.to_dict() for s in subscribers])

@app.route('/api/subscribers', methods=['POST'])
def create_subscriber():
    data = request.json
    
    existing = Subscriber.query.filter_by(email=data['email']).first()
    if existing:
        return jsonify({'error': 'Email already exists'}), 400
    
    subscriber = Subscriber(
        name=data['name'],
        email=data['email'],
        program_interest=data.get('program_interest', ''),
        status='active'
    )
    db.session.add(subscriber)
    db.session.commit()
    
    return jsonify(subscriber.to_dict()), 201

@app.route('/api/subscribers/<int:id>', methods=['PUT'])
def update_subscriber(id):
    subscriber = Subscriber.query.get_or_404(id)
    data = request.json
    
    subscriber.name = data.get('name', subscriber.name)
    subscriber.email = data.get('email', subscriber.email)
    subscriber.program_interest = data.get('program_interest', subscriber.program_interest)
    subscriber.status = data.get('status', subscriber.status)
    
    db.session.commit()
    return jsonify(subscriber.to_dict())

@app.route('/api/subscribers/<int:id>', methods=['DELETE'])
def delete_subscriber(id):
    subscriber = Subscriber.query.get_or_404(id)
    db.session.delete(subscriber)
    db.session.commit()
    return jsonify({'message': 'Subscriber deleted'})

# CRUD - Templates
@app.route('/templates')
def templates():
    return render_template('templates.html')

@app.route('/api/templates', methods=['GET'])
def get_templates():
    templates = NewsletterTemplate.query.all()
    return jsonify([t.to_dict() for t in templates])

@app.route('/api/templates', methods=['POST'])
def create_template():
    data = request.json
    
    template = NewsletterTemplate(
        title=data['title'],
        subject=data['subject'],
        content=data['content']
    )
    db.session.add(template)
    db.session.commit()
    
    return jsonify(template.to_dict()), 201

@app.route('/api/templates/<int:id>', methods=['PUT'])
def update_template(id):
    template = NewsletterTemplate.query.get_or_404(id)
    data = request.json
    
    template.title = data.get('title', template.title)
    template.subject = data.get('subject', template.subject)
    template.content = data.get('content', template.content)
    template.updated_at = datetime.utcnow()
    
    db.session.commit()
    return jsonify(template.to_dict())

@app.route('/api/templates/<int:id>', methods=['DELETE'])
def delete_template(id):
    template = NewsletterTemplate.query.get_or_404(id)
    db.session.delete(template)
    db.session.commit()
    return jsonify({'message': 'Template deleted'})

# AI Content Generation
@app.route('/api/generate-content', methods=['POST'])
def generate_content():
    data = request.json
    topic = data.get('topic', 'Monthly Leadership Update')
    program_focus = data.get('program_focus')
    
    content = generate_newsletter_content(topic, program_focus)
    
    if content:
        return jsonify({'content': content})
    else:
        return jsonify({'error': 'Failed to generate content'}), 500

# CRUD - Campaigns
@app.route('/campaigns')
def campaigns():
    return render_template('campaigns.html')

@app.route('/api/campaigns', methods=['GET'])
def get_campaigns():
    campaigns = Campaign.query.order_by(Campaign.created_at.desc()).all()
    return jsonify([c.to_dict() for c in campaigns])

@app.route('/api/campaigns', methods=['POST'])
def create_campaign():
    data = request.json
    
    campaign = Campaign(
        name=data['name'],
        template_id=data['template_id'],
        status='draft'
    )
    db.session.add(campaign)
    db.session.commit()
    
    return jsonify(campaign.to_dict()), 201

@app.route('/api/campaigns/<int:id>', methods=['PUT'])
def update_campaign(id):
    campaign = Campaign.query.get_or_404(id)
    data = request.json
    
    campaign.name = data.get('name', campaign.name)
    campaign.template_id = data.get('template_id', campaign.template_id)
    campaign.status = data.get('status', campaign.status)
    
    if data.get('scheduled_date'):
        campaign.scheduled_date = datetime.fromisoformat(data['scheduled_date'])
    
    db.session.commit()
    return jsonify(campaign.to_dict())

@app.route('/api/campaigns/<int:id>', methods=['DELETE'])
def delete_campaign(id):
    campaign = Campaign.query.get_or_404(id)
    db.session.delete(campaign)
    db.session.commit()
    return jsonify({'message': 'Campaign deleted'})

@app.route('/api/campaigns/<int:id>/send', methods=['POST'])
def send_campaign(id):
    """Send newsletter campaign to all active subscribers"""
    campaign = Campaign.query.get_or_404(id)
    template = NewsletterTemplate.query.get_or_404(campaign.template_id)
    subscribers = Subscriber.query.filter_by(status='active').all()
    
    sent_count = 0
    for subscriber in subscribers:
        try:
            # Personalize content
            personalized_content = template.content.replace('{{name}}', subscriber.name)
            
            msg = Message(
                subject=template.subject,
                recipients=[subscriber.email],
                html=personalized_content
            )
            mail.send(msg)
            sent_count += 1
        except Exception as e:
            print(f"Failed to send to {subscriber.email}: {e}")
    
    campaign.status = 'sent'
    campaign.sent_date = datetime.utcnow()
    campaign.recipients_count = sent_count
    db.session.commit()
    
    return jsonify({
        'message': f'Campaign sent to {sent_count} subscribers',
        'campaign': campaign.to_dict()
    })

# Automated Monthly Scheduling
def schedule_monthly_newsletter():
    """Schedule newsletter to be sent on the 1st of every month"""
    def send_monthly():
        # Get the latest active template or create default
        template = NewsletterTemplate.query.order_by(NewsletterTemplate.updated_at.desc()).first()
        
        if template:
            # Create and send campaign
            campaign = Campaign(
                name=f"Monthly Newsletter - {datetime.now().strftime('%B %Y')}",
                template_id=template.id,
                status='scheduled',
                scheduled_date=datetime.now()
            )
            db.session.add(campaign)
            db.session.commit()
            
            # Send the campaign
            with app.app_context():
                send_campaign(campaign.id)
    
    # Schedule for 1st of every month at 9:00 AM
    schedule.every().month.at("09:00").do(send_monthly)
    
    while True:
        schedule.run_pending()
        time.sleep(3600)  # Check every hour

# Initialize Database
def init_db():
    with app.app_context():
        db.create_all()
        
        # Add sample data if empty
        if Subscriber.query.count() == 0:
            samples = [
                Subscriber(name="Priya Sharma", email="priya@example.com", program_interest="LEP", status="active"),
                Subscriber(name="Anjali Mehta", email="anjali@example.com", program_interest="1-Crore Club", status="active"),
                Subscriber(name="Neha Gupta", email="neha@example.com", program_interest="100 Board Members", status="active"),
            ]
            db.session.add_all(samples)
            db.session.commit()
            print("✅ Sample subscribers added")

if __name__ == '__main__':
    init_db()
    
    # Start scheduler in background thread
    # scheduler_thread = threading.Thread(target=schedule_monthly_newsletter, daemon=True)
    # scheduler_thread.start()
    
    print("\n" + "="*80)
    print("🎉 Iron Lady Newsletter System Starting...")
    print("="*80)
    print("\n📧 Dashboard: http://localhost:5000")
    print("📊 Subscribers: http://localhost:5000/subscribers")
    print("📝 Templates: http://localhost:5000/templates")
    print("📨 Campaigns: http://localhost:5000/campaigns")
    print("\n" + "="*80 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
