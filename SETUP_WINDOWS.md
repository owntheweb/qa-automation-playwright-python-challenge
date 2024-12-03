## Windows Setup

On Windows, it's recommended to use Python directly rather than through WSL for Playwright tests. This allows for easier UI mode testing if needed.

### Install Python

Download the latest Windows installer at:
https://www.python.org/downloads/windows/

### Create a Virtual Environment With pyenv

Install pyenv for Windows.

Follow instructions at:
https://pyenv-win.github.io/pyenv-win/

Short version: Run this in PowerShell:

```
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
```

Completely close terminal. Then in new Command Prompt or PowerShell:

```
pyenv -v
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

### Install Microsoft Visual C++ Build Tools

Some Python packages, including Playwright, require Microsoft Visual C++ 14.0 or greater. To install it:

-   Visit https://visualstudio.microsoft.com/downloads/
-   Download the community free downloads
-   Run the app and select Workloads -> Desktop development with C++
    -   Note: A guru may be able to remove extra packages in Individual Components and update this README, yet this will work for now.
-   Go get a snack while 50GB of dependencies download and install.
