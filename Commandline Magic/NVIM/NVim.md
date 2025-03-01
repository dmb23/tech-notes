# Getting started
>[!WARNING] Careful: Vim plugins (Mason) can install Python packages (Ruff) into your current environment
### Mac

- `brew install nvim ripgrep`
- install a [NerdFont](https://www.nerdfonts.com/#home)
	- set the font in the terminal
- install [kickstart](https://github.com/nvim-lua/kickstart.nvim)

# TODO
- [x] look into debugging
	- nvim-dap
	- nvim-dap-ui
	- nvim-dap-virtual-text
	- nvim-dap-python
- [x] look into oil.nvim
- [ ] undestand treesitter?
- [ ] understand buffers / windows
# Keymaps

- `gd` / `gr`go to definition / reference
	- `^T` go back
- `[d` / `]d` previous / next Diagnostic Mesage (error)
	- `<C-W>d` show diagnostic under cursor
- `K` show documentation
- Autocomplete:
	- `<C-n>` / `<C-p>` next / previous completion option
	- `<C-y>` select completion option
- `<Leader><Leader>` search buffers
- `<Leader>rn` rename symbol
- `<Leader>cs` document symbols (overview of all symbols in buffer)
- `<Leader>s` search ...
	- `h` help
	- `f` files (in workspace)
	- `n` Neovim files
	- `k` keymaps
	- `s` symbols (emojis, Icons)
- `<C-t>` Toggle
	- `t` terminal
	- `l` lazygit
- `<leader>d` debug things
	- `<leader>dm` debug method (Python)
# Plugins
- `lazy` plugin manager
- `which-key`
- `telescope` fuzzy finder
	- `:help telescope.builtin`
- `toggleterm`
	- use it with [[lazygit]] for nice git interface