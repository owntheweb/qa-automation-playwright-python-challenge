# QA Automation Playwright Python

## Coding Challenge Requirements

-   Use Playwright for the project.
-   Use Python for the project.
-   Write tests for https://www.saucedemo.com
-   Work out a way to make logins fluid/reusable when testing features on and/or after the login page.
-   Lead the path on what should be tested and how it should be tested.
-   There's not a requirement to write tests for all features. The goal is to show the team how you can adapt and create. We'll be checking for best practices generally and how you think when working through new Playwright tests.
-   Have fun! 🎉

## OS Setup

See:

-   [Windows Setup](SETUP_WINDOWS.md)
-   [Mac Setup](SETUP_MAC.md)
-   [Linux Setup](SETUP_LINUX.md)

## Configure pyenv

Confirm pyenv is installed.

```
pyenv --version
```

Install Python version 3.11. The version doesn't matter too much in this demo, yet an agreement on which version to use may help in team troubleshooting later.

```
pyenv install 3.11
```

Activate Python environment with selected version.

```
pyenv local 3.11
```

Confirm the active Python version.

```
python --version
```

## Configure VS Code

Open the Playwright project by choosing `File` -> `Open Folder...`, and select the Playwright project folder.

Configure VS Code to make use of the correct Python interpreter created by pyenv. Start by opening a project Python file. In the bottom bar, right-ish side, a python version will be visible. Click it and select the installed pyenv version being used in the project.

Optionally open a new terminal window in VS Code with `Ctrl+J` or by choosing `Terminal` -> `New Terminal` in the top menu. Ensure Command Prompt or PowerShell is active. If it's defaulting to WSL or some other terminal, a new one can be created in the terminal panel by choosing the down (`v`) icon next to the `+` (new terminal) in the right-side panel in the terminal panel where PowerShell or `Command Prompt` can be chosen.

## Install Playwright

With Python and build tools installed, install the Playwright project dependencies:

```
pip install -r requirements.txt
```

Install Playwright Python browser binaries chromium, FireFox and WebKit (Safari's engine). Note: If Chrome and Edge are installed to the computer, these can also be run later.

```
playwright install
```

## Setup .env File

Copy the .env.example to .env that will get read by Playwright tests.

On Windows:

```
copy .env.example .env
```

On Mac/Linux:

```
cp .env.example .env
```

Configure the environment variables in .env. See notes and examples in the file.

Be sure to update the .env file

```
UI_USERNAME="username here"
UI_PASSWORD="password here"
UI_BASE_URL="https://www.saucedemo.com/"
```

## How To Run Tests

Run all tests, verbose:

```
pytest -v
```

Run all tests, verbose, show console output/print statements:

```
pytest -v -s
```

Run tests with HTML report. Note: Tests are currently set to output this and a CTRF JSON report automatically by default.

```
pytest -v -s --html=pwreport1.html --self-contained-html
```

Run in headed mode to see what Playwright is doing when running tests:

```
pytest --headed
```

Slowdown headed mode to be able to follow tests as a human a bit better, in this example a one second pause between each step:

```
pytest --headed --slowmo 1000
```

Run a single test file.

```
pytest tests/some_test.py
```

Run a set of test files.

```
pytest tests/some_test.py tests/another_set_of_tests.py
```

Run all tests in multiple browsers.

```
pytest -v --browser chromium --browser firefox --browser webkit
```

Run tests on localy installed Edge and Chromium (can run headless or --headed)

```
pytest -v --browser-channel=msedge && \
pytest -v --browser-channel=chrome
```

Run in headed debug mode (stops on errors).

```
pytest -v --headed --pdb
```

Enable stepped debugging to see all steps in the headed session. In .env:

```
PWDEBUG=1
```

Then run:

```
pytest --headed
```

New debug controls will become available in a window in addition to the browser window.

## Generate Code

While not a full solution for creating tests, this can help with gathering locators and general order of operations for tests. Once started, use the website and steps and locators will be identified and listed which can be copied and brought into tests.

```
playwright codegen --ignore-https-errors https://www.saucedemo.com/
```

## How To Update Playwright

```
pip install --upgrade playwright
playwright install
```

## Best Practices

-   [Playwright Python Best Practices](https://playwright.dev/python/docs/best-practices)
-   Check out Ruff for keeping files clean.
-   Use pytest fixtures for setup and teardown
-   Utilize page object models for better test organization

For more help, consult the [Playwright Python documentation](https://playwright.dev/python/docs/intro) or open an issue in the project repository.
