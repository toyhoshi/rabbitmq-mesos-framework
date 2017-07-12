# rabbitmq-mesos-framework

docker pull toyhoshi/rabbitmq-dcos

- Driver
- Scheduler
- Executor

Version 0.1 :) 
- Deploy a rabbitmq cluster with automatic election of a master. 
- We use MesosDNS to find node and rename container, using json from dcos:8123/v1/services/_clustername._tcp.marathon.mesos

Next version
- Try to use mesos.interface module
- Autoscale
- Crash node :)
