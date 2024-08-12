# Getting started
Careful: Vim plugins (Mason) can install Python packages (Ruff) into your current environment
### Mac
- `brew install nvim ripgrep`
- install a [NerdFont](https://www.nerdfonts.com/#home)
	- set the font in the terminal
- install [kickstart](https://github.com/nvim-lua/kickstart.nvim)

# TODO
- [ ] look into debugging
	- nvim-dap
	- nvim-dap-ui
	- nvim-dap-virtual-text
	- nvim-dap-python
- [ ] look into oil.nvim
- [ ] undestand treesitter?
- [ ] understand buffers / windows
# Keymaps

- `:e $MYVIMRC`
- `<leader>s` search
	- `<leader>sh` search help
	- `<leader>sk` search keymaps
	- ...
- `gd` / `gr`go to definition / reference
	- `^T` go back
- `[d` / `]d` previous / next Diagnostic Mesage (error)
	- `<C-W>d` show diagnostic under cursor
- `K` show documentation
- Autocomplete:
	- `<C-n>` / `<C-p>` next / previous completion option
	- `<C-y>` select completion option

# Plugins
- `lazy` plugin manager
- `which-key`
- `telescope` fuzzy finder
	- `:help telescope.builtin`