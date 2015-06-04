__author__ = 'Sereni'
"""
This script launches test and main crawls consecutively
"""

import sys
import warnings
from subprocess import Popen, PIPE


class NoPathsException(Exception):
    pass

# set pagecount for test corpus
pagecount = ['-s', 'CLOSESPIDER_PAGECOUNT=2']

# read arguments from command line
# okay. this has no checks whatsoever as to what was submitted. benevolent AND careful users only
# todo write checks for args. I _really_ want to use click for this.
# arg order: name, wordcount, dates
try:
    name = sys.argv[1]
except:
    raise AttributeError("Provide the bot name")
try:
    wordcount = 'wordcount=' + sys.argv[2]
except IndexError:
    wordcount = 'wordcount=10000'
    warnings.warn("No wordcount provided. Using default value")
try:
    dates = sys.argv[3]
except IndexError:
    dates = 'None'
    warnings.warn("No dates provided")

# launch the test corpus crawl
proc = Popen(["scrapy", "crawl", "-a", "first=True"] + [name] + pagecount, stdout=PIPE)

# read stdout
out = proc.communicate()

# fixme this might need an -a before each xpath
# write down xpaths
xpaths = [i for i in out[0].split('\n') if i]

if not xpaths:
    raise NoPathsException("No xpaths found from test corpus. Are you connected to the internet?")

spider_args = ["-a", wordcount, "-a"] + xpaths  # it's a one-string list

# launch the crawl again with these args
Popen(["scrapy", "crawl"] + spider_args + [name])