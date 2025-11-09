# How to Access Your SHL Recommendation System

## Your Deployment Information

**Resource ID:**
```
projects/YOUR_PROJECT_NUMBER/locations/us-central1/reasoningEngines/YOUR_RESOURCE_ID
```

**Project:** YOUR_PROJECT_ID  
**Location:** us-central1  
**Status:** Building (5-10 minutes) - Fixed faiss-cpu version issue

## Monitor Deployment Progress

**View Logs:**
https://console.cloud.google.com/logs/query?project=YOUR_PROJECT_ID

**View in Console:**
https://console.cloud.google.com/vertex-ai/reasoning-engines?project=YOUR_PROJECT_ID

## Once Deployment is Complete (5-10 minutes)

### Step 1: Activate Environment
```bash
source /Users/siddhantgond/Desktop/shl/vir_env/bin/activate
export PATH="/Users/siddhantgond/.local/bin:$PATH"
cd /Users/siddhantgond/Desktop/shl/shl-recommendation-system
```

Or use the quick activation script:
```bash
source activate.sh
```

### Step 2: Create a Session
```bash
poetry run python deployment/remote.py --create_session \
  --resource_id=projects/YOUR_PROJECT_NUMBER/locations/us-central1/reasoningEngines/YOUR_RESOURCE_ID
```

**Save the session ID** from the output!

### Step 3: Send Your First Query
```bash
poetry run python deployment/remote.py --send \
  --resource_id=projects/YOUR_PROJECT_NUMBER/locations/us-central1/reasoningEngines/YOUR_RESOURCE_ID \
  --session_id=YOUR_SESSION_ID \
  --message="I need a Python developer with leadership skills"
```

## Example Queries to Try

### 1. Technical + Behavioral
```bash
poetry run python deployment/remote.py --send \
  --resource_id=projects/YOUR_PROJECT_NUMBER/locations/us-central1/reasoningEngines/YOUR_RESOURCE_ID \
  --session_id=YOUR_SESSION_ID \
  --message="Java developer who can collaborate with business teams"
```

### 2. Pure Technical
```bash
poetry run python deployment/remote.py --send \
  --resource_id=projects/YOUR_PROJECT_NUMBER/locations/us-central1/reasoningEngines/YOUR_RESOURCE_ID \
  --session_id=YOUR_SESSION_ID \
  --message="Python, SQL and JavaScript proficiency"
```

### 3. Sales Role
```bash
poetry run python deployment/remote.py --send \
  --resource_id=projects/YOUR_PROJECT_NUMBER/locations/us-central1/reasoningEngines/YOUR_RESOURCE_ID \
  --session_id=YOUR_SESSION_ID \
  --message="Sales representative with strong communication"
```

### 4. Leadership Assessment
```bash
poetry run python deployment/remote.py --send \
  --resource_id=projects/YOUR_PROJECT_NUMBER/locations/us-central1/reasoningEngines/YOUR_RESOURCE_ID \
  --session_id=YOUR_SESSION_ID \
  --message="Leadership and management skills for senior roles"
```

## Useful Commands

### List All Deployments
```bash
poetry run python deployment/remote.py --list
```

### List Sessions
```bash
poetry run python deployment/remote.py --list_sessions \
  --resource_id=projects/YOUR_PROJECT_NUMBER/locations/us-central1/reasoningEngines/YOUR_RESOURCE_ID
```

### Get Session Details
```bash
poetry run python deployment/remote.py --get_session \
  --resource_id=projects/YOUR_PROJECT_NUMBER/locations/us-central1/reasoningEngines/YOUR_RESOURCE_ID \
  --session_id=YOUR_SESSION_ID
```

### Delete Deployment (when done)
```bash
poetry run python deployment/remote.py --delete \
  --resource_id=projects/YOUR_PROJECT_NUMBER/locations/us-central1/reasoningEngines/YOUR_RESOURCE_ID
```

## Check Deployment Status

Run this command to check if deployment is complete:
```bash
gcloud ai reasoning-engines describe YOUR_RESOURCE_ID \
  --region=us-central1 \
  --project=YOUR_PROJECT_ID
```

