# Google Cloud Deployment Setup - Complete

## ✓ Completed Steps

### 1. Google Cloud SDK
- ✓ Installed and configured
- ✓ Authenticated with `gcloud auth login`
- ✓ Project set to: `YOUR_PROJECT_ID`
- ✓ Application default credentials configured

### 2. Poetry Package Manager
- ✓ Installed Poetry 2.2.1
- ✓ Added to PATH: `/Users/siddhantgond/.local/bin`
- ✓ All dependencies installed successfully

### 3. Google Cloud APIs
- ✓ Vertex AI Platform API enabled
- ✓ Cloud Storage API enabled

### 4. Cloud Storage
- ✓ Bucket created: `gs://YOUR_BUCKET_NAME`
- ✓ Location: `us-central1`

### 5. Project Structure
```
shl-recommendation-system/
├── pyproject.toml          # Poetry configuration
├── .env                    # Environment variables (root)
├── DEPLOYMENT.md           # Full deployment guide
├── QUICKSTART.md           # Quick start guide
├── setup_gcloud.sh         # Automated setup script
├── deployment/
│   ├── __init__.py
│   ├── local.py           # Local testing script
│   ├── remote.py          # Remote deployment script
│   └── cleanup.py         # Cleanup script
├── app/
│   ├── .env               # Environment variables (app)
│   ├── main.py            # FastAPI application
│   ├── requirements.txt   # Requirements
│   └── shl_agent/
│       ├── agent.py       # ADK agent configuration
│       └── tools/
│           ├── search_tool.py
│           └── format_tool.py
└── data/
    └── individual-assessment.json
```

### 6. Environment Configuration
File: `.env`
```bash
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_CLOUD_STAGING_BUCKET=gs://YOUR_BUCKET_NAME
GEMINI_API_KEY=AIzaSyCqMxXXHLGbG-eRx7YLOXBwWPwZq4dnLOw
```

## Next Steps - Ready to Deploy!

### Step 1: Activate Virtual Environment
```bash
source /path/to/your/project/vir_env/bin/activate
export PATH="/Users/siddhantgond/.local/bin:$PATH"
cd /path/to/your/project/shl-recommendation-system
```

### Step 2: Test Locally (Recommended)
```bash
poetry run python deployment/local.py
```

This will:
- Create a local ADK app instance
- Initialize a test session
- Run 3 sample queries:
  - "I need a Java developer with good collaboration skills"
  - "Python programmer with leadership abilities"
  - "Sales representative assessment"

### Step 3: Deploy to Google Cloud
```bash
poetry run python deployment/remote.py --create
```

Expected output:
```
✓ Created remote app: projects/868684576817/locations/us-central1/reasoningEngines/XXXXX
```

**IMPORTANT:** Save the resource ID!

### Step 4: Create a Session
```bash
poetry run python deployment/remote.py --create_session --resource_id=YOUR_RESOURCE_ID
```

**IMPORTANT:** Save the session ID!

### Step 5: Test Deployment
```bash
poetry run python deployment/remote.py --send \
  --resource_id=YOUR_RESOURCE_ID \
  --session_id=YOUR_SESSION_ID \
  --message="I need a Python developer with leadership skills"
```

## Available Commands

### Deployment Management
```bash
# List all deployments
poetry run python deployment/remote.py --list

# Delete a deployment
poetry run python deployment/remote.py --delete --resource_id=YOUR_RESOURCE_ID

# Clean up all deployments
poetry run python deployment/cleanup.py
```

### Session Management
```bash
# List sessions for a user
poetry run python deployment/remote.py --list_sessions --resource_id=YOUR_RESOURCE_ID

# Get session details
poetry run python deployment/remote.py --get_session \
  --resource_id=YOUR_RESOURCE_ID \
  --session_id=YOUR_SESSION_ID
```

### Query Testing
```bash
# Send custom queries
poetry run python deployment/remote.py --send \
  --resource_id=YOUR_RESOURCE_ID \
  --session_id=YOUR_SESSION_ID \
  --message="Your custom query here"
```

## Troubleshooting

### If you get "command not found: poetry"
```bash
export PATH="/Users/siddhantgond/.local/bin:$PATH"
```

### If you get authentication errors
```bash
gcloud auth application-default login
```

### If you get permission errors
```bash
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="user:siddhant.gond22b@iiitg.ac.in" \
  --role="roles/aiplatform.user"
```

### If bucket doesn't exist
```bash
gsutil mb -l us-central1 gs://YOUR_BUCKET_NAME
```

## Cost Monitoring

Monitor your costs in Google Cloud Console:
- Navigate to: https://console.cloud.google.com/billing
- Set up budget alerts
- Review Agent Engine usage

## Documentation

- [DEPLOYMENT.md](DEPLOYMENT.md) - Detailed deployment guide
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [README.md](README.md) - Project overview

## Support

If you encounter issues:
1. Check environment variables in `.env`
2. Verify Google Cloud project has billing enabled
3. Ensure required APIs are enabled
4. Check you have necessary permissions

## Success Checklist

Before deploying, ensure:
- [ ] Virtual environment activated
- [ ] Poetry installed and in PATH
- [ ] Google Cloud authenticated
- [ ] APIs enabled
- [ ] Storage bucket created
- [ ] `.env` file configured
- [ ] Local test passed

You're all set! 🚀
