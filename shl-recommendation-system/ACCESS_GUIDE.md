# How to Access Your SHL Recommendation System

## Your Deployment Information

**Resource ID:**
```
projects/868684576817/locations/us-central1/reasoningEngines/4371319582456020992
```

**Project:** shl-recommender-477516  
**Location:** us-central1  
**Status:** Deploying (check logs below)

## Monitor Deployment Progress

**View Logs:**
https://console.cloud.google.com/logs/query?project=shl-recommender-477516

**View in Console:**
https://console.cloud.google.com/vertex-ai/reasoning-engines?project=shl-recommender-477516

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
  --resource_id=projects/868684576817/locations/us-central1/reasoningEngines/4371319582456020992
```

**Save the session ID** from the output!

### Step 3: Send Your First Query
```bash
poetry run python deployment/remote.py --send \
  --resource_id=projects/868684576817/locations/us-central1/reasoningEngines/4371319582456020992 \
  --session_id=YOUR_SESSION_ID \
  --message="I need a Python developer with leadership skills"
```

## Example Queries to Try

### 1. Technical + Behavioral
```bash
poetry run python deployment/remote.py --send \
  --resource_id=projects/868684576817/locations/us-central1/reasoningEngines/4371319582456020992 \
  --session_id=YOUR_SESSION_ID \
  --message="Java developer who can collaborate with business teams"
```

### 2. Pure Technical
```bash
poetry run python deployment/remote.py --send \
  --resource_id=projects/868684576817/locations/us-central1/reasoningEngines/4371319582456020992 \
  --session_id=YOUR_SESSION_ID \
  --message="Python, SQL and JavaScript proficiency"
```

### 3. Sales Role
```bash
poetry run python deployment/remote.py --send \
  --resource_id=projects/868684576817/locations/us-central1/reasoningEngines/4371319582456020992 \
  --session_id=YOUR_SESSION_ID \
  --message="Sales representative with strong communication"
```

### 4. Leadership Assessment
```bash
poetry run python deployment/remote.py --send \
  --resource_id=projects/868684576817/locations/us-central1/reasoningEngines/4371319582456020992 \
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
  --resource_id=projects/868684576817/locations/us-central1/reasoningEngines/4371319582456020992
```

### Get Session Details
```bash
poetry run python deployment/remote.py --get_session \
  --resource_id=projects/868684576817/locations/us-central1/reasoningEngines/4371319582456020992 \
  --session_id=YOUR_SESSION_ID
```

### Delete Deployment (when done)
```bash
poetry run python deployment/remote.py --delete \
  --resource_id=projects/868684576817/locations/us-central1/reasoningEngines/4371319582456020992
```

## Check Deployment Status

Run this command to check if deployment is complete:
```bash
gcloud ai reasoning-engines describe 4371319582456020992 \
  --region=us-central1 \
  --project=shl-recommender-477516
```

Look for `state: ACTIVE` in the output.

## Alternative: Using Python Script

Create a file `check_deployment.py`:
```python
import vertexai
from vertexai import agent_engines

vertexai.init(
    project="shl-recommender-477516",
    location="us-central1",
    staging_bucket="gs://shl-agent-staging"
)

resource_id = "projects/868684576817/locations/us-central1/reasoningEngines/4371319582456020992"

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

1. Go to: https://console.cloud.google.com/vertex-ai/reasoning-engines?project=shl-recommender-477516
2. Find your agent: `4371319582456020992`
3. Click to view details and test directly in the console

## Integration into Your Application

Once deployed, you can integrate it into your FastAPI app:

```python
from vertexai import agent_engines
import vertexai

# Initialize
vertexai.init(
    project="shl-recommender-477516",
    location="us-central1",
    staging_bucket="gs://shl-agent-staging"
)

# Get the deployed agent
resource_id = "projects/868684576817/locations/us-central1/reasoningEngines/4371319582456020992"
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
- **Console:** https://console.cloud.google.com/billing?project=shl-recommender-477516
- **Agent Engine:** Charged per session
- **Gemini API:** Charged per token

## Support

If you encounter issues:
1. Check logs: https://console.cloud.google.com/logs/query?project=shl-recommender-477516
2. Verify deployment status in console
3. Ensure credentials are valid: `gcloud auth application-default login`

## Quick Reference

**Resource ID (save this!):**
```
projects/868684576817/locations/us-central1/reasoningEngines/4371319582456020992
```

**Project:** `shl-recommender-477516`  
**Location:** `us-central1`  
**Bucket:** `gs://shl-agent-staging`
