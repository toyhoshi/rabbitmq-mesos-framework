import subprocess
import re
import os
import urllib, json 
from urlparse import urlparse

#p = subprocess.Popen(["ps caux | grep docker"], shell=True,stdout=subprocess.PIPE)
#out, err = p.communicate()
#pid = out.split()[1]
#print "PID %s" % pid


#retvalue = subprocess.Popen(["echo $TEST"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#out = retvalue.communicate()[0]
#data=[e.strip() for e in out.split(',')]
#print "Value: %s" % data[1][:-1]


line = "-> 10.57.0.144:28078"

regex_realhost = ur"-> (10\.57\.0\.(\d{1,3})):(\d+)"
print len(re.findall(regex_realhost, line, re.DOTALL))

print "---------------------------------"


#url = "http://test-dcos1:8123/v1/services/_cluster-rmq._tcp.marathon.mesos"
#data = urllib.urlopen(url).read()
#outp = json.loads(data)

#for key in outp:
#	if (key['ip'] == os.environ["HOST"]) & (key['port'] == "5672"):
#		print key['host'][:-1]

#os.system('/usr/bin/hostname ' + key['host'][:-1])

def compare_host_ip(host):
    # http://test-dcos1:8123/v1/services/_cluster-rmq._tcp.marathon.mesos
    url = "http://test-dcos1:8123/v1/services/_cluster-rmq._tcp.marathon.mesos"
    data = urllib.urlopen(url).read()
    outp = json.loads(data)

    for key in outp:
        if key['ip'] == host:
            own_host = key['host'][:-1]

    return own_host

print compare_host_ip("10.57.0.187")


print "---------------------------------"

aaa = "aaaa.marathon.mesos"
hostname = aaa.partition('.')
print hostname[0]
