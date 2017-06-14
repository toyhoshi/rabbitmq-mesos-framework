FROM docker.io/rabbitmq:latest

MAINTAINER Marco Varagnolo (marco.varagnolo@gmail.com)

RUN sudo rabbitmq-plugins enable rabbitmq_management

# Install Python and relevant libraries
RUN export http_proxy=http://cg00353:Cerved123@proxy.cervedgroup.com:8080 \
 && export https_proxy=http://cg00353:Cerved123@proxy.cervedgroup.com:8080 \

RUN apt-get install -y python python-pip python-dev \
 && pip install flask docopt psutil

# Add necessary files
RUN mkdir -p /instRMQ 
 && cd /instRMQ \
 && git clone http://gitcs01.cervedgroup.com/devops/rabbitmq.git

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

# Set Erlang cookie and access control
RUN echo "ERLANGCOOKIE" > /var/lib/rabbitmq/.erlang.cookie
RUN chown rabbitmq:rabbitmq /var/lib/rabbitmq/.erlang.cookie
RUN chmod 400 /var/lib/rabbitmq/.erlang.cookie

# Enable clients to connect from hosts other than localhost
RUN echo "[{rabbit, [{loopback_users, []}]}]." > /etc/rabbitmq/rabbitmq.config

# Entrypoint script
ENTRYPOINT ["python", "/instRMQ/start-rabbitmq.py"]

