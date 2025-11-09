"""Check deployment status"""
import vertexai
from vertexai import agent_engines

# Initialize
vertexai.init(
    project="shl-recommender-477516",
    location="us-central1",
    staging_bucket="gs://shl-agent-staging"
)

resource_id = "projects/868684576817/locations/us-central1/reasoningEngines/6294356623343222784"

try:
    remote_app = agent_engines.get(resource_id)
    print("✓ Deployment is ACTIVE!")
    print(f"Resource Name: {remote_app.resource_name}")
    print(f"\nYou can now create sessions and send queries.")
except Exception as e:
    if "not found" in str(e).lower():
        print("✗ Deployment not found - it may have failed during build.")
    elif "not ready" in str(e).lower() or "creating" in str(e).lower():
        print("⏳ Deployment is still building...")
        print("This can take 5-10 minutes. Check logs for progress.")
    else:
        print(f"Status check error: {e}")
