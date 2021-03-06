# Shell commands
START_SRV_CMD    = "ERL_EPMD_PORT={EPMD_PORT}RABBITMQ_NODE_PORT={PORT}RABBITMQ_NODENAME={NODENAME}RABBITMQ_DIST_PORT={DIST_PORT}"
START_APP_CMD    = "ERL_EPMD_PORT={EPMD_PORT} rabbitmqctl -n {NODENAME} start_app"
ADD_USERS_CMD    = "ERL_EPMD_PORT={EPMD_PORT} rabbitmqctl -n {NODENAME} add_user {USERNAME} {PASS}"
SET_USER_TAGS    = "ERL_EPMD_PORT={EPMD_PORT} rabbitmqctl -n {NODENAME} set_user_tags {USERNAME} administrator"
STOP_APP_CMD     = "ERL_EPMD_PORT={EPMD_PORT} rabbitmqctl -n {NODENAME} stop_app"
JOIN_CLUSTER_CMD = "ERL_EPMD_PORT={EPMD_PORT} rabbitmqctl -n {NODENAME} join_cluster {MASTER_NODE}"

# Port indices
RABBIT_PORT_INDEX       = 0
RABBIT_DIST_PORT_INDEX  = 2
EPMD_PORT_INDEX         = 3
WS_PORT_INDEX           = 0
