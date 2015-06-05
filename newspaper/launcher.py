__author__ = 'Sereni'
"""
This script launches test and main crawls consecutively
"""

# todo add some meaningful progress messages

import sys
import warnings
import time
from subprocess import Popen, PIPE


class NoPathsException(Exception):
    pass

# set pagecount for test corpus
# fixme note: on extra slow machines, pagecount=2 may not be enough to gather a large test corpus
pagecount = ['-s', 'CLOSESPIDER_PAGECOUNT=2']

try:
    name = sys.argv[1]
except:
    raise AttributeError("Provide the bot name")

# launch the test corpus crawl
proc = Popen(["scrapy", "crawl", "-a", "first=True"] + [name] + pagecount, stdout=PIPE)

# read stdout
out = proc.communicate()

# write down xpaths
params = [i for i in out[0].split('\n') if i]

# catch a possible DNS lookup error (and all the other mysterious errors)
if not params:
    raise NoPathsException("No xpaths found from test corpus. Are you connected to the internet?")

spider_args = ["-a"] + [params[0]] + ["-a"] + [params[1]]  # it's a one-string list

# launch the crawl again with these args
main_crawl = Popen(["scrapy", "crawl"] + spider_args + [name])

# sit here, count the seconds, kill the process after a (little) while
time.sleep(5)

main_crawl.terminate()