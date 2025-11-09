"""
Remote deployment script for SHL Assessment Recommendation System
Deploys the agent to Google Cloud Agent Engine
"""

import os
import sys

import vertexai
from absl import app, flags
from dotenv import load_dotenv
from vertexai import agent_engines
from vertexai.preview import reasoning_engines

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.shl_agent.agent import root_agent

FLAGS = flags.FLAGS
flags.DEFINE_string("project_id", None, "GCP project ID.")
flags.DEFINE_string("location", None, "GCP location.")
flags.DEFINE_string("bucket", None, "GCP bucket.")
flags.DEFINE_string("resource_id", None, "ReasoningEngine resource ID.")
flags.DEFINE_string("user_id", "test_user", "User ID for session operations.")
flags.DEFINE_string("session_id", None, "Session ID for operations.")
flags.DEFINE_bool("create", False, "Creates a new deployment.")
flags.DEFINE_bool("delete", False, "Deletes an existing deployment.")
flags.DEFINE_bool("list", False, "Lists all deployments.")
flags.DEFINE_bool("create_session", False, "Creates a new session.")
flags.DEFINE_bool("list_sessions", False, "Lists all sessions for a user.")
flags.DEFINE_bool("get_session", False, "Gets a specific session.")
flags.DEFINE_bool("send", False, "Sends a message to the deployed agent.")
flags.DEFINE_string(
    "message",
    "I need assessments for a Python developer with leadership skills",
    "Message to send to the agent.",
)
flags.mark_bool_flags_as_mutual_exclusive(
    [
        "create",
        "delete",
        "list",
        "create_session",
        "list_sessions",
        "get_session",
        "send",
    ]
)


def create() -> None:
    """Creates a new deployment."""
    print("Creating deployment...")
    
    # First wrap the agent in AdkApp
    app = reasoning_engines.AdkApp(
        agent=root_agent,
        enable_tracing=True,
    )

    # Now deploy to Agent Engine
    print("Deploying to Agent Engine...")
    remote_app = agent_engines.create(
        agent_engine=app,
        requirements=[
            "faiss-cpu==1.9.0.post1",
            "sentence-transformers==3.1.1",
            "numpy==1.26.4",  # Use specific version with pre-built wheels
        ],
        extra_packages=["./app/shl_agent", "./data"],
    )
    print(f"✓ Created remote app: {remote_app.resource_name}")
    print(f"\nSave this resource ID for future operations:")
    print(f"  {remote_app.resource_name}")


def delete(resource_id: str) -> None:
    """Deletes an existing deployment."""
    print(f"Deleting deployment: {resource_id}")
    remote_app = agent_engines.get(resource_id)
    remote_app.delete(force=True)
    print(f"✓ Deleted remote app: {resource_id}")


def list_deployments() -> None:
    """Lists all deployments."""
    print("Fetching deployments...")
    deployments = agent_engines.list()
    if not deployments:
        print("No deployments found.")
        return
    print("\nDeployments:")
    for deployment in deployments:
        print(f"  - {deployment.resource_name}")


def create_session(resource_id: str, user_id: str) -> None:
    """Creates a new session for the specified user."""
    print(f"Creating session for user: {user_id}")
    remote_app = agent_engines.get(resource_id)
    remote_session = remote_app.create_session(user_id=user_id)
    print("\n✓ Created session:")
    print(f"  Session ID: {remote_session['id']}")
    print(f"  User ID: {remote_session['user_id']}")
    print(f"  App name: {remote_session['app_name']}")
    print(f"  Last update time: {remote_session['last_update_time']}")
    print("\nUse this session ID with --session_id when sending messages.")


def list_sessions(resource_id: str, user_id: str) -> None:
    """Lists all sessions for the specified user."""
    print(f"Fetching sessions for user: {user_id}")
    remote_app = agent_engines.get(resource_id)
    sessions = remote_app.list_sessions(user_id=user_id)
    print(f"\nSessions for user '{user_id}':")
    if not sessions:
        print("  No sessions found.")
        return
    for session in sessions:
        print(f"  - Session ID: {session['id']}")


