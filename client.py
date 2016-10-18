#!/usr/bin/env python
# -*- coding: utf-8 -*-


from oslo_config import cfg
from oslo_log import log as logging
from i18n import _, _LI, _LW, _LE
import oslo_messaging


oslo_messaging_opts = [
    cfg.StrOpt('event_stream_topic',
                default="test_notification",
                help=_('topic name for receiving events from a queue')
    )
]

cfg.CONF.register_opts(oslo_messaging_opts, group='oslo_messaging')

"""
For Notification mode, the control_exchange means the exchange in rabbitmq.
"""
oslo_messaging.set_transport_defaults(control_exchange='notification')

"""
Init the oslo_log
"""
LOG = logging.getLogger(__name__)

def prepare():
    product_name = 'oslo_test'
    logging.register_options(cfg.CONF)
    logging.setup(cfg.CONF, product_name)

class Client(object):

    def __init__(self):
        """
        Usage for cfg.CONF
            cfg.CONF.{group_name}.{cfg.StrOpt.name}
        """
        self.topic = cfg.CONF.oslo_messaging.event_stream_topic
        prepare()

    def send(self, message):
        pass


class RPCClient(Client):

    def __init__(self):
        super(RPCClient, self).__init__()
        self.transport = oslo_messaging.get_transport(cfg.CONF)
        self.target = oslo_messaging.Target(topic=self.topic, exchange='common',
                namespace='control', fanout=False, version='1.0')
        self.client = oslo_messaging.RPCClient(self.transport, self.target)

    def send(self, message):
        """method to send message to listener
        :param message:{} a dict object to send
        :return: None
        """
        """
        RPCClient has two function for sending message
        1.cast(ctxt, method, **kwargs): Do not have return value
        2.call(ctxt, method, **kwargs): Have return value
        :param ctxt:
        :param method:
        :param **kwargs:
        """
        self.client.cast({}, 'update_info', container=message)


class NotificationClient(Client):

    def __init__(self):
        super(NotificationClient, self).__init__()


    def send(self, message):
        """method to send message to listener
        :param message:{} a dict object to send
        :return: None
        """
        pass

if __name__ == '__main__':
    message = {'test':'A Test for oslo_messaging'}
    rpc_client = Client()
    notification_client = NotificationClient()
    #rpc_client.send(message)
    #notification_client.send(message)
    prepare()
    LOG.info(_LI("welcome"))