Look for `state: ACTIVE` in the output.

## Alternative: Using Python Script

Create a file `check_deployment.py`:
```python
import vertexai
from vertexai import agent_engines

vertexai.init(
    project="YOUR_PROJECT_ID",
    location="us-central1",
    staging_bucket="gs://YOUR_BUCKET_NAME"
)

resource_id = "projects/YOUR_PROJECT_NUMBER/locations/us-central1/reasoningEngines/YOUR_RESOURCE_ID"

try:
    remote_app = agent_engines.get(resource_id)
    print("✓ Deployment is ready!")
    print(f"Resource: {remote_app.resource_name}")
except Exception as e:
    print(f"Deployment not ready yet: {e}")
```

Run it:
```bash
poetry run python check_deployment.py
```

## Access via Google Cloud Console

1. Go to: https://console.cloud.google.com/vertex-ai/reasoning-engines?project=YOUR_PROJECT_ID
2. Find your agent: `YOUR_RESOURCE_ID`
3. Click to view details and test directly in the console

## Integration into Your Application

Once deployed, you can integrate it into your FastAPI app:

```python
from vertexai import agent_engines
import vertexai

# Initialize
vertexai.init(
    project="YOUR_PROJECT_ID",
    location="us-central1",
    staging_bucket="gs://YOUR_BUCKET_NAME"
)

# Get the deployed agent
resource_id = "projects/YOUR_PROJECT_NUMBER/locations/us-central1/reasoningEngines/YOUR_RESOURCE_ID"
remote_app = agent_engines.get(resource_id)

# Create session
session = remote_app.create_session(user_id="user123")

# Query
for event in remote_app.stream_query(
    user_id="user123",
    session_id=session['id'],
    message="Python developer assessment"
):
    print(event)
```

## Costs

Monitor your usage and costs:
- **Console:** https://console.cloud.google.com/billing?project=YOUR_PROJECT_ID
- **Agent Engine:** Charged per session
- **Gemini API:** Charged per token

## Troubleshooting

### Common Issues

#### 1. "Build failed" Error
- **Cause:** Dependency conflicts or timeout during build
- **Solution:** Check Cloud Build logs, verify requirements.txt, ensure numpy/faiss versions are compatible

#### 2. "ReasoningEngine does not exist"
- **Cause:** Deployment failed or hasn't completed yet
- **Solution:** Wait 5-10 minutes for build, check logs for errors

#### 3. "DefaultCredentialsError"
- **Cause:** Not authenticated with Google Cloud
- **Solution:** Run `gcloud auth application-default login`

#### 4. Session creation fails
- **Cause:** Deployment not in ACTIVE state
- **Solution:** Verify deployment with `poetry run python deployment/remote.py --list`

### Getting Help

If you encounter issues:
1. **Check build logs:** https://console.cloud.google.com/logs/query?project=YOUR_PROJECT_ID
2. **Verify deployment status:** Run the check_status.py script
3. **Review configuration:** Ensure .env file has correct values
4. **Validate credentials:** `gcloud auth application-default login`

## Configuration Reference

### Required Environment Variables

Create a `.env` file in the project root (or use `app/.env`):

```bash
# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_CLOUD_STAGING_BUCKET=gs://YOUR_BUCKET_NAME

# API Keys
GEMINI_API_KEY=your-api-key-here

# Optional: Enable Vertex AI
GOOGLE_GENAI_USE_VERTEXAI=TRUE
```

### Getting Your Configuration Values

1. **Project ID:** Find at https://console.cloud.google.com/home/dashboard
2. **Bucket Name:** Created during setup or create manually
3. **API Key:** Get from https://aistudio.google.com/app/apikey
4. **Resource ID:** Returned after successful deployment

## Quick Reference

**Resource ID Format:**
```
projects/YOUR_PROJECT_NUMBER/locations/LOCATION/reasoningEngines/YOUR_RESOURCE_ID
```

**Example Configuration:**
- **Project:** `YOUR_PROJECT_ID` (e.g., my-shl-project)
- **Location:** `us-central1` (or your preferred region)
- **Bucket:** `gs://YOUR_BUCKET_NAME` (e.g., my-agent-staging)
