#!/usr/bin/python

import os
import logging
import time
import urllib, json
from docopt import docopt
from scheduler import MarathonObject
from executor import RabbitMQObject
from webservice import WebService

# Setup logging (%(filename)s:%(lineno)s)
logging.basicConfig(format='[%(levelname)-5s] - %(asctime)s - %(message)s',level=logging.DEBUG)

doc = """Framework RabbitMQ on Mesos
    Usage:
	driver.py -dc <url> -rn <namenode>

    Options:
    -h                                 show this help message
	-dc=<url>                          set dcos url
	-rn=<rabbit_nodename>              Name of the rabbit node
	"""

def compare_host_ip(host):
    # http://test-dcos1:8123/v1/services/_cluster-rmq._tcp.marathon.mesos
    url = "http://test-dcos1:8123/v1/services/_cluster-rmq._tcp.marathon.mesos"
    data = urllib.urlopen(url).read()
    outp = json.loads(data)

    for key in outp:
        if key['ip'] == host:
            own_host = key['host'][:-1]

    return own_host


if __name__ == '__main__':
    # Parse docopt arguments
    args = docopt(doc)

    #logging.info("Received the following arguments:")
    #[logging.info("%s:%s" %(k,v)) for k,v in args.iteritems()]

    logging.info("*** Initializing Driver...")
    dcos_url = args.get("<url>")
    rabbit_nodename = args.get("<namenode>")

    #if mesos_url == None:
    #    mesos_url = marathon_url.replace("8080","5050")

    marathon = MarathonObject(dcos_url=dcos_url)
    # marathon.modify_etc_hosts()

    logging.info("Starting webservice in progress...")

    # Initialize RabbitMQObject
    rabbit = RabbitMQObject(rabbit_nodename=rabbit_nodename)
    logging.info("Starting RabbitMQ instance in progress...")

     # Start server
    rabbit_pid = rabbit.start_rabbit_server()
    # Wait several secs until server is started
    time.sleep(15)
    rabbit.start_rabbit_app()
    logging.info("RabbitMQ instance successfully started!")

    # Join cluster
    master_hosts = marathon.find_master_hosts()
    if master_hosts != None:
        logging.info("Master hosts != None")
        rabbit.stop_rabbit_app()
        # Loop until cluster has been successfully formed
        success = False
        for master_host in master_hosts:
            if success == False:
                logging.info("Try rabbit setup cluster...")
                success = rabbit.setup_cluster(master_host=compare_host_ip(master_host), retry_count=10, retry_interval=3)
                                            #   retry_count=int(args.get("--retry_count")),
                                            #   retry_interval=int(args.get("--retry_interval")))
                logging.debug("Connecting to node %s got status: %s" %(master_host, success))
            else:
                logging.debug("Not attempting to join node %s to form cluster because one of the earlier attempts was successful" %master_host)
        if success  == False:
            # If cannot form cluster with any other nodes, stop trying and run in standalone
            logging.error("Could not connect to any other RabbitMQ node to form a cluster. Running in standalone...")
        # Start Rabbit app
        rabbit.start_rabbit_app()

    # Start WebService (mainly for Marathon HealthCheck)
    logging.debug("Starting webservice in progress, pid %s on nodename %s..." %(rabbit_pid, rabbit_nodename))
    WebService(5000, rabbit_pid, rabbit_nodename + "@" + os.environ.get("HOSTNAME"))
