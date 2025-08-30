# create_workspace.py

from azure.ai.ml import MLClient
from azure.ai.ml.entities import Workspace
from azure.identity import DefaultAzureCredential
import config


def get_ml_client():
    """Authenticate and return MLClient."""
    credential = DefaultAzureCredential()
    return MLClient(
        credential=credential,
        subscription_id=config.SUBSCRIPTION_ID,
        resource_group_name=config.RESOURCE_GROUP
    )


def get_or_create_workspace():
    """Check if workspace exists; create if not."""
    ml_client = get_ml_client()
    try:
        ws = ml_client.workspaces.get(config.WORKSPACE_NAME)
        print(f"Workspace '{ws.name}' already exists in resource group '{ws.resource_group}'.")
        return ws
    except Exception:
        print(f"Workspace '{config.WORKSPACE_NAME}' not found. Creating new one...")

        ws = Workspace(
            name=config.WORKSPACE_NAME,
            location=config.LOCATION,
            description="ML workspace for MLOps experiments",
            friendly_name="MLOpsDukeWorkspace"
        )

        ws = ml_client.workspaces.begin_create(ws).result()
        print(f"Workspace '{ws.name}' created in resource group '{ws.resource_group}'.")
        return ws


def delete_workspace():
    """Delete the workspace when done working."""
    ml_client = get_ml_client()
    print(f"Deleting workspace '{config.WORKSPACE_NAME}'...")
    ml_client.workspaces.begin_delete(config.WORKSPACE_NAME).result()
    print("Workspace deleted.")


if __name__ == "__main__":
    ws = get_or_create_workspace()
    # Do your work here with the workspace
    delete_workspace()
