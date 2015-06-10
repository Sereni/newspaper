# coding=utf-8
__author__ = 'Sereni'
"""
This script launches test and main crawls consecutively
"""

# fixme scrapy fails silently if internet connection has failed on the second stage -- add some alert?

import sys
import warnings
import time
from subprocess import Popen, PIPE


class NoPathsException(Exception):
    pass

# set pagecount for test corpus
pagecount = ['-s', 'CLOSESPIDER_PAGECOUNT=4']

try:
    name = sys.argv[1]
except:
    raise AttributeError(u"Укажите имя сайта (rbc, ria, izvestia, sovsport, kp)")

print 'Собираю тестовую выборку'
# launch the test corpus crawl
proc = Popen(["scrapy", "crawl", "-a", "first=True"] + [name] + pagecount, stdout=PIPE)

# read stdout
out = proc.communicate()

# write down xpaths
params = [i for i in out[0].split('\n') if i]

# catch a possible DNS lookup error (and all the other mysterious errors)
if not params:
    raise NoPathsException("Не нашлось данных в тестовой выборке. Проверьте, стабильно ли соединение с интернетом.")

spider_args = ["-a"] + [params[0]] + ["-a"] + [params[1]]  # it's a one-string list

# launch the crawl again with these args
print 'Начинаю сбор данных'
main_crawl = Popen(["scrapy", "crawl"] + spider_args + [name])

# sit here, count the seconds, kill the process after a (little) while
time.sleep(300)

print "Закончил сбор данных"
main_crawl.terminate()