from test_prioritizer import TestPrioritizer

tp = TestPrioritizer()

# Tests to run example
tests_to_run = ["test_login", "test_checkout", "test_new_feature", "test_profile_update"]

# Prioritize them
ordered_tests = tp.prioritize_tests(tests_to_run)

print("Recommended execution order", ordered_tests)

# Simulate updating  history after a run
tp.update_history("test_new_feature", "pass")
tp.update_history("test_checkout", "fail")
tp.update_history("test_login", "fail")
