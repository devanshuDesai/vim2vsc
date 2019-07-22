# -*- coding: utf-8 -*-
__version__ = "0.1.0"

# TODO: Add ability to set nohlsearch, incsearch etc
# TODO: Add integration for plugins like vim-airline

import platform
import argparse
import json
import re
import sys
import os

HOME_PATH = ""

# For UNIX based systems
try:
    HOME_PATH = os.environ['HOME']
except:
    pass

# For Windows based systems
try:
    HOME_PATH = os.environ['APPDATA']
except:
    pass

# Everything in this segment is to handle for different
# paths to settings.json and .vimrc in different systems
WINDOWS_PATH = HOME_PATH + r"\Code\User\settings.json"
MAC_PATH = "%s/Library/Application Support/Code/User/settings.json" % HOME_PATH
LINUX_PATH = "%s/.config/Code/User/settings.json" % HOME_PATH

vsc_paths = {"Windows": WINDOWS_PATH,
             "Darwin": MAC_PATH,
             "Linux": LINUX_PATH}

UNIX_VIM_PATH = "%s/.vimrc" % HOME_PATH
WINDOWS_VIM_PATH = "%s/_vimrc" % HOME_PATH

vim_paths = {"Windows": WINDOWS_VIM_PATH,
             "Darwin": UNIX_VIM_PATH,
             "Linux": UNIX_VIM_PATH}

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--vimrc", help="path to vimrc that needs to be converted")
parser.add_argument("-s", "--settings", help="path to settings.json for your VSCode")
parser.add_argument("-n", "--nobackup", help="doesn't save your old settings as old_settings.json if flag is set", action="store_false")
args = parser.parse_args()

current_platform = platform.system()
vsc_path = args.settings
vim_path = args.vimrc

# Uses settings.json path specified by user since vim2vsc doesn't recognize the platform
if vsc_path is None:
    vsc_path = vsc_paths.get(current_platform)
    if vsc_path is None:
        sys.exit("Please specify a path to settings.json for your VSCode")

# Uses .vimrc path specified by user since vim2vsc doesn't recognize the platform
if vim_path is None:
    vim_path = vim_paths.get(current_platform)
    if vim_path is None:
        sys.exit("Please specify a path to .vimrc in your system")
# Loading contents of settings.json
try:
    with open(vsc_path) as file:
        vscode = json.load(file)
except FileNotFoundError:
    sys.exit("Please specify a correct path to your settings.json")

# Loading contents of .vimrc
try:
    vimrc = ''.join(open(vim_path).readlines())
except FileNotFoundError:
    sys.exit("Please specify a correct path to your .vimrc")

def get_dict(bindings):
    bindings_list = []
    for binding in bindings:
        before, after = None, None
        binding_dict = {}
        try:
            before, after = re.findall(r'(.*?)\s(.*)', binding)[0]
        except:
            print("Failed to bind {%s}. Please check its formatting." % binding)
            continue
        binding_dict['before'] = list(before)
        # Special case for commands
        if after[0] == ':':
            binding_dict['commands'] = [after.replace('<Enter>', '').replace('<CR>', '')]
        else:
            binding_dict['after'] = list(after)
        bindings_list.append(binding_dict)
    return bindings_list

def main():
    # Initializing vim keys in settings.json
    vscode['vim.insertModeKeyBindings'] = []
    vscode['vim.normalModeKeyBindings'] = []
    vscode['vim.visualModeKeyBindings'] = []
    vscode['vim.insertModeKeyBindingsNonRecursive'] = []
    vscode['vim.normalModeKeyBindingsNonRecursive'] = []
    vscode['vim.visualModeKeyBindingsNonRecursive'] = []

    # Normal, Visual, Operator-Pending Bindings
    bindings = get_dict(re.findall(r'map (.*)', vimrc))
    vscode['vim.normalModeKeyBindings'] += bindings
    vscode['vim.visualModeKeyBindings'] += bindings

    # Normal, Visual, Operator-Pending Non-Recursive Bindings
    bindings = get_dict(re.findall(r'noremap (.*)', vimrc))
    vscode['vim.normalModeKeyBindingsNonRecursive'] += bindings
    vscode['vim.visualModeKeyBindingsNonRecursive'] += bindings

    # Normal Mode Recursive Bindings
    bindings = get_dict(re.findall(r'nmap (.*)', vimrc))
    vscode['vim.normalModeKeyBindings'] += bindings

    # Normal Mode Non-Recursive Bindings
    bindings = get_dict(re.findall(r'nnoremap (.*)', vimrc))
    vscode['vim.normalModeKeyBindingsNonRecursive'] += bindings

    # Insert Mode Recursive Bindings
    bindings = get_dict(re.findall(r'imap (.*)', vimrc))
    vscode['vim.insertModeKeyBindings'] += bindings

    # Insert Mode Non-Recursive Bindings
    bindings = get_dict(re.findall(r'inoremap (.*)', vimrc))
    vscode['vim.insertModeKeyBindingsNonRecursive'] += bindings

    # Visual Mode Recursive Bindings
    bindings = get_dict(re.findall(r'vmap (.*)', vimrc))
    vscode['vim.visualModeKeyBindings'] += bindings

    # Visual Mode Non-Recursive Bindings
    bindings = get_dict(re.findall(r'vnoremap (.*)', vimrc))
    vscode['vim.visualModeKeyBindingsNonRecursive'] += bindings

    # Replace old settings.json with new settings.json and backup unless specified
    if not args.nobackup:
        os.rename(vsc_path, vsc_path.replace('/settings.json', '/old_settings.json'))
    with open(vsc_path, 'w', encoding='utf-8') as f:
        json.dump(vscode, f, ensure_ascii=False, indent=4)

