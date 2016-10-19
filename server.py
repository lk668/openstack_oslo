#!/usr/bin/env python
# -*- coding: utf-8 -*-

from oslo_config import cfg
from oslo_log import log as logging
from i18n import _, _LI
import oslo_messaging
import json
import time

oslo_messaging_opts = [
    cfg.StrOpt('event_stream_topic',
               default='test_notification',
               help=_('topic name for receiving events from a queue'))
]

cfg.CONF.register_opts(oslo_messaging_opts, group='oslo_messaging')


LOG = logging.getLogger(__name__)

def prepare():
    product_name = "oslo_server"
    logging.register_options(cfg.CONF)
    logging.setup(cfg.CONF, product_name)


class RPCEndPoint():
    target = oslo_messaging.Target(namespace="control", version='1.0')

    def update_info(self, ctx, container):
        """
        method is used for client the run
        """
        self.action(container)

    def action(self, data):
        LOG.info(_LI(json.dumps(data)))


class NotificationEndPoint():
    filter_rule = oslo_messaging.NotificationFilter(
            publisher_id='oslo_test')

    def info(self, ctxt, publisher_id, event_type, payload, metadata):
        """
        Method is used for notification client.
        """
        self.action(payload)

    def action(self, data):
        LOG.info(_LI(json.dumps(data)))


class Server(object):

    def __init__(self):
        self.topic = cfg.CONF.oslo_messaging.event_stream_topic
        self.server = None
        prepare()


class RPCServer(Server):

    def __init__(self):
        super(RPCServer, self).__init__()
        self.hostname = "damonl-lk"
        self.transport = oslo_messaging.get_transport(cfg.CONF)
        self.target = oslo_messaging.Target(topic=self.topic, exchange='common', server=self.hostname, fanout=False)
        self.endpoints = [RPCEndPoint()]

    def start(self):
        LOG.info(_LI("Start RPC server..."))
        self.server = oslo_messaging.get_rpc_server(self.transport, self.target, self.endpoints)
        self.server.start()
        self.server.wait()

    def stop(self, graceful=False):
        if self.server:
            LOG.info(_LI("Stop the RPC server..."))
            self.server.stop()
            if graceful:
                LOG.info(_LI("RPC server stopped successfully. Waiting for final message to be processed..."))
                self.server.wait()


class NotificationServer(Server):

    def __init__(self):
        super(NotificationServer, self).__init__()
        self.transport = oslo_messaging.get_notification_transport(cfg.CONF)
        # The exchange must be the same as control_exchange in transport setting in client.
        self.targets = [oslo_messaging.Target(topic=self.topic, exchange='notification')]
        self.endpoints = [NotificationEndPoint()]

    def start(self):
        LOG.info(_LI("Start Notification server..."))
        self.server = oslo_messaging.get_notification_listener(self.transport, self.targets, self.endpoints)
        self.server.start()
        self.server.wait()

    def stop(self, graceful=False):
        if self.server:
            LOG.info(_LI("Stop the Notification server..."))
            self.server.stop()
            if graceful:
                LOG.info(_LI("Notification server stopped successfully. Waiting for final message to be processed..."))
                self.server.wait()


if __name__ == '__main__':
    rpc_server = RPCServer()
    notification_server = NotificationServer()
    rpc_server.start()
    #notification_server.start()
