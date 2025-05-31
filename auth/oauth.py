from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2AuthorizationCodeBearer
from sqlalchemy.orm import Session
from google.oauth2 import id_token
from google.auth.transport import requests
from google_auth_oauthlib.flow import Flow
from models.user import User
from database.session import get_db
from datetime import datetime
import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# OAuth 2.0 client configuration
CLIENT_SECRETS_FILE = Path(__file__).parent.parent / "client_secrets.json"
SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]

# Create Flow instance with client secrets
flow = Flow.from_client_secrets_file(
    str(CLIENT_SECRETS_FILE),
    scopes=SCOPES,
    redirect_uri="http://localhost:8082/auth/callback"
)

def get_google_auth_url():
    """Generate Google OAuth2 authorization URL"""
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    return authorization_url

async def verify_google_token(token: str):
    """Verify Google OAuth2 token and return user info"""
    try:
        id_info = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            flow.client_config['client_id']
        )
        return id_info
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )

async def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> User:
    """Get current user from request"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    token = auth_header.split(' ')[1]
    try:
        user_info = await verify_google_token(token)
        google_id = user_info['sub']
        
        # Get or create user
        user = db.query(User).filter(User.google_id == google_id).first()
        if not user:
            user = User(
                email=user_info.get('email'),
                full_name=user_info.get('name'),
                google_id=google_id,
                is_active=True,
                created_at=datetime.utcnow(),
                last_login=datetime.utcnow()
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            user.last_login = datetime.utcnow()
            db.commit()
        
        return user
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"}
        )

async def handle_oauth_callback(code: str, db: Session):
    """Handle OAuth callback and return user info"""
    try:
        flow.fetch_token(code=code)
        credentials = flow.credentials
        
        id_info = id_token.verify_oauth2_token(
            credentials.id_token,
            requests.Request(),
            flow.client_config['client_id']
        )
        
        # Get or create user
        google_id = id_info['sub']
        user = db.query(User).filter(User.google_id == google_id).first()
        
        if not user:
            user = User(
                email=id_info.get('email'),
                full_name=id_info.get('name'),
                google_id=google_id,
                is_active=True,
                created_at=datetime.utcnow(),
                last_login=datetime.utcnow()
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            user.last_login = datetime.utcnow()
            db.commit()
        
        return {
            'token': credentials.id_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'full_name': user.full_name,
                'subscription_tier': user.subscription_tier
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Failed to process OAuth callback: {str(e)}"
        )
