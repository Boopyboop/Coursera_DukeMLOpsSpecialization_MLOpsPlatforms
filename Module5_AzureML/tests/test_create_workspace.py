import pytest
import create_workspace


def test_get_or_create_workspace_existing(mocker):
    """Test that existing workspace is returned without creating a new one."""
    mock_client = mocker.Mock()
    mock_ws = mocker.Mock()
    mock_ws.name = "test-ws"
    mock_ws.resource_group = "test-rg"

    # Mock MLClient and get()
    mock_client.workspaces.get.return_value = mock_ws
    mocker.patch("create_workspace.get_ml_client", return_value=mock_client)

    ws = create_workspace.get_or_create_workspace()

    assert ws.name == "test-ws"
    mock_client.workspaces.get.assert_called_once_with("mlops-duke-workspace")


def test_get_or_create_workspace_new(mocker):
    """Test that a new workspace is created if not found."""
    mock_client = mocker.Mock()
    mock_ws = mocker.Mock()
    mock_ws.name = "new-ws"
    mock_ws.resource_group = "test-rg"

    # Simulate get() raising exception (workspace not found)
    mock_client.workspaces.get.side_effect = Exception("Not found")
    mock_client.workspaces.begin_create.return_value.result.return_value = mock_ws

    mocker.patch("create_workspace.get_ml_client", return_value=mock_client)

    ws = create_workspace.get_or_create_workspace()

    assert ws.name == "new-ws"
    mock_client.workspaces.begin_create.assert_called_once()


def test_delete_workspace(mocker):
    """Test that delete_workspace calls begin_delete()."""
    mock_client = mocker.Mock()
    mocker.patch("create_workspace.get_ml_client", return_value=mock_client)

    create_workspace.delete_workspace()

    mock_client.workspaces.begin_delete.assert_called_once_with("mlops-duke-workspace")
