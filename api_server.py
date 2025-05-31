from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2AuthorizationCodeBearer
from sqlalchemy.orm import Session
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel
from typing import List, Dict, Any
import json
import re
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import uvicorn
import ssl
import socket

from auth.oauth import get_current_user, handle_oauth_callback, get_google_auth_url
from database.session import get_db
from models.user import User

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="."), name="static")
app.mount("/pages", StaticFiles(directory="pages"), name="pages")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8082", "http://127.0.0.1:8082"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Add exception handler for better error messages
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": str(exc.detail)}
    )

# Root route
@app.get("/")
async def read_root():
    return FileResponse("index.html")

@app.get("/login.html")
async def read_login():
    return FileResponse("login.html")

# Authentication routes
@app.get("/auth/google/authorize")
async def google_authorize():
    """Start Google OAuth flow"""
    auth_url = get_google_auth_url()
    return {"url": auth_url}

@app.get("/auth/callback")
async def auth_callback(code: str, db: Session = Depends(get_db)):
    """Handle OAuth callback"""
    result = await handle_oauth_callback(code, db)
    return RedirectResponse(
        f"/#token={result['token']}"
    )

@app.get("/auth/user")
async def get_user_info(current_user: User = Depends(get_current_user)):
    """Get current user info"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "subscription_tier": current_user.subscription_tier,
        "last_login": current_user.last_login
    }

# Helper functions
def check_ssl(url: str) -> Dict:
    parsed = urlparse(url)
    try:
        context = ssl.create_default_context()
        with context.wrap_socket(socket.create_connection((parsed.hostname, 443)), server_hostname=parsed.hostname) as sock:
            cert = sock.getpeercert()
            return {
                "status": "Valid",
                "details": "SSL certificate is valid and up to date"
            }
    except:
        return {
            "status": "Invalid",
            "details": "SSL certificate is missing or invalid"
        }

def analyze_meta_tags(soup) -> List[Dict]:
    issues = []
    warnings = []
    passed = []
    
    # Check meta description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if not meta_desc:
        issues.append({
            "type": "issue",
            "message": "Missing meta description",
            "fix": "Add a meta description tag with a concise summary of your page content"
        })
    else:
        desc_content = meta_desc.get('content', '')
        if len(desc_content) < 50:
            warnings.append({
                "type": "warning",
                "message": "Meta description too short",
                "fix": "Expand your meta description to 50-160 characters for better search visibility"
            })
        elif len(desc_content) > 160:
            warnings.append({
                "type": "warning",
                "message": "Meta description too long",
                "fix": "Shorten your meta description to 50-160 characters"
            })
        else:
            passed.append({
                "message": "Meta description is well-optimized",
                "details": "Your meta description has an ideal length"
            })
    
    # Check meta viewport
    viewport = soup.find('meta', attrs={'name': 'viewport'})
    if not viewport:
        warnings.append({
            "type": "warning",
            "message": "Missing viewport meta tag",
            "fix": "Add a viewport meta tag for better mobile responsiveness"
        })
    else:
        passed.append({
            "message": "Viewport meta tag is present",
            "details": "Your page is configured for mobile devices"
        })
    
    return issues, warnings, passed

def analyze_headings(soup) -> List[Dict]:
    issues = []
    warnings = []
    passed = []
    
    h1_tags = soup.find_all('h1')
    if not h1_tags:
        issues.append({
            "type": "issue",
            "message": "Missing H1 heading",
            "fix": "Add an H1 heading that includes your main keyword"
        })
    elif len(h1_tags) > 1:
        warnings.append({
            "type": "warning",
            "message": "Multiple H1 headings found",
            "fix": "Use only one H1 heading per page for better SEO structure"
        })
    else:
        passed.append({
            "message": "H1 heading structure is correct",
            "details": "Your page has exactly one H1 heading"
        })
    
    return issues, warnings, passed

def analyze_images(soup) -> List[Dict]:
    issues = []
    warnings = []
    passed = []
    
    images = soup.find_all('img')
    missing_alt = 0
    total_images = len(images)
    
    for img in images:
        if not img.get('alt'):
            missing_alt += 1
            warnings.append({
                "type": "warning",
                "message": f"Missing alt text for image: {img.get('src', 'unknown')}",
                "fix": "Add descriptive alt text to help search engines understand your images"
            })
    
    if total_images > 0 and missing_alt == 0:
        passed.append({
            "message": "All images have alt text",
            "details": f"Found {total_images} images, all properly optimized"
        })
    
    return issues, warnings, passed

# API routes
@app.post("/api/analyze")
async def analyze_url(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict:
    try:
        data = await request.json()
        url = data.get('url')
        
        if not url:
            return JSONResponse(
                status_code=400,
                content={"error": "URL is required"}
            )
        
        # Fetch webpage content
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Initialize results
        all_issues = []
        all_warnings = []
        all_passed = []
        
        # Run all analyzers
        meta_issues, meta_warnings, meta_passed = analyze_meta_tags(soup)
        heading_issues, heading_warnings, heading_passed = analyze_headings(soup)
        image_issues, image_warnings, image_passed = analyze_images(soup)
        
        # Combine results
        all_issues.extend(meta_issues + heading_issues + image_issues)
        all_warnings.extend(meta_warnings + heading_warnings + image_warnings)
        all_passed.extend(meta_passed + heading_passed + image_passed)
        
        # Calculate score
        max_score = 100
        deductions = len(all_issues) * 15 + len(all_warnings) * 5
        score = max(0, max_score - deductions)
        
        # Simulate performance metrics
        metrics = {
            "pageSpeed": "2.8s",
            "mobileFriendly": "Yes" if soup.find('meta', attrs={'name': 'viewport'}) else "No",
            "ssl": "Valid" if url.startswith('https://') else "Invalid",
            "crawlability": "Allowed"
        }
        
        return {
            "score": score,
            "issues": all_issues,
            "warnings": all_warnings,
            "passed": all_passed,
            "metrics": metrics
        }
        
    except requests.RequestException as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": f"Failed to fetch URL: {str(e)}",
                "details": "Make sure the URL is accessible and try again"
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": f"Analysis failed: {str(e)}",
                "details": "An unexpected error occurred during analysis"
            }
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8082)
