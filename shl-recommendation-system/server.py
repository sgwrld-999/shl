#!/usr/bin/env python3
"""
SHL Assessment Recommender - Simple Local Server
Runs on localhost with optional public URL via ngrok
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
import os
import sys
import time
from pathlib import Path

# Add app directory to path to import agent
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir))

# Try to import the search tool
HAS_SEARCH = False
try:
    from shl_agent.tools.search_tool import search_assessments
    HAS_SEARCH = True
    print("✅ Search tool loaded successfully")
except Exception as e:
    print(f"⚠️  Search tool not available: {e}")
    print("   Server will run in demo mode")

# Initialize FastAPI
app = FastAPI(
    title="SHL Assessment Recommender API",
    description="Intelligent assessment recommendations for hiring managers",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware for browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class RecommendationRequest(BaseModel):
    """Request for assessment recommendations"""
    query: str
    job_level: Optional[str] = ""
    industry: Optional[str] = ""
    language: Optional[str] = "English"
    max_results: Optional[int] = 5

class Assessment(BaseModel):
    """Single assessment recommendation"""
    name: str
    url: Optional[str] = None
    description: str
    relevance_score: Optional[float] = None
    job_family: Optional[str] = None
    test_type: Optional[str] = None
    duration: Optional[str] = None
    adaptive_available: Optional[bool] = None
    remote_available: Optional[bool] = None

class RecommendationResponse(BaseModel):
    """Response with recommendations"""
    status: str
    query: str
    recommendations: List[Assessment]
    total_results: int
    processing_time_ms: Optional[float] = None
    mode: Optional[str] = "production" if HAS_SEARCH else "demo"

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
def root():
    """Root endpoint - API info"""
    return {
        "service": "SHL Assessment Recommender",
        "version": "1.0.0",
        "status": "operational",
        "search_enabled": HAS_SEARCH,
        "mode": "production" if HAS_SEARCH else "demo",
        "endpoints": {
            "health": "GET /health",
            "recommend": "POST /recommend",
            "test": "POST /test",
            "filters": "GET /filters",
            "docs": "/docs"
        },
        "submission_info": {
            "project": "SHL Assessment Recommendation System",
            "features": [
                "348+ SHL assessments",
                "Semantic search with FAISS",
                "Job role matching",
                "Test type recommendations"
            ]
        }
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "search_available": HAS_SEARCH,
        "mode": "production" if HAS_SEARCH else "demo",
        "service": "shl-recommender",
        "assessments_count": 348 if HAS_SEARCH else 0
    }

@app.post("/recommend", response_model=RecommendationResponse)
async def recommend_assessments(request: RecommendationRequest):
    """
    Get assessment recommendations based on hiring query
    
    **Example Request:**
    ```json
    {
        "query": "Need senior Java developer with 5 years experience",
        "job_level": "Senior",
        "industry": "Technology",
        "language": "English",
        "max_results": 5
    }
    ```
    
    **Returns:** List of recommended SHL assessments with relevance scores
    """
    
    start_time = time.time()
    
    if not HAS_SEARCH:
        # Demo mode - return mock data
        return RecommendationResponse(
            status="success",
            query=request.query,
            recommendations=[
                Assessment(
                    name="Technical Skills Assessment - Java Developer",
                    url="https://www.shl.com/solutions/products/assessments/",
                    description=f"Comprehensive technical assessment recommended for: {request.query}. Evaluates Java programming, problem-solving, and software development skills.",
                    relevance_score=0.95,
                    job_family="IT / Technology",
                    test_type="Technical + Cognitive",
                    duration="60 minutes",
                    adaptive_available=True,
                    remote_available=True
                ),
                Assessment(
                    name="Problem Solving & Critical Thinking",
                    url="https://www.shl.com/solutions/products/assessments/",
                    description="Evaluates analytical abilities, logical reasoning, and problem-solving skills essential for technical roles.",
                    relevance_score=0.88,
                    job_family="General",
                    test_type="Cognitive Abilities",
                    duration="30 minutes",
                    adaptive_available=True,
                    remote_available=True
                ),
                Assessment(
                    name="Personality Profile for IT Professionals",
                    url="https://www.shl.com/solutions/products/assessments/",
                    description="Assesses personality traits relevant to IT roles including attention to detail, teamwork, and adaptability.",
                    relevance_score=0.82,
                    job_family="IT / Technology",
                    test_type="Personality & Behavioral",
                    duration="25 minutes",
                    adaptive_available=False,
                    remote_available=True
                ),
            ],
            total_results=3,
            processing_time_ms=(time.time() - start_time) * 1000,
            mode="demo"
        )
    
    try:
        # Use actual search tool
        # Build search parameters
        search_params = {
            "query": request.query,
            "max_results": request.max_results or 5
        }
        
        # Add optional filters if provided
        if request.job_level:
            search_params["job_level"] = request.job_level
        if request.industry:
            search_params["industry"] = request.industry
        
        # Call the search function
        results = search_assessments(**search_params)
        
        # Parse results - the search_assessments function returns a dict
        if isinstance(results, dict):
            assessments_data = results.get("recommendations", [])
        elif isinstance(results, list):
            assessments_data = results
        else:
            assessments_data = []
        
        # Convert to Assessment objects
        recommendations = []
        for item in assessments_data:
            recommendations.append(Assessment(
                name=item.get("name", "Unknown Assessment"),
                url=item.get("url", "https://www.shl.com/"),
                description=item.get("description", ""),
                relevance_score=item.get("relevance_score") or item.get("score"),
                job_family=item.get("job_family"),
                test_type=item.get("test_type"),
                duration=item.get("duration"),
                adaptive_available=item.get("adaptive_available"),
                remote_available=item.get("remote_available")
            ))
        
        processing_time = (time.time() - start_time) * 1000
        
        return RecommendationResponse(
            status="success",
            query=request.query,
            recommendations=recommendations,
            total_results=len(recommendations),
            processing_time_ms=processing_time,
            mode="production"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Recommendation failed: {str(e)}"
        )

@app.post("/test")
def test_endpoint(data: Dict[str, Any]):
    """
    Simple test endpoint to verify API is working
    
    **Example:**
    ```json
    {"message": "Hello SHL!"}
    ```
    """
    return {
        "status": "success",
        "received": data,
        "echo": data.get("message", "No message provided"),
        "search_enabled": HAS_SEARCH,
        "mode": "production" if HAS_SEARCH else "demo"
    }

@app.get("/filters")
def get_available_filters():
    """
    Get available filter options for assessments
    """
    return {
        "job_levels": [
            "Entry", "Junior", "Mid", "Senior", 
            "Lead", "Principal", "Executive"
        ],
        "industries": [
            "Technology", "Healthcare", "Finance", 
            "Retail", "Manufacturing", "Education",
            "Consulting", "Media", "Energy"
        ],
        "languages": [
            "English", "Spanish", "French", "German", 
            "Mandarin", "Portuguese", "Arabic", "Japanese"
        ],
        "job_families": [
            "IT / Technology", "Finance / Accounting", 
            "Marketing / Sales", "Operations / Supply Chain", 
            "HR / People Operations", "Engineering", 
            "Customer Service", "Healthcare"
        ],
        "test_types": [
            "Cognitive Abilities",
            "Personality & Behavioral",
            "Technical Skills",
            "Job Competencies",
            "Simulations",
            "Knowledge Tests"
        ]
    }

@app.get("/about")
def about():
    """Information about the service"""
    return {
        "project": "SHL Assessment Recommendation System",
        "description": "AI-powered assessment recommendations for hiring managers",
        "features": [
            "348+ SHL assessments in database",
            "Semantic search using FAISS vector database",
            "Job role and skills matching",
            "Test type recommendations",
            "Adaptive and remote testing support"
        ],
        "technology": {
            "backend": "FastAPI (Python)",
            "search": "FAISS + Sentence Transformers",
            "ml_model": "all-MiniLM-L6-v2",
            "data": "348 SHL individual assessments"
        },
        "submission": {
            "for": "SHL Technical Assessment",
            "date": "November 2025"
        }
    }

# ============================================================================
# MAIN - SERVER STARTUP
# ============================================================================

if __name__ == "__main__":
    import datetime
    
    # Configuration
    HOST = "0.0.0.0"
    PORT = int(os.getenv("PORT", 8000))
    
    print("=" * 70)
    print("🚀 SHL ASSESSMENT RECOMMENDER - LOCAL SERVER")
    print("=" * 70)
    print(f"📍 Host: {HOST}")
    print(f"🔌 Port: {PORT}")
    print(f"🔍 Search: {'Enabled (348 assessments)' if HAS_SEARCH else 'Demo Mode'}")
    print(f"⏰ Started: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    print("📖 API Documentation:")
    print(f"   http://localhost:{PORT}/docs")
    print(f"   http://localhost:{PORT}/redoc")
    print()
    print("🔗 Endpoints:")
    print(f"   GET  http://localhost:{PORT}/")
    print(f"   GET  http://localhost:{PORT}/health")
    print(f"   POST http://localhost:{PORT}/recommend")
    print(f"   POST http://localhost:{PORT}/test")
    print(f"   GET  http://localhost:{PORT}/filters")
    print(f"   GET  http://localhost:{PORT}/about")
    print()
    print("💡 To create public URL:")
    print("   python start_public.py")
    print()
    print("🛑 To stop: Press Ctrl+C")
    print("=" * 70)
    print()
    
    # Start server
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        log_level="info"
    )
