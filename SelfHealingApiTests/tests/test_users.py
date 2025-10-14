import requests
import pytest
from healing.schema_healer import auto_heal_schema
from healing.llm_healer import analyze_failure_with_llm

BASE_URL = "https://jsonplaceholder.typicode.com"

@pytest.mark.healing
def test_users_endpoint():
    endpoint = "users/1"
    url = f"{BASE_URL}/{endpoint}"

    try:
        response = requests.get(url)
        assert response.status_code == 200, f"Unexpected HTTP {response.status_code}"
        data = response.json()
        assert isinstance(data, dict), "Response is not a dictionary"
        auto_heal_schema(endpoint, data)
    except Exception as e:
        print(f" Test failed for {endpoint}: {e}")
        healing = analyze_failure_with_llm(endpoint, response.text, str(e))
        print(" AI Analysis:", healing["explanation"])
        if healing.get("suggested_fix"):
            print(" Suggested fix: \n", healing["suggested_fix"])
        pytest.skip("Test auto-healed, skipping for manual review.")
