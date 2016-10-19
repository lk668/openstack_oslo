# oslo_\* module in OpenStack
In this repository, I introduce the usage of oslo_messaging, oslo_config and oslo_log. These modules
are often used in OpenStack.

## Requirements:

Install related package. You can run the following commands on ubuntu.

> sudo apt-get install python-oslo-messaging python-oslo-log
> python-oslo-config python-oslo-i18n

## Introduction

This repository, I introduce two mode in oslo_messaing.

1. RPC mode
2. Notification mode: This mode is based on rabbitmq

## Reference:

- [oslo_messaging](http://docs.openstack.org/developer/oslo.messaging/)
- [RPC Server](http://docs.openstack.org/developer/oslo.messaging/server.html)
- [RPC Client](http://docs.openstack.org/developer/oslo.messaging/rpcclient.html)
- [Notification Listener](http://docs.openstack.org/developer/oslo.messaging/notification_listener.html)
- [Notification Client](http://docs.openstack.org/developer/oslo.messaging/notifier.html)
