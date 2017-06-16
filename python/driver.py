#!/usr/bin/python

import os
import logging
import time
from docopt import docopt
from scheduler import MarathonObject
from executor import RabbitMQObject

# Setup logging
logging.basicConfig(format='[%(levelname)-8s] - %(asctime)s - %(message)s - %(filename)s:%(lineno)s',level=logging.DEBUG)

doc = """Framework RabbitMQ on Mesos 
    
    Usage: 
	driver.py --dcos_url <url>
    
    Options:
        -h,  --help     : show this help message
	-dc, --dcos_url : set dcos url
	"""
if __name__ == '__main__':
    # Parse docopt arguments
    args = docopt(doc)

    #logging.info("Received the following arguments:")
    #[logging.info("%s:%s" %(k,v)) for k,v in args.iteritems()]

    dcos_url = args.get("<url>")
    print dcos_url
    
    #if mesos_url == None:
    #    mesos_url = marathon_url.replace("8080","5050")

    marathon = MarathonObject(dcos_url=dcos_url)
    #marathon.modify_etc_hosts()

    logging.info("Starting webservice in progress...")

    # Initialize RabbitMQObject
    rabbit = RabbitMQObject()
    logging.info("Starting RabbitMQ instance in progress...")




