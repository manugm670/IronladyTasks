"""
Iron Lady Newsletter System - Quick Start Script
This script helps you set up the application quickly
"""

import os
import sys
from pathlib import Path

def print_header(text):
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80 + "\n")

def check_python_version():
    """Check if Python version is 3.8+"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def check_env_file():
    """Check if .env file exists"""
    env_file = Path(".env")
    
    if not env_file.exists():
        print("❌ .env file not found!")
        print("\nCreating .env from template...")
        
        if Path(".env.example").exists():
            import shutil
            shutil.copy(".env.example", ".env")
            print("✅ .env file created!")
            print("\n⚠️  IMPORTANT: Edit .env file with your credentials:")
            print("   - MAIL_USERNAME: Your Gmail address")
            print("   - MAIL_PASSWORD: Gmail app-specific password")
            print("   - ANTHROPIC_API_KEY: Your Anthropic API key")
            return False
        else:
            print("❌ .env.example not found")
            return False
    
    # Check if env file has required variables
    with open(".env", "r") as f:
        content = f.read()
    
    required = ["MAIL_USERNAME", "MAIL_PASSWORD", "ANTHROPIC_API_KEY"]
    missing = []
    
    for var in required:
        if var not in content or f"{var}=your-" in content:
            missing.append(var)
    
    if missing:
        print(f"⚠️  Please configure these variables in .env:")
        for var in missing:
            print(f"   - {var}")
        return False
    
    print("✅ .env file configured")
    return True

def install_dependencies():
    """Install required packages"""
    print("📦 Installing dependencies...")
    
    try:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "-q"])
        print("✅ All dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def check_gmail_setup():
    """Provide Gmail setup instructions"""
    print("\n📧 Gmail Setup Instructions:")
    print("="*80)
    print("""
1. Go to your Google Account: https://myaccount.google.com/
2. Navigate to Security → 2-Step Verification (enable if not enabled)
3. Navigate to Security → App passwords
4. Select 'Mail' and 'Other (Custom name)'
5. Name it 'Iron Lady Newsletter'
6. Copy the 16-character password
7. Paste it in .env as MAIL_PASSWORD (no spaces)

⚠️  Do NOT use your regular Gmail password!
    """)

def print_next_steps():
    """Print what to do next"""
    print_header("🎉 Setup Complete!")
    print("""
Your Iron Lady Newsletter System is ready to run!

Next steps:

1. Make sure your .env file is configured with:
   ✓ MAIL_USERNAME (your Gmail)
   ✓ MAIL_PASSWORD (Gmail app password)
   ✓ ANTHROPIC_API_KEY (for AI features)

2. Run the application:
   
   python app.py

3. Open your browser to:
   
   http://localhost:5000

4. Start using the system:
   - Add subscribers
   - Generate newsletters with AI
   - Create and send campaigns

For detailed instructions, see README.md
For demo video guide, see DEMO_VIDEO_GUIDE.md
    """)

def main():
    print_header("📧 Iron Lady Newsletter System - Quick Setup")
    
    # Step 1: Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Step 2: Check if we're in the right directory
    if not Path("app.py").exists():
        print("❌ app.py not found!")
        print("   Make sure you're in the ironlady-newsletter directory")
        sys.exit(1)
    
    print("✅ Project files found")
    
    # Step 3: Check/create .env file
    env_configured = check_env_file()
    
    # Step 4: Install dependencies
    print("\n" + "-"*80)
    choice = input("\nInstall/update dependencies? (y/n): ").lower()
    if choice == 'y':
        if not install_dependencies():
            sys.exit(1)
    
    # Step 5: Provide Gmail setup guide
    if not env_configured:
        check_gmail_setup()
        print("\n⚠️  Please configure .env file before running the app")
        print("   Then run: python app.py")
        sys.exit(0)
    
    # Step 6: Print next steps
    print_next_steps()
    
    # Step 7: Ask if user wants to run now
    choice = input("\nRun the application now? (y/n): ").lower()
    if choice == 'y':
        print("\n" + "="*80)
        print("Starting Iron Lady Newsletter System...")
        print("="*80 + "\n")
        
        import subprocess
        try:
            subprocess.run([sys.executable, "app.py"])
        except KeyboardInterrupt:
            print("\n\n✋ Application stopped by user")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✋ Setup cancelled by user")
