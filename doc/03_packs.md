# Packs

Packs, short for package, are organization units that bundle together the various
extension points that StackStorm provides. In a pack you can distribute the following:

* actions
* workflows
* rules
* sensors
* triggers
* Python `requirements.txt` files
* Additional content (think Jinja templates, Ansible playbooks, etc)

Packs are just `git` repos! You can either install them with the URL to the `git` repo
or by name from the public [StackStorm exchange](https://exchange.stackstorm.org)

In this demo we're going to install the `rabbitmq` pack and configure it so
we can post a message to a Queue from StackStorm.

## Install RabbitMQ pack from exchange

First, install the `rabbitmq` pack from my github.
[xod442 github](https://github.com/xod442/stackstorm-rabbitmq).

``` shell
st2 pack install https://github.com/xod442/stackstorm-rabbitmq
```

## Prior to running RabbitMQ
Going to need to jumpstart the rabbitMQ pluggins like this:
`rabbitmq-plugins enable rabbitmq_management`


## Configure RabbitMQ queue

Create a queue in RabbitMQ where messages will be sent

``` shell
rabbitmqadmin declare exchange name=demo type=topic durable=false
rabbitmqadmin declare queue name=demoqueue
rabbitmqadmin declare binding source=demo destination=demoqueue routing_key=demokey
```

### Test out the RabbitMQ pack

```shell
st2 run rabbitmq.publish_message host=127.0.0.1 exchange=demo exchange_type=topic routing_key=demokey message="test"
```

Read from the queue to see if our message was delivered:

```shell
rabbitmqadmin get queue=demoqueue count=99
```
