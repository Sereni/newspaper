__author__ = 'Sereni'
"""
This script launches test and main crawls consecutively
"""

import sys
import warnings
import time
from subprocess import Popen, PIPE

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
    wordcount = 'wordcount=100'
    warnings.warn("No wordcount provided. Using default value")
try:
    dates = sys.argv[3]
except IndexError:
    dates = 'None'
    warnings.warn("No dates provided")

# fixme doesn't stop on keyboard interrupt or anything at all, really
# mmmmmm
# can I send a signal to spiders from here?
# key pressed -> keyboard interrupt exception -> signal to scrapy through stdin -> spiders stop
# ... but that's for testing...
# todo catch exception for unresolved server
#  ERROR: Error downloading <GET http://izvestia.ru>: DNS lookup failed: address 'izvestia.ru' not found: [Errno 8] nodename nor servname provided, or not known.
# todo subprocess shell True for windows -- find a better way or implement
# launch the test corpus crawl
# proc = Popen(["scrapy", "crawl", "-a", "first=True"] + [name] + pagecount, stdout=PIPE)
proc = Popen(' '.join(["scrapy", "crawl", "-a", "first=True"] + [name] + pagecount), stdout=PIPE, shell=True)


# read stdout
out = proc.communicate()

# write down xpaths
xpaths = [i for i in out[0].split('\n') if i]
# xpaths = [i.replace('"', '\"') for i in out[0].split('\n') if i]


spider_args = ['-a', wordcount, '-a'] + xpaths  # it's a one-string list

# launch the crawl again with these args
main_crawl = Popen(["scrapy", "crawl"] + spider_args + [name])
# args = " ".join(['scrapy', 'crawl'] + spider_args + [name])
# main_crawl = Popen(args, shell=True)

# sit here, count the seconds, kill the process after a (little) while
time.sleep(3)
# start = time.clock()
# while time.clock() - start < 300:
#     # interesting, if I put sleep here, does it pause the subprocess? I guess not.
#     time.sleep(5)
#     # but then, hey, I don't need the loop at all.
main_crawl.terminate()