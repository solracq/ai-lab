import json
from datetime import datetime

class TestPrioritizer:
    def __init__(self, history_file="test_history.json"):
        self.history_file = history_file
        self.history = self.load_history()

    def load_history(self):
        """
        Loads test result history from file
        :return: json file
        """
        try:
            with open(self.history_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def update_history(self, test_name, status):
        """
        Records test results (PASS/FAIL) with timestamp into the history file.
        :param test_name: Name of the test
        :param status: PASS/FAIL status
        """
        record = {
            "last_run": datetime.now().isoformat(),
            "status": status
        }
        self.history[test_name] = record
        with open(self.history_file, "w") as file:
            json.dump(self.history, file, indent=2)

    def prioritize_tests(self, test_list):
        """
        Returns a list of tests stored by priority:
        1. Failed last time
        2. Never run before
        3. Passed last time
        :param test_list:
        :return: list of tests sorted in high priority order
        """
        def score(test):
            record = self.history.get(test)
            if not record:
                return 2  # new test = medium priority
            elif record["status"] == "fail":
                return 3  # high priority
            else:
                return 1  # low priority
        return sorted(test_list, key=score, reverse=True)
