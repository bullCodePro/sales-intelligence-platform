from fastapi.testclient import TestClient

from apps.api import main


def test_workspace_state_can_be_saved_and_loaded(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(main, "STATE_PATH", tmp_path / "workspace_state.json")
    client = TestClient(main.app)

    payload = {
        "clientName": "Client A",
        "workspaceName": "Market search",
        "targetCountry": "Brazil",
        "icpName": "Retail 200+",
        "minEmployees": 200,
        "maxEmployees": "",
        "targetSectors": "Retail",
        "positiveSignals": "Multiple locations",
        "targetRoles": "HR Manager",
        "companies": [
            {
                "name": "Example Retail",
                "sector": "Retail",
                "country": "Brazil",
                "employees": 300,
                "signals": "Multiple locations",
            }
        ],
        "filter": "all",
    }

    save_response = client.put("/api/workspace-state", json=payload)
    load_response = client.get("/api/workspace-state")

    assert save_response.status_code == 200
    assert save_response.json()["status"] == "saved"
    assert load_response.status_code == 200
    assert load_response.json()["clientName"] == "Client A"
    assert load_response.json()["companies"][0]["name"] == "Example Retail"
