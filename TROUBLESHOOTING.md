# 🔧 Troubleshooting Guide - Sthree AI

## Problem: "localhost not working" or "Connection failed"

### Quick Fix Steps:

#### 1. Make sure BOTH processes are running

You need TWO terminal windows open:

**Terminal 1:**
```bash
python agent.py dev
```
Should show:
```
✅ registered worker
```

**Terminal 2:**
```bash
python server.py
```
Should show:
```
🌐 Web UI will be available at: http://localhost:5000
```

#### 2. Check if server is actually running

Open a new browser tab and go to:
```
http://localhost:5000/api/health
```

You should see:
```json
{"status":"ok"}
```

If you see this, the server is working!

#### 3. Common Issues:

**Issue: "Address already in use" or "Port 5000 is already in use"**

Solution: Kill the existing process or use a different port

Windows:
```bash
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F
```

Or change the port in server.py:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Changed from 5000 to 5001
```

Then open `http://localhost:5001`

---

**Issue: "Module not found" errors**

Solution: Install dependencies
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install flask flask-cors livekit python-dotenv livekit-agents
```

---

**Issue: Agent shows "ws_url is required"**

Solution: Check your .env file
- Make sure .env file exists in the same folder
- Check that there are NO SPACES around the = sign
- Correct: `LIVEKIT_URL=wss://...`
- Wrong: `LIVEKIT_URL = wss://...`

---

**Issue: "Connection failed" in browser**

Solution: Check browser console (F12)
- Look for specific error messages
- Common causes:
  - Server not running
  - Wrong URL (should be http://localhost:5000)
  - Firewall blocking connection

---

**Issue: "No audio" or "Can't hear Sthree AI"**

Solution:
1. Check browser permissions - allow microphone access
2. Check if agent joined the room (look in agent terminal for "Participant connected")
3. Check system volume and browser audio settings
4. Try a different browser (Chrome works best)

---

**Issue: Microphone button doesn't respond**

Solution:
1. Check browser console (F12) for JavaScript errors
2. Make sure you clicked "Allow" for microphone permissions
3. Wait for "Sthree AI is listening..." message before speaking
4. Try refreshing the page

---

## 🎯 Step-by-Step Verification

### Step 1: Check File Structure
Your folder should have:
```
📁 sthree-ai/
├── agent.py
├── server.py
├── .env
├── requirements.txt
├── start.bat (for Windows)
└── 📁 static/
    └── index.html
```

### Step 2: Verify .env File
Open .env and check:
```env
LIVEKIT_API_KEY=APIwB9yyvPb4qAA
LIVEKIT_API_SECRET=jPxFuyLiE3faRvwNxMseUjAboQcCfzCwam13swKkt8FA
LIVEKIT_URL=wss://aichat-0ghm95br.livekit.cloud
GOOGLE_API_KEY=AIzaSyBoYs0kEi0vxAgPR_m2Y5W2wh0s4ywGwDs
```

### Step 3: Test Agent First
```bash
python agent.py dev
```
Wait until you see:
```
✅ registered worker
```

### Step 4: Test Server
In a NEW terminal:
```bash
python server.py
```
Should show:
```
🎤 Sthree AI Server Starting...
🌐 Web UI will be available at: http://localhost:5000
```

### Step 5: Test Health Endpoint
Open browser:
```
http://localhost:5000/api/health
```
Should return: `{"status":"ok"}`

### Step 6: Open UI
```
http://localhost:5000
```

---

## 🪟 Windows Specific Issues

**Issue: Python not recognized**

Solution: Make sure Python is in PATH
```bash
python --version
```

If it doesn't work, try:
```bash
py --version
```

Then use `py` instead of `python`:
```bash
py agent.py dev
py server.py
```

---

**Issue: Permission denied**

Solution: Run terminal as Administrator
- Right-click CMD or PowerShell
- Select "Run as Administrator"

---

## 🔍 Debug Mode

To see detailed logs, edit server.py and change:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

This will show all requests and errors.

---

## 💡 Still Not Working?

1. **Restart everything:**
   - Close all terminals
   - Close browser
   - Start fresh

2. **Try the easy way:**
   - Double-click `start.bat` (Windows only)
   - This opens both terminals automatically

3. **Check the basics:**
   - Is Python installed? `python --version`
   - Is pip working? `pip --version`
   - Are you in the right folder? `dir` (Windows) or `ls` (Mac/Linux)

4. **Nuclear option - Fresh install:**
   ```bash
   # Remove venv if exists
   rmdir /s venv
   
   # Create new venv
   python -m venv venv
   venv\Scripts\activate
   
   # Install everything fresh
   pip install -r requirements.txt
   ```

---

## 📞 Need More Help?

Share the EXACT error message you're seeing, including:
- Which step failed
- Full error text
- Terminal output
- Browser console errors (F12)

Common log locations:
- Agent logs: In the terminal running `agent.py`
- Server logs: In the terminal running `server.py`
- Browser logs: F12 → Console tab
