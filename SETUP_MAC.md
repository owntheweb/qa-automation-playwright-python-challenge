## Mac Setup

### Create a Virtual Environment With pyenv

Install Homebrew following instructions [here](https://brew.sh/) if not already installed.

Install pyenv for Mac. ([reference](https://ericsysmin.com/2024/02/05/how-to-install-pyenv-on-macos))

```
brew update
brew install ncurses
brew install pyenv
```

Add config to .zshrc

```
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
source ~/.zshrc
```

Or .bashrc

```
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc
```
