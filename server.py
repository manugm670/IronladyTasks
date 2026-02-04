from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from livekit import api
import os
from dotenv import load_dotenv
import secrets

load_dotenv()

app = Flask(__name__, static_folder='static')
CORS(app)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/token', methods=['GET'])
def get_token():
    """Generate a token for the user to join the room"""
    try:
        api_key = os.getenv("LIVEKIT_API_KEY")
        api_secret = os.getenv("LIVEKIT_API_SECRET")
        livekit_url = os.getenv("LIVEKIT_URL")
        
        if not api_key or not api_secret or not livekit_url:
            return jsonify({"error": "Server configuration error"}), 500
        
        # Generate a unique room name or use a default
        room_name = "sthree-ai-room"
        
        # Generate unique participant identity
        participant_id = f"user-{secrets.token_hex(4)}"
        
        token = api.AccessToken(api_key, api_secret)
        token.with_identity(participant_id).with_name("User").with_grants(
            api.VideoGrants(
                room_join=True,
                room=room_name,
                can_publish=True,
                can_subscribe=True,
            )
        )
        
        return jsonify({
            "token": token.to_jwt(),
            "url": livekit_url,
            "room": room_name
        })
    
    except Exception as e:
        print(f"Error generating token: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    # Check if required environment variables are set
    required_vars = ['LIVEKIT_API_KEY', 'LIVEKIT_API_SECRET', 'LIVEKIT_URL']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Error: Missing environment variables: {', '.join(missing_vars)}")
        print("Please check your .env file")
        exit(1)
    
    print("\n" + "="*80)
    print("🎤 Sthree AI Server Starting...")
    print("="*80)
    print(f"\n✅ LiveKit URL: {os.getenv('LIVEKIT_URL')}")
    print(f"✅ API Key: {os.getenv('LIVEKIT_API_KEY')[:10]}...")
    print(f"\n🌐 Web UI will be available at: http://localhost:5000")
    print("\n" + "="*80 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
