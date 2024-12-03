import json
import os
import time
import platform
import subprocess
import pytest
from typing import Optional

class CTRFReporter:
    def __init__(self):
        self.report_data = {
            "results": {
                "tool": {
                    "name": "playwright-python",
                    "version": pytest.__version__,
                },
                "summary": {
                    "tests": 0,
                    "passed": 0,
                    "failed": 0,
                    "skipped": 0,
                    "pending": 0,
                    "other": 0,
                    "start": int(time.time()),
                    "stop": 0
                },
                "environment": {
                    "osPlatform": platform.system(),
                    "osRelease": platform.release(),
                    "osVersion": platform.version(),
                    "testEnvironment": os.getenv("TEST_ENV", "test"),
                    "extra": {
                        "pythonVersion": platform.python_version(),
                        "pythonImplementation": platform.python_implementation(),
                    }
                },
                "tests": []
            }
        }

        # Try to get pyenv version if available
        try:
            pyenv_version = subprocess.check_output(
                ["pyenv", "version"], 
                stderr=subprocess.STDOUT
            ).decode().strip()
            # pyenv output includes version name and (set by path), we just want version
            pyenv_version = pyenv_version.split(" ")[0]
            self.report_data["results"]["environment"]["extra"]["pyenvVersion"] = pyenv_version
        except (subprocess.CalledProcessError, FileNotFoundError):
            # pyenv not available or not in use
            pass

        self.test_markers = {}  # Store markers keyed by test ID
        self.test_start_times = {}  # Store test start times

    # Rest of the class implementation remains the same...
    def pytest_collection_modifyitems(self, items):
        """Capture markers during test collection"""
        for item in items:
            markers = [marker.name for marker in item.iter_markers()]
            self.test_markers[item.nodeid] = markers

    def pytest_runtest_logstart(self, nodeid, location):
        """Called at the start of running a test"""
        self.test_start_times[nodeid] = int(time.time() * 1000)  # milliseconds

    def pytest_sessionfinish(self, session):
        """Called after test session finishes"""
        self.report_data["results"]["summary"]["stop"] = int(time.time())
        
        # Write report to file
        output_file = "ctrf-report.json"
        with open(output_file, "w") as f:
            json.dump(self.report_data, f, indent=2)

    def pytest_runtest_logreport(self, report):
        """Called for each test report phase (setup, call, teardown)"""
        # Only process when test is complete (teardown) or skipped (setup)
        if report.when == "teardown" or (report.when == "setup" and report.skipped):
            # Update summary counts
            if report.when == "teardown":
                self.report_data["results"]["summary"]["tests"] += 1
                if report.passed:
                    self.report_data["results"]["summary"]["passed"] += 1
                elif report.failed:
                    self.report_data["results"]["summary"]["failed"] += 1
            elif report.skipped:
                self.report_data["results"]["summary"]["skipped"] += 1

            # Calculate timing in milliseconds
            start_time = self.test_start_times.get(report.nodeid, 0)
            stop_time = int(time.time() * 1000)
            duration = stop_time - start_time

            # Get test path components
            path_parts = report.nodeid.split("::")
            file_path = path_parts[0]
            suite = path_parts[1] if len(path_parts) > 1 else None

            # Extract browser info if available
            browser = None
            if "[" in report.nodeid and "]" in report.nodeid:
                browser = report.nodeid.split("[")[-1].rstrip("]")

            # Build test entry
            test_data = {
                "name": path_parts[-1],
                "status": "skipped" if report.skipped else "failed" if report.failed else "passed",
                "duration": duration,
                "start": start_time,
                "stop": stop_time,
                "suite": suite,
                "tags": self.test_markers.get(report.nodeid, []),
                "type": "e2e",
                "filePath": file_path,
                "browser": browser
            }

            # Add error information if test failed
            if report.failed:
                test_data.update({
                    "message": str(report.longrepr),
                    "trace": self._format_traceback(report.longrepr) if hasattr(report, 'longrepr') else None
                })

            self.report_data["results"]["tests"].append(test_data)

    def _format_traceback(self, longrepr) -> Optional[str]:
        """Format traceback information if available"""
        if hasattr(longrepr, 'reprtraceback'):
            return str(longrepr.reprtraceback)
        return str(longrepr) if longrepr else None

def pytest_configure(config):
    """Register CTRF reporter plugin"""
    ctrf_reporter = CTRFReporter()
    config.pluginmanager.register(ctrf_reporter)