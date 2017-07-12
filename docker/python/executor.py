import os
import logging
import subprocess, shlex
import multiprocessing
import properties
import time
import urllib, json

# Function to start RabbitMQ server
def start_rabbit_server(process_cmd):
    logging.debug("Starting RabbitMQ server with the following command: %s" %process_cmd)
    process_cmd = shlex.split(process_cmd)
    subprocess.Popen(process_cmd).wait()
    logging.error("RabbitMQ server stopped!")

class RabbitMQObject:

    own_host = None
    own_port = None
    own_ip = None
    own_dist_port = None
    own_epmd_port = None
    master_host = None
    master_port = None
    nodename = None
    nodename_short = None

    def __init__(self, rabbit_nodename):
        logging.info("*** Initializing Executor...")
        # Obtain own host and ports
        #own_host = os.environ["HOSTNAME"]
        #self.own_host = own_host[:own_host.find(".")]

        # http://test-dcos1:8123/v1/services/_cluster-rmq._tcp.marathon.mesos
        url = "http://test-dcos1:8123/v1/services/_cluster-rmq._tcp.marathon.mesos"
        data = urllib.urlopen(url).read()
        outp = json.loads(data)

        # Set MesosDNS hostname
        for key in outp:
            if (key['ip'] == os.environ["HOST"]) & (key['port'] == "5672"):
                self.own_host = key['host'][:-1].partition('.')[0]
                self.own_ip = key['ip']

        # Add entry on /etc/hosts
        logging.info("Registering rabbitmq nodes (slave hosts) in /etc/hosts in progress...")
        env = open("/etc/hosts","a")
        # env.write(self.own_ip + "\t" + self.own_host)
        # logging.info("Added rabbitmq nodes %s with ip %s" %(self.own_ip, self.own_host))

        # Add IP and hostname (without domain marathon.mesos)
        for key in outp:
            if (key['port'] == "4369"):
                node = key['host'][:-1].partition('.')[0]
                env.write(key['ip'] + "\t" + node + "\n")

        logging.info("MesosDNS looking for host...: %s" %self.own_host)
        os.system('hostname '+ self.own_host)
        os.environ["HOSTNAME"] = self.own_host
        logging.debug("Changed hostname to: %s", self.own_host)

        # self.own_host = os.environ["HOSTNAME"]

        own_ports = os.environ["PORTS"].split(",")
        self.own_port = own_ports[properties.RABBIT_PORT_INDEX]
        # $PORT0 from hostPort
        logging.info("Own hostname is %s and own port is %s" %(self.own_host, self.own_port))

        self.own_dist_port = own_ports[properties.RABBIT_DIST_PORT_INDEX]
        logging.info("RABBIT_DIST_PORT set to %s" %self.own_dist_port)

        self.own_epmd_port = own_ports[properties.EPMD_PORT_INDEX]
        logging.info("Erlang port mapper daemon's port set to %s" %self.own_epmd_port)

        self.nodename = str(rabbit_nodename) + "@" + str(self.own_host)
        self.nodename_short = rabbit_nodename
        logging.debug("Nodename set to %s" %self.nodename)

        # Set erlang cookie
        # self.set_erlang_cookie(erlang_cookie)

    # def set_erlang_cookie(self, erlang_cookie):
    #     logging.debug("Setting Erlang cookie (%s) in progress" %erlang_cookie)
    #     self.exec_rabbitmq_command(cmd = 'sudo echo "%s" > /var/lib/rabbitmq/.erlang.cookie' %erlang_cookie)
    #     self.exec_rabbitmq_command(cmd = 'sudo chown rabbitmq:rabbitmq /var/lib/rabbitmq/.erlang.cookie')
    #     self.exec_rabbitmq_command(cmd = 'sudo chmod 400 /var/lib/rabbitmq/.erlang.cookie')
    #     logging.info("Erlang cookie (%s) successfully set!" %erlang_cookie)

    def exec_rabbitmq_command(self, cmd, replace_dict=None):
        logging.debug("Executing shell command in progress...")
        if replace_dict != None:
            for k,v in replace_dict.iteritems():
                cmd = cmd.replace(k, v)
        logging.debug("Executing the following shell command: %s" %cmd)

        # cmd = shlex.split(cmd)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #p = subprocess.Popen(cmd)
        p.wait()

        if p.returncode != 0:
            raise Exception("Was not able to execute shell command! Received exit code %s"
                                %(p.returncode))
        logging.debug("Shell command has been successfully executed!")

    def start_rabbit_server(self):
        logging.debug("Starting RabbitMQ server in progress...")
        nodename = self.nodename

        env = open("/instRMQ/rabbitmq-envX.conf","w")

        start_rabbit_cmd = properties.START_SRV_CMD.replace("{PORT}", self.own_port + '\n')
        start_rabbit_cmd = start_rabbit_cmd.replace("{NODENAME}", nodename + '\n')
        start_rabbit_cmd = start_rabbit_cmd.replace("{EPMD_PORT}", self.own_epmd_port + '\n')
        start_rabbit_cmd = start_rabbit_cmd.replace("{DIST_PORT}", self.own_dist_port + '\n')

        #p = multiprocessing.Process(target=start_rabbit_server, args=(start_rabbit_cmd, ))
        #p.start()

        env.write(start_rabbit_cmd)
        # p = subprocess.Popen('RABBITMQ_CONF_ENV_FILE=/instRMQ/rabbitmq-envX.conf rabbitmq-server -detached', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p = subprocess.Popen('RABBITMQ_CONF_ENV_FILE=/instRMQ/rabbitmq-envX.conf rabbitmq-server > /var/log/rabbitmq/rabbitmq.log &', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # rabbit_pid = p.pid
        gpid = subprocess.Popen(["rabbitmqctl status | grep pid"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        rval = gpid.communicate()[0]
        data = [e.strip() for e in rval.split(',')]

        rabbit_pid = data[1][:-1]

        logging.info("RabbitMQ server started (process pid: %s)!" %rabbit_pid)
        return rabbit_pid


    def start_rabbit_app(self):
        logging.debug("Starting RabbitMQ app in progress...")
        self.exec_rabbitmq_command(cmd = properties.START_APP_CMD,
                                   replace_dict={"{NODENAME}": self.nodename,
                                                 "{EPMD_PORT}": self.own_epmd_port})
        logging.info("RabbitMQ app successfully started!")

    def stop_rabbit_app(self):
        logging.debug("Stopping RabbitMQ app in progress...")
        self.exec_rabbitmq_command(cmd = properties.STOP_APP_CMD,
                                   replace_dict={"{NODENAME}": self.nodename,
                                                 "{EPMD_PORT}": self.own_epmd_port})
        logging.info("RabbitMQ app successfully stopped!")

    def join_master(self, master_nodename):
        logging.debug("Joining RabbitMQ master in progress...")
        self.exec_rabbitmq_command(cmd = properties.JOIN_CLUSTER_CMD,
                                   replace_dict={"{NODENAME}": self.nodename,
                                                 "{EPMD_PORT}": self.own_epmd_port,
                                                 "{MASTER_NODE}": master_nodename})
        logging.info("RabbitMQ node successfully joined cluster!")

    def add_user(self, username, password):
        logging.info("Setting admin user for RabbitMQ in progress...")
        self.exec_rabbitmq_command(cmd = properties.ADD_RABBIT_USER,
                                   replace_dict={"{NODENAME}": self.nodename,
                                                 "{EPMD_PORT}": self.own_epmd_port,
                                                 "{USERNAME}": username,
                                                 "{PASS}": password})
        self.exec_rabbitmq_command(cmd = properties.SET_USER_TAGS,
                                   replace_dict={"{NODENAME}": self.nodename,
                                                 "{EPMD_PORT}": self.own_epmd_port,
                                                 "{USERNAME}": username})
        logging.info("Successfully added user %s to RabbitMQ. Password: %s" %(username, password))

    def setup_cluster(self, master_host, retry_count, retry_interval):
        if master_host != None:
            # Set hostname without domain
            master_host = master_host.partition('.')[0]
            logging.info("Setting up cluster in progress...")
            master_nodename = "%s@%s" %(self.nodename_short,
                                          master_host)
                                        # master_host[:master_host.find(".")])
            if master_nodename != self.nodename:
                logging.info("Joining cluster (%s) is in progress..." %master_nodename)

                i = 1 # Counter
                looping = True
                success = False
                while looping == True:
                    try:
                        self.join_master(master_nodename)
                        logging.info("RabbitMQ node successfully connected to the cluster!")
                        success = True
                        looping = False
                    except:
                        logging.info("Was not able to join node named %s. Retrying in %s seconds..." %(master_nodename,
                                                                                               retry_interval))
                        time.sleep(retry_interval)
                        i += 1
                    if i >= retry_count:
                        logging.debug("Attempted unsuccessfully to form cluster with node named %s %s times" %(master_nodename, retry_count))
                        looping = False
                if success:
                    return True
                else:
                    return False
            else:
                return True
