import os
import pytest
from dotenv import load_dotenv
from global_setup_teardown import global_setup, global_teardown
from playwright.sync_api import Page
from ctrf_reporter import CTRFReporter
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Explicitly set PWDEBUG if it's in .env
if os.getenv('PWDEBUG'):
    os.environ['PWDEBUG'] = os.getenv('PWDEBUG')
    print(f"Debug mode enabled: PWDEBUG={os.getenv('PWDEBUG')}")

def pytest_configure(config):
    
    config.addinivalue_line("markers", "smoke: mark test as smoke test")

    # Register CTRF reporter
    ctrf_reporter = CTRFReporter()
    config.pluginmanager.register(ctrf_reporter)

@pytest.fixture(scope="session")
def html_report_path():
    """Generate a unique filename for the HTML report"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"test-report_{timestamp}.html"

def pytest_html_report_title(report):
    """Set the title of the HTML report"""
    report.title = "Playwright Test Report"

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Add extra HTML report details including browser and timing information"""
    outcome = yield
    report = outcome.get_result()
    
    # Add browser information to the report if available
    browser = item.config.option.browser if hasattr(item.config.option, 'browser') else None
    setattr(report, "browser", browser)
    
    # Add timestamp to the report
    setattr(report, "timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    # If it's a failed test and has a page fixture, capture a screenshot
    if report.when == "call" and report.failed:
        try:
            page = item.funcargs.get("page")
            if page:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = f"screenshot_{item.name}_{timestamp}.png"
                page.screenshot(path=screenshot_path)
                # Add screenshot to the HTML report
                if hasattr(item.config, "_html"):
                    html = item.config._html
                    html.append(html.html_screenshot(screenshot_path))
        except Exception as e:
            print(f"Failed to capture screenshot: {str(e)}")

@pytest.fixture(scope="session", autouse=True)
def setup_teardown():
    global_setup()
    yield
    global_teardown()

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "ignore_https_errors": bool(os.getenv("IGNORE_HTTP_ERRORS", False))
    }

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args, pytestconfig):
    """Fixture to configure browser launch arguments"""
    return {
        **browser_type_launch_args,
        "timeout": 120000,
        "headless": not pytestconfig.getoption("--headed")
    }
