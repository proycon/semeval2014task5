from __future__ import print_function, unicode_literals, division, absolute_import

from libsemeval2014task5.format import SentencePair, Fragment, Writer, Reader

import sys
import os
import datetime
import subprocess
import random


def bold(s):
    CSI="\x1B["
    return CSI+"1m" + s + CSI + "0m"

def white(s):
    CSI="\x1B["
    return CSI+"37m" + s + CSI + "0m"


def red(s):
    CSI="\x1B["
    return CSI+"31m" + s + CSI + "0m"

def green(s):
    CSI="\x1B["
    return CSI+"32m" + s + CSI + "0m"


def yellow(s):
    CSI="\x1B["
    return CSI+"33m" + s + CSI + "0m"


def blue(s):
    CSI="\x1B["
    return CSI+"34m" + s + CSI + "0m"


def magenta(s):
    CSI="\x1B["
    return CSI+"35m" + s + CSI + "0m"


def log(msg, color=None, dobold = False):
    if color:
        msg = color(msg)
    if dobold:
        msg = bold(msg)
    print(msg, file=sys.stderr)

def execheader(name,*outputfiles, **kwargs):
    print("----------------------------------------------------",file=sys.stderr)
    if outputfiles:
        skip = True
        for outputfile in outputfiles:
            if not os.path.exists(outputfile):
                skip = False
                break
        if skip:
            log("Skipping " + name, yellow, True)
            return False
    if 'cmd' in kwargs:
        log("Calling " + name + " " + timestamp() ,white, True)
        log("Command "+ ": " + kwargs['cmd'])
    else:
        log("Calling " + name + " " + timestamp(),white, True)
    return True

def timestamp():
    return "\t" + magenta("@" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

def execfooter(name, r, *outputfiles, **kwargs):
    if 'successcodes' in kwargs:
        successcodes = kwargs['successcodes']
    else:
        successcodes = [0]
    if r in successcodes:
        log("Finished " + name + " " + timestamp(),green,True)
    else:
        log("Runtime error from " + name + ' (return code ' + str(r) + ') ' + timestamp(),red,True)
        return False
    if outputfiles:
        error = False
        for outputfile in outputfiles:
            if os.path.exists(outputfile):
                log("Produced output file " + outputfile,green)
            else:
                log("Expected output file " + outputfile+ ", not produced!",red)
                error = True
        if error:
            return False
    return True

def runcmd(cmd, name, *outputfiles, **kwargs):
    if not execheader(name,*outputfiles, cmd=cmd): return True
    r = subprocess.call(cmd, shell=True)
    return execfooter(name, r, *outputfiles,**kwargs)
