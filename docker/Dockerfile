FROM docker.io/rabbitmq:latest

MAINTAINER Marco Varagnolo (marco.varagnolo@gmail.com)

RUN rabbitmq-plugins enable rabbitmq_management

# Install Python and relevant libraries
RUN export http_proxy=http://cg00353:Cerved123@proxy.cervedgroup.com:8080 \
    && export https_proxy=http://cg00353:Cerved123@proxy.cervedgroup.com:8080 \
    && apt-get update \
    && apt-get install -y python python-pip python-dev \
    && pip install flask docopt psutil

# Add necessary files
RUN mkdir -p /instRMQ 
#    && cd /instRMQ \
#    && git clone http://gitcs01.cervedgroup.com/devops/rabbitmq.git

ADD /root/rabbitmq-mesos-framework/python/* /instRMQ 

EXPOSE 5000
EXPOSE 5672
EXPOSE 4369
EXPOSE 25672
EXPOSE 5672
EXPOSE 5671
EXPOSE 15672
EXPOSE 61613
EXPOSE 61614
EXPOSE 1883
EXPOSE 8883

# Enable clients to connect from hosts other than localhost
RUN echo "[{rabbit, [{loopback_users, []}]}]." > /etc/rabbitmq/rabbitmq.config

# Entrypoint script
ENTRYPOINT ["python", "/instRMQ/driver.py"]

