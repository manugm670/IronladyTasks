# 🎙️ Sthree AI - Iron Lady Voice Assistant

A production-ready voice AI assistant for Iron Lady, helping women learn about leadership programs and training.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Make sure your `.env` file has:

```env
LIVEKIT_API_KEY=APIwB9yyvPb4qAA
LIVEKIT_API_SECRET=jPxFuyLiE3faRvwNxMseUjAboQcCfzCwam13swKkt8FA
LIVEKIT_URL=wss://aichat-0ghm95br.livekit.cloud
GOOGLE_API_KEY=AIzaSyBoYs0kEi0vxAgPR_m2Y5W2wh0s4ywGwDs
```

### 3. Run the Agent (Terminal 1)

```bash
python agent.py dev
```

Keep this running. You should see:
```
✅ registered worker
```

### 4. Run the Web Server (Terminal 2)

```bash
python server.py
```

You should see:
```
🎤 Sthree AI Server Starting...
🌐 Web UI will be available at: http://localhost:5000
```

### 5. Open the UI

Open your browser and go to:
```
http://localhost:5000
```

### 6. Use Sthree AI

1. **Click the microphone button once** to turn ON
2. **Wait for "Sthree AI is listening..."** status
3. **Start speaking naturally** - the AI will respond automatically
4. **Click again** to turn OFF when done

## 🌐 Deployment

### Deploy to Production

#### Option 1: Deploy to Heroku

1. Create `Procfile`:
```
web: gunicorn server:app
worker: python agent.py start
```

2. Install gunicorn:
```bash
pip install gunicorn
pip freeze > requirements.txt
```

3. Deploy:
```bash
heroku create sthree-ai
heroku config:set LIVEKIT_API_KEY=your_key
heroku config:set LIVEKIT_API_SECRET=your_secret
heroku config:set LIVEKIT_URL=your_url
heroku config:set GOOGLE_API_KEY=your_google_key
git push heroku main
heroku ps:scale web=1 worker=1
```

#### Option 2: Deploy to Railway

1. Push code to GitHub
2. Connect Railway to your repo
3. Add environment variables in Railway dashboard
4. Deploy automatically

#### Option 3: Deploy to AWS/DigitalOcean

1. Set up a server (Ubuntu recommended)
2. Install Python 3.10+
3. Clone your repository
4. Install dependencies
5. Use PM2 or systemd to run both processes:
   - `python agent.py start`
   - `python server.py`
6. Set up Nginx as reverse proxy for port 5000

### Environment Variables for Production

```env
LIVEKIT_API_KEY=your_production_key
LIVEKIT_API_SECRET=your_production_secret
LIVEKIT_URL=wss://your-production-server.livekit.cloud
GOOGLE_API_KEY=your_google_api_key
```

## 📁 Project Structure

```
sthree-ai/
├── agent.py              # Voice AI agent (LiveKit)
├── server.py             # Backend API server (Flask)
├── static/
│   └── index.html        # Frontend UI
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (not in git)
└── README.md            # This file
```

## 🎯 Features

- ✅ One-click ON/OFF button
- ✅ Automatic voice detection (VAD)
- ✅ Beautiful, responsive UI
- ✅ Secure token generation
- ✅ Production-ready
- ✅ Mobile-friendly
- ✅ Real-time voice conversation
- ✅ Specialized for Iron Lady content

## 🔧 Troubleshooting

### Agent won't connect
- Check if `agent.py` is running
- Verify environment variables in `.env`
- Check LiveKit server status

### UI shows "Connection failed"
- Make sure `server.py` is running on port 5000
- Check browser console for errors
- Verify `http://localhost:5000/api/health` returns `{"status":"ok"}`

### No audio
- Allow microphone permissions in browser
- Check if agent joined the room (look for "Participant connected" in agent logs)
- Verify audio output is not muted

## 📱 Testing

1. **Local Testing**: Use `http://localhost:5000`
2. **Network Testing**: Use your local IP (e.g., `http://192.168.1.x:5000`)
3. **Production Testing**: Use your deployed URL

## 🛡️ Security Notes

- Never commit `.env` file to git
- Regenerate API keys for production
- Use HTTPS in production
- Implement rate limiting for `/api/token` endpoint
- Add authentication if needed

## 📞 Support

For issues with:
- **LiveKit**: Check https://docs.livekit.io
- **Google AI**: Check https://ai.google.dev
- **Iron Lady**: Visit https://iamironlady.com

---

Made with ❤️ for empowering women leaders
