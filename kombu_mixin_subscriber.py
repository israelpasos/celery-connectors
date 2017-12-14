#!/usr/bin/env python

import logging
from celery_connectors.utils import ev
from celery_connectors.log.setup_logging import setup_logging
from celery_connectors.kombu_subscriber import KombuSubscriber

setup_logging()

name = "kombu-mixin-subscriber"

log = logging.getLogger(name)

log.info("Start - {}".format(name))


recv_msgs = []


def handle_message(body, message):
    log.info(("callback received msg "
              "body={}")
             .format(body))
    recv_msgs.append(body)
    message.ack()
# end of handle_message


# Initialize KombuSubscriber
ssl_options = {}
sub = KombuSubscriber("kombu-mixin-subscriber",
                      ev("BROKER_URL", "amqp://rabbitmq:rabbitmq@localhost:5672//"),
                      ssl_options)


# Now consume:
seconds_to_consume = 10.0
heartbeat = 60
serializer = "application/json"
exchange = "reporting.payments"
routing_key = "reporting.payments"
queue = "reporting.payments"
sub.consume(callback=handle_message,
            queue=queue,
            exchange=exchange,
            routing_key=routing_key,
            serializer=serializer,
            heartbeat=heartbeat,
            time_to_wait=seconds_to_consume)

log.info("End - {}".format(name))