import pytest

def pytest_runtest_makereport(item, call):
    """
    Hook to detect test failures and mark them for healing.
    """
    if call.when == "call" and call.excinfo is not None:
        if "healing" in item.keywords:
            print(f"\n Healing mode active for test: {item.name}")