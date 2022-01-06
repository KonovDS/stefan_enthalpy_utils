# ui.py by Konov D.S.
# Help functions for enhanced user experience
# Version 0.1
from __future__ import print_function
import sys
import re
import time


# https://stackoverflow.com/questions/3160699/python-progress-bar
class ProgressBar(object):
    DEFAULT = 'Progress: %(bar)s %(percent)3d%%'
    FULL = '%(bar)s %(current)d/%(total)d (%(percent)d%%)'

    def __init__(self, total, width=40, fmt=FULL, symbol='=', output=sys.stdout):
        assert len(symbol) == 1

        self.total = total
        self.width = width
        self.symbol = symbol
        self.output = output
        self.fmt = re.sub(r'(?P<name>%\(.+?\))d', r'\g<name>%dd' % len(str(total)), fmt)
        self.current = 0

    def __call__(self):
        percent = self.current / float(self.total)
        size = int(self.width * percent)
        remaining = self.total - self.current
        bar = '[' + self.symbol * size + ' ' * (self.width - size) + ']'

        args = {
            'total': self.total,
            'bar': bar,
            'current': self.current,
            'percent': percent * 100,
            'remaining': remaining
        }
        print('\r' + self.fmt % args, file=self.output, end='')

    def done(self):
        self.current = self.total
        self()
        print('', file=self.output)


prog = ProgressBar(0, symbol="=")


def start_progress(total):
    prog.total = total
    prog.current = 0
    prog()


def increase_progress():
    prog.current += 1
    prog()
    if prog.current == prog.total:
        prog.done()
        prog.total = 0


def notice(msg, show_time=False):
    mask = ""
    if prog.total != 0:
        mask += "\n"
    if show_time:
        mask += time.strftime("%X") + " "
    mask += "[NOTICE] %s"
    print(mask % msg)


def error(msg, code=-1, show_time=True):
    mask = ""
    if prog.total != 0:
        mask += "\n"
    if show_time:
        mask += time.strftime("%X") + " "
    mask += " [ERROR] %s"
    print(mask % msg)
    print("Exiting with code = %d" % code)
    exit(code)