def get_session(resource_id: str, user_id: str, session_id: str) -> None:
    """Gets a specific session."""
    print(f"Fetching session: {session_id}")
    remote_app = agent_engines.get(resource_id)
    session = remote_app.get_session(user_id=user_id, session_id=session_id)
    print("\nSession details:")
    print(f"  ID: {session['id']}")
    print(f"  User ID: {session['user_id']}")
    print(f"  App name: {session['app_name']}")
    print(f"  Last update time: {session['last_update_time']}")


def send_message(resource_id: str, user_id: str, session_id: str, message: str) -> None:
    """Sends a message to the deployed agent."""
    remote_app = agent_engines.get(resource_id)

    print(f"\nSending message to session {session_id}:")
    print(f"Query: {message}")
    print(f"\n{'='*80}")
    print("Response:")
    print(f"{'='*80}\n")
    
    for event in remote_app.stream_query(
        user_id=user_id,
        session_id=session_id,
        message=message,
    ):
        print(event)


def main(argv=None):
    """Main function that can be called directly or through app.run()."""
    # Parse flags first
    if argv is None:
        argv = flags.FLAGS(sys.argv)
    else:
        argv = flags.FLAGS(argv)

    load_dotenv()

    # Now we can safely access the flags
    project_id = (
        FLAGS.project_id if FLAGS.project_id else os.getenv("GOOGLE_CLOUD_PROJECT")
    )
    location = FLAGS.location if FLAGS.location else os.getenv("GOOGLE_CLOUD_LOCATION")
    bucket = FLAGS.bucket if FLAGS.bucket else os.getenv("GOOGLE_CLOUD_STAGING_BUCKET")
    user_id = FLAGS.user_id

    if not project_id:
        print("ERROR: Missing required environment variable: GOOGLE_CLOUD_PROJECT")
        return
    elif not location:
        print("ERROR: Missing required environment variable: GOOGLE_CLOUD_LOCATION")
        return
    elif not bucket:
        print("ERROR: Missing required environment variable: GOOGLE_CLOUD_STAGING_BUCKET")
        return

    print(f"\nInitializing Vertex AI:")
    print(f"  Project: {project_id}")
    print(f"  Location: {location}")
    print(f"  Staging Bucket: {bucket}\n")

    vertexai.init(
        project=project_id,
        location=location,
        staging_bucket=bucket,
    )

    if FLAGS.create:
        create()
    elif FLAGS.delete:
        if not FLAGS.resource_id:
            print("ERROR: resource_id is required for delete")
            return
        delete(FLAGS.resource_id)
    elif FLAGS.list:
        list_deployments()
    elif FLAGS.create_session:
        if not FLAGS.resource_id:
            print("ERROR: resource_id is required for create_session")
            return
        create_session(FLAGS.resource_id, user_id)
    elif FLAGS.list_sessions:
        if not FLAGS.resource_id:
            print("ERROR: resource_id is required for list_sessions")
            return
        list_sessions(FLAGS.resource_id, user_id)
    elif FLAGS.get_session:
        if not FLAGS.resource_id:
            print("ERROR: resource_id is required for get_session")
            return
        if not FLAGS.session_id:
            print("ERROR: session_id is required for get_session")
            return
        get_session(FLAGS.resource_id, user_id, FLAGS.session_id)
    elif FLAGS.send:
        if not FLAGS.resource_id:
            print("ERROR: resource_id is required for send")
            return
        if not FLAGS.session_id:
            print("ERROR: session_id is required for send")
            return
        send_message(FLAGS.resource_id, user_id, FLAGS.session_id, FLAGS.message)
    else:
        print(
            "Please specify one of: --create, --delete, --list, --create_session, --list_sessions, --get_session, or --send"
        )


if __name__ == "__main__":
    app.run(main)
