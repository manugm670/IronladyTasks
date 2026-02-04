# 📧 Iron Lady - Automated Monthly Newsletter System

An AI-powered newsletter automation system for Iron Lady leadership organization, featuring subscriber management, AI content generation, campaign scheduling, and automated monthly newsletter distribution.

## 🎯 Project Overview

This system automates the entire newsletter workflow for Iron Lady, from content creation to delivery:

### **Business Problem Solved:**
- Manual newsletter creation is time-consuming
- Forgetting to send monthly newsletters
- Difficulty managing growing subscriber lists
- Need for personalized, high-quality content
- Tracking engagement and reach

### **Solution Features:**
✅ Complete CRUD for Subscribers, Templates, and Campaigns  
✅ AI-powered content generation using Claude AI  
✅ Automated monthly scheduling (1st of every month)  
✅ Email delivery with personalization  
✅ Campaign analytics and tracking  
✅ Beautiful, responsive dashboard  
✅ Real-time statistics  

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Gmail account (for sending emails)
- Anthropic API key (for AI features)

### Installation

1. **Clone/Download the project**
```bash
cd ironlady-newsletter
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**

Create a `.env` file:
```env
SECRET_KEY=your-secret-key-change-this
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
ANTHROPIC_API_KEY=your-anthropic-api-key
```

**Gmail Setup:**
- Enable 2-Factor Authentication in Google Account
- Go to Google Account → Security → App Passwords
- Generate a new app password for "Mail"
- Use that 16-character password in `.env`

4. **Run the application**
```bash
python app.py
```

5. **Access the dashboard**
```
http://localhost:5000
```

---

## 📱 Features Walkthrough

### 1. Dashboard (`/`)
- View total subscribers, campaigns, and stats
- Quick access to all features
- Recent campaigns list
- AI quick actions

### 2. Subscriber Management (`/subscribers`)
**CRUD Operations:**
- ✅ **Create:** Add new subscribers with name, email, program interest
- ✅ **Read:** View all subscribers in a table
- ✅ **Update:** Edit subscriber details and status
- ✅ **Delete:** Remove subscribers

**Features:**
- Track program interests (LEP, 1-Crore Club, MBW, etc.)
- Active/Unsubscribed status management
- Join date tracking

### 3. Newsletter Templates (`/templates`)
**CRUD Operations:**
- ✅ **Create:** Design custom HTML email templates
- ✅ **Read:** View all saved templates
- ✅ **Update:** Edit template content
- ✅ **Delete:** Remove unused templates

**AI Features:**
- Generate complete newsletters with Claude AI
- Automatic subject line creation
- Personalization with `{{name}}` placeholder
- HTML preview functionality

### 4. Email Campaigns (`/campaigns`)
**CRUD Operations:**
- ✅ **Create:** New campaigns with selected templates
- ✅ **Read:** View all campaigns and their status
- ✅ **Update:** Schedule or modify campaigns
- ✅ **Delete:** Remove campaigns

**Features:**
- Send immediately or schedule for later
- Automatic monthly scheduling
- Recipient tracking
- Campaign status (Draft, Scheduled, Sent)
- Email delivery with personalization

---

## 🤖 AI Integration

### Content Generation
Uses **Claude Sonnet 4** to generate:
- Professional newsletter content
- Compelling subject lines
- Information about Iron Lady programs
- Call-to-action sections
- Inspiring quotes for women leaders

### How to Use AI:
1. Go to Templates page
2. Click "AI Generate"
3. Enter topic (e.g., "Women Leadership in Tech 2026")
4. Select program focus (optional)
5. AI generates complete newsletter in seconds
6. Review and save as template

---

## 🔄 Automated Monthly Scheduling

The system automatically sends newsletters on the **1st of every month at 9:00 AM**.

### How it Works:
1. Latest active template is selected
2. Campaign is created automatically
3. Email sent to all active subscribers
4. Results tracked in campaign analytics

### To Enable Auto-Scheduling:
Uncomment these lines in `app.py`:
```python
# scheduler_thread = threading.Thread(target=schedule_monthly_newsletter, daemon=True)
# scheduler_thread.start()
```

---

## 📊 Database Schema

### Subscribers Table
```
id              INTEGER PRIMARY KEY
name            VARCHAR(100)
email           VARCHAR(120) UNIQUE
program_interest VARCHAR(100)
status          VARCHAR(20)  # active, unsubscribed
created_at      DATETIME
```

### NewsletterTemplate Table
```
id          INTEGER PRIMARY KEY
title       VARCHAR(200)
subject     VARCHAR(200)
content     TEXT
created_at  DATETIME
updated_at  DATETIME
```

### Campaign Table
```
id              INTEGER PRIMARY KEY
name            VARCHAR(200)
template_id     INTEGER FOREIGN KEY
status          VARCHAR(20)  # draft, scheduled, sent
scheduled_date  DATETIME
sent_date       DATETIME
recipients_count INTEGER
opened_count    INTEGER
clicked_count   INTEGER
created_at      DATETIME
```

---

## 🎥 Demo Video Script

### Part 1: Introduction (30 seconds)
"Welcome to the Iron Lady Automated Newsletter System. This application solves the challenge of manually managing newsletters by providing complete automation with AI-powered content generation."

### Part 2: CRUD Demonstration (60 seconds)

**Subscribers:**
- "Let me add a new subscriber" → Fill form → Submit
- "I can edit subscriber details" → Click edit → Modify → Save
- "And delete if needed" → Click delete → Confirm

**Templates:**
- "Create a template manually" → Fill HTML content → Save
- "Or use AI to generate one" → AI Generate → Enter topic → Generate
- "Preview and edit" → Click preview → Show content

**Campaigns:**
- "Create a campaign" → Select template → Save
- "Send immediately" → Click send → Confirm
- "Or schedule for later" → Click schedule → Select date → Schedule

### Part 3: AI Features (30 seconds)
"The AI integration uses Claude Sonnet 4 to generate professional newsletters tailored to Iron Lady's mission of empowering women leaders. It includes program information, success stories, and compelling calls-to-action."

### Part 4: Automation (30 seconds)
"The system automatically sends newsletters on the 1st of every month, tracks engagement, and manages the entire workflow without manual intervention."

---

## 🛠️ Technical Stack

- **Backend:** Flask (Python)
- **Database:** SQLite (SQLAlchemy ORM)
- **Frontend:** Bootstrap 5, JavaScript (Axios)
- **Email:** Flask-Mail (SMTP)
- **AI:** Anthropic Claude API
- **Scheduling:** Python Schedule library

---

## 📁 Project Structure

```
ironlady-newsletter/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── newsletter.db          # SQLite database (auto-created)
├── templates/             # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── dashboard.html    # Dashboard page
│   ├── subscribers.html  # Subscriber CRUD
│   ├── templates.html    # Template CRUD with AI
│   └── campaigns.html    # Campaign CRUD and sending
└── static/               # Static assets (if needed)
```

---

## 🔒 Security Notes

- Never commit `.env` file to version control
- Use app-specific passwords for Gmail
- Keep API keys secure
- Implement rate limiting in production
- Add user authentication for production deployment

---

## 🚀 Deployment Guide

### Option 1: Heroku
```bash
# Install Heroku CLI
heroku create ironlady-newsletter
heroku config:set SECRET_KEY=your-key
heroku config:set MAIL_USERNAME=your-email
heroku config:set MAIL_PASSWORD=your-password
heroku config:set ANTHROPIC_API_KEY=your-key
git push heroku main
```

### Option 2: Railway
1. Push to GitHub
2. Connect Railway to repository
3. Add environment variables in dashboard
4. Deploy automatically

### Option 3: VPS (DigitalOcean, AWS, etc.)
```bash
# On server
git clone your-repo
cd ironlady-newsletter
pip install -r requirements.txt
# Set up environment variables
# Use gunicorn or uwsgi
gunicorn app:app --bind 0.0.0.0:5000
```

---

## 📈 Future Enhancements

- [ ] Email open/click tracking
- [ ] A/B testing for subject lines
- [ ] Segmentation by program interest
- [ ] Rich text editor for templates
- [ ] CSV import for bulk subscribers
- [ ] Analytics dashboard with charts
- [ ] Integration with Iron Lady CRM
- [ ] SMS notifications
- [ ] Multi-language support

---

## 🤝 About Iron Lady

**Iron Lady** (https://iamironlady.com) is a transformative leadership organization dedicated to empowering women in business and careers.

**Programs:**
- Leadership Essentials Program (LEP)
- 1-Crore Club
- 100 Board Members
- Master Business Warfare (MBW)
- Various Masterclasses

**Mission:** "Million Women at the TOP"

---

## 📞 Support

For technical issues or questions:
- Check the code comments in `app.py`
- Review the troubleshooting section
- Test email sending with sample subscribers first
- Verify Gmail app password is correct

---

## 📝 License

This project is created for Iron Lady organization internal use.

---

**Created for Iron Lady TAP-JOB-ID-2421 Assignment**  
**Task 2: Internal Business Automation Solution**  
**Submission Date: February 2, 2026**
