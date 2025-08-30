# create_workspace.py

from azure.ai.ml import MLClient
from azure.ai.ml.entities import Workspace
from azure.identity import DefaultAzureCredential
import config

def create_workspace():
    """Creates or connects to an Azure ML Workspace."""
    # Authenticate (uses az login, managed identity, or env vars)
    credential = DefaultAzureCredential()

    ml_client = MLClient(
        credential=credential,
        subscription_id=config.SUBSCRIPTION_ID,
        resource_group_name=config.RESOURCE_GROUP
    )

    # Define workspace
    ws = Workspace(
        name=config.WORKSPACE_NAME,
        location=config.LOCATION,
        description="ML workspace for MLOps experiments",
        friendly_name="MLOpsDukeWorkspace"
    )

    # Create or update workspace
    ws = ml_client.workspaces.begin_create(ws).result()
    print(f"Workspace '{ws.name}' created in resource group '{ws.resource_group}'.")

if __name__ == "__main__":
    create_workspace()
