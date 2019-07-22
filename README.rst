vim2vsc
========

This tool is meant to convert your custom vim bindings from your .vimrc into 
VSCode compatible bindings. At the time this tool was created, .vimrc is not
officially supported by the VScodeVim extension (the most popular vim emulator
for VSCode) and there are no known tool that automate the process formatting vim 
bindings for vscode-vim.

Link to VSCodeVim: `<https://github.com/VSCodeVim/Vim/>`

Features
--------

- Formats bindings for Normal Mode, Insert Mode and Visual Mode

- Auto-enables popular vim extensions like airline and vim-easymotion by activating vscode ports. **Planned**

- Sets flags like ``:set hlsearch`` and ``set :inclsearch``. **Planned**

Requirements
------------
- Python 3.6+

Installation
------------

You can get vim2vsc by running:

    git clone https://github.com/devanshuDesai/vim2vsc

Usage
-----------

    cd vim2vsc
    python3 convert.py

``convert.py`` accepts three flags:
- ``--vimrc`` Specify the path to your ``.vimrc`` installation (guesses 
path based on system if you don't provide one).
- ``--settings`` Specify the path to your ``settings.json`` for your VSCode Installation(guesses 
path based on system if you don't provide one).
- ``--nobackup`` If this flag is set, vscode-vim doesn't save your old ``package.json``
before modifying it.

Examples
----------

    python3 convert.py --settings ~/downloads/settings.json --nobackup

Equivalently,

    python3 convert.py --s ~/downloads/settings.json --b

Contribute
----------

- Issue Tracker: github.com/$devanshuDesai/vim2vsc/issues
- Source Code: github.com/devanshuDesai/vim2vsc


License
-------

    The project is licensed under the MIT license.
