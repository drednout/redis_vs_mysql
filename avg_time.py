"""
Usage:
    python avg_time.py < file_name.txt
"""
import sys
import re
import datetime

def to_micro_seconds(t):
    return (t.hour*3600 + t.minute*60 + t.second) * 10**6 + t.microsecond

lines = sys.stdin.readlines()
times = []
for line in lines:
    m = re.search("\d:\d{2}:\d{2}[.]\d+", line)
    times.append(to_micro_seconds(datetime.datetime.strptime(m.group(0), "%H:%M:%S.%f").time()))

times.sort()
times = times[1:-1]
print(times)
print("%.2f" % (round(sum(times)/float(10**6)/len(times), 3)) )
