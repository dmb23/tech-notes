# Conda

> [!WARNING] Mac ARM systems
>
> `conda` is still best to provide Python versions for Mac ARM architectures. 
> 
> Current setup: use conda to manage Python versions and then setup Poetry environments for the package management.
 
# pyenv

- allows to easily set project-specific versions
- by default installs (builds) each python version

> [!WARNING] Mac ARM systems
> I had some problems getting pyenv installations mapping to the correct platform... I went back to Conda.

### register an existing python version

> If you have an existing Python installation under `<prefix>`, you can symlink `$(pyenv root)/versions/<arbitrary name>` to that `<prefix>`. Pyenv would see and handle this `<arbitrary name>` like any other version entry.


> [!NOTE] For homebrew-installed versions:
> Homebrew does only provide all executables (notably pip) when you create a new virtual environment!
> E.g. `$(brew --prefix)/opt/python@3.12/bin/python3.12 -m venv $(pyenv root)/versions/brew@3.12`
