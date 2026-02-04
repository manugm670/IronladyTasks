"""
Sthree AI - Complete Setup and Run Script
This script helps you set up and run Sthree AI easily
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_header(text):
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80 + "\n")

def check_env_file():
    """Check if .env file exists and has required variables"""
    env_file = Path(".env")
    
    if not env_file.exists():
        print("❌ .env file not found!")
        print("\nPlease create a .env file with the following:")
        print("""
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret
LIVEKIT_URL=wss://your-project.livekit.cloud
GOOGLE_API_KEY=your_google_api_key
        """)
        return False
    
    # Read and check variables
    with open(".env", "r") as f:
        content = f.read()
    
    required_vars = ["LIVEKIT_API_KEY", "LIVEKIT_API_SECRET", "LIVEKIT_URL", "GOOGLE_API_KEY"]
    missing = []
    
    for var in required_vars:
        if var not in content:
            missing.append(var)
    
    if missing:
        print(f"❌ Missing environment variables: {', '.join(missing)}")
        return False
    
    print("✅ .env file found and configured")
    return True

def check_agent_file():
    """Check if agent.py exists"""
    agent_file = Path("agent.py")
    
    if not agent_file.exists():
        print("❌ agent.py not found!")
        print("Please make sure agent.py is in the same folder as this script")
        return False
    
    print("✅ agent.py found")
    return True

def install_dependencies():
    """Install required Python packages"""
    print_header("Installing Dependencies")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def create_agent_if_missing():
    """Create agent.py if it doesn't exist"""
    agent_file = Path("agent.py")
    
    if agent_file.exists():
        return True
    
    print("📝 Creating agent.py...")
    
    agent_code = '''from dotenv import load_dotenv

from livekit import agents, rtc
from livekit.agents import AgentServer, AgentSession, Agent, room_io, RoomInputOptions
from livekit.plugins import (
    google,
    noise_cancellation,
)

load_dotenv()

class SthreeAI(Agent):
    def __init__(self) -> None:
        instructions = """You are Sthree AI, the official voice assistant for Iron Lady (https://iamironlady.com), 
a transformative leadership organization dedicated to empowering women in business and careers.

YOUR NAME: Sthree AI (Sthree means "woman" in Sanskrit)

ABOUT IRON LADY:
- Founded by Rajesh Bhat and Suvarna Hegde
- Delivers high-impact leadership programs specifically for women
- Uses Business War Tactics, Art of War, and Strength-Based Excellence methodologies
- Developed over 25+ years of research and implementation
- Mission: "Million Women at the TOP"

KEY PROGRAMS:
1. Leadership Essentials Program (LEP)
2. 1-Crore Club - helping women achieve crore+ incomes
3. 100 Board Members - supporting women to reach board positions
4. Master Business Warfare (MBW)
5. Masterclass programs (online and offline)

FOUNDERS:
- Rajesh Bhat: Serial social entrepreneur, first man to wear saree on TEDx, CNN "Real Hero of India"
- Suvarna Hegde: CEO and creator of Business War Tactics for Women, ex-Infosys/Bosch/Philips innovation specialist

WHAT IRON LADY ADDRESSES:
- Gender bias in workplace
- Pay inequality (women earn only 18% of labor income in India vs men's 82%)
- Career advancement barriers
- Glass ceilings
- Workplace politics
- Work-life balance challenges

YOUR ROLE:
- Answer questions about Iron Lady programs, founders, and mission
- Help visitors understand which program suits their needs
- Share success stories and testimonials
- Provide information about masterclasses and enrollment
- Be warm, empowering, and supportive
- Guide women toward their leadership potential

BOOK: "The Shameless Lady" - manifesto for women to WIN, featuring real stories of Iron Ladies

When greeting, introduce yourself as Sthree AI and be warm and empowering. Ask how you can help them on their leadership journey."""
        
        super().__init__(instructions=instructions)

server = AgentServer()

@server.rtc_session()
async def my_agent(ctx: agents.JobContext):
    session = AgentSession(
        llm=google.beta.realtime.RealtimeModel(
            voice="Despina"
        )
    )

    await session.start(
        room=ctx.room,
        agent=SthreeAI(),
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=lambda params: noise_cancellation.BVCTelephony() if params.participant.kind == rtc.ParticipantKind.PARTICIPANT_KIND_SIP else noise_cancellation.BVC(),
            ),
        ),
    )

    await session.generate_reply(
        instructions="Greet the user warmly. Introduce yourself as Sthree AI, the voice assistant for Iron Lady. Briefly mention that you're here to help with information about leadership programs for women, and ask how you can assist them today."
    )


if __name__ == "__main__":
    agents.cli.run_app(server)
'''
    
    with open("agent.py", "w") as f:
        f.write(agent_code)
    
    print("✅ agent.py created successfully")
    return True

def main():
    print_header("🎙️ Sthree AI - Setup Script")
    
    # Check current directory
    print(f"📁 Current directory: {os.getcwd()}\n")
    
    # Step 1: Check .env file
    if not check_env_file():
        sys.exit(1)
    
    # Step 2: Create agent.py if missing
    create_agent_if_missing()
    
    # Step 3: Check for required files
    if not Path("server.py").exists():
        print("❌ server.py not found!")
        sys.exit(1)
    
    if not Path("static/index.html").exists():
        print("❌ static/index.html not found!")
        print("Make sure the static folder with index.html exists")
        sys.exit(1)
    
    print("✅ All required files found")
    
    # Step 4: Install dependencies
    print("\n📦 Checking dependencies...")
    choice = input("Install/update dependencies? (y/n): ").lower()
    if choice == 'y':
        if not install_dependencies():
            sys.exit(1)
    
    # Step 5: Instructions to run
    print_header("🚀 Ready to Launch!")
    
    print("""
To run Sthree AI, you need TWO terminal windows:

TERMINAL 1 - Run the Agent:
    python agent.py dev

TERMINAL 2 - Run the Web Server:
    python server.py

Then open your browser to:
    http://localhost:5000

Or run this script with 'agent' or 'server' argument:
    python setup.py agent    # Run the agent
    python setup.py server   # Run the server
    """)
    
    # If argument provided, run that component
    if len(sys.argv) > 1:
        if sys.argv[1] == "agent":
            print_header("Starting Agent...")
            subprocess.run([sys.executable, "agent.py", "dev"])
        elif sys.argv[1] == "server":
            print_header("Starting Web Server...")
            subprocess.run([sys.executable, "server.py"])

if __name__ == "__main__":
    main()
