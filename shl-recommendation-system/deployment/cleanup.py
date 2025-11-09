"""
Cleanup script for SHL Assessment Recommendation System deployments
"""

import os
import sys

import vertexai
from dotenv import load_dotenv
from vertexai import agent_engines


def cleanup_deployment():
    """Clean up all deployments."""
    load_dotenv()

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION")
    bucket = os.getenv("GOOGLE_CLOUD_STAGING_BUCKET")

    if not project_id or not location or not bucket:
        print("ERROR: Missing required environment variables")
        print("Please set GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION, and GOOGLE_CLOUD_STAGING_BUCKET")
        sys.exit(1)

    print(f"Initializing Vertex AI:")
    print(f"  Project: {project_id}")
    print(f"  Location: {location}\n")

    vertexai.init(
        project=project_id,
        location=location,
        staging_bucket=bucket,
    )

    print("Fetching all deployments...")
    deployments = agent_engines.list()
    
    if not deployments:
        print("No deployments found to clean up.")
        return

    print(f"\nFound {len(deployments)} deployment(s):")
    for i, deployment in enumerate(deployments, 1):
        print(f"  {i}. {deployment.resource_name}")

    confirm = input("\nDo you want to delete ALL deployments? (yes/no): ")
    
    if confirm.lower() not in ['yes', 'y']:
        print("Cleanup cancelled.")
        return

    print("\nDeleting deployments...")
    for deployment in deployments:
        try:
            print(f"  Deleting {deployment.resource_name}...", end=" ")
            remote_app = agent_engines.get(deployment.resource_name)
            remote_app.delete(force=True)
            print("✓")
        except Exception as e:
            print(f"✗ Error: {e}")

    print("\n✓ Cleanup completed!")


if __name__ == "__main__":
    cleanup_deployment()
