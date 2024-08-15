# uv
Apparently uv works now (even though the API may still change). Allows to manage python versions (like pyenv, just better), manage environments & requirements (like poetry)

>- `uv` does not depend on Python itself. Precompiled, standalone binaries  can be [easily installed](https://github.com/astral-sh/uv/blob/0.2.35/docs/getting-started/installation.md) on Linux, macOS and Windows.
>- `uv python` manages Python versions! No need to resort to OS-specific mechanisms, like `pyenv`, `deadsnakes`, or to heavyweight tools like `conda`.
>- `uv tool` manages tools in centralized environments! No more need for `pipx` or `fades`.
>- `uv init` creates a barebones `pyproject.toml` using `hatchling` as build backend and a working src-layout with an empty README and a dummy module.
    - If you need something more sophisticated, you could always use `copier` or `cookiecutter` with some more sophisticated template.
> - `uv add` adds dependencies to `pyproject.toml`, _creates a `venv` if one didn't exist_, and installs them!
> - `uv lock` creates a lock file with all your dependencies, which you can then use in `uv sync`.
    - And if you want a good old `requirements.txt`, `uv pip compile` does it for you, just like `pip-tools`!
> - `uv run` executes scripts and commands, again _without explicitly activating environments_!
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
