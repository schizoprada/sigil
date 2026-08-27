# ~/sigil/src/sigil/shell/__init__.py
from __future__ import annotations
import os, pty, sys, typing as t
import functools as ft, subprocess as sp

if t.TYPE_CHECKING:
    from subprocess import CompletedProcess

sp.run

def il(
    env: bool = True,
    path: str = '/bin/bash',
    *args,
    **kwargs
    ) -> 'CompletedProcess':
    use = path if not env else os.environ["SHELL"]
    flag = "-lic" if 'bash' in path.lower() else "-ic"
    return sp.run([use, flag, *args], **kwargs)

zsh = ft.partial(il, env=False, path='/bin/zsh')
bash = ft.partial(il, env=False, path='/bin/bash')




def tty(
    env: bool = True,
    path: str = '/bin/bash',
    *args,
    **kwargs
    ) -> int:
    use = path if not env else os.environ["SHELL"]
    return pty.spawn(use, *args, **kwargs)

zty = ft.partial(tty, env=False, path='/bin/zsh')
bty = ft.partial(tty, env=False, path='/bin/bash')


def source(path: str = '~/.bashrc') -> 'CompletedProcess': raise

zshrc = ft.partial(source, path='~/.zshrc')
bashrc = ft.partial(source, path='~/.bashrc')
