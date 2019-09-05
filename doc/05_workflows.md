# Workflows

Workflows allow us to chain actions together, implement conditional logic and branching, and
turn actions into composable automations.

Workflows are actions too! They simply use a different `runner_type: mistral-v2`.

We'll demonstrate workflows by creating one that retrieves the NASA APOD picture URL
then publish this URL to a RabbitMQ Queue.

### Create workflow action metadata

The workflow action's metadata file is just like any other action metadata file. It
has `runner_type: mistral-v2`, input parameters just like the a Python action,
and `entry_point` set to the path of workflow definition YAML file (relative to
the pack's `actions/` directory)

Edit `/opt/stackstorm/packs/tutorial/actions/nasa_apod_rabbitmq_publish.yaml` and insert
the following content:

``` yaml
---
name: nasa_apod_rabbitmq_publish
pack: tutorial
description: "Queries NASA's APOD (Astronomy Picture Of the Day) API to get the link to the picture of the day, then publishes that link to a RabbitMQ queue"
runner_type: "orquesta"
enabled: true
entry_point: workflows/nasa_apod_rabbitmq_publish.yaml
parameters:
  date:
    type: string
    description: "The date [YYYY-MM-DD] of the APOD image to retrieve."
  message:
    type: string
    description: "Extra message to publish with the URL"
  host:
    type: string
    default: "127.0.0.1"
  exchange:
    type: string
    default: "demo"
    description: "Name of the RabbitMQ exchange"
  exchange_type:
    type: string
    default: "topic"
    description: "Type of the RabbitMQ exchange"
  routing_key:
    type: string
    default: "demokey"
    description: "Name of the RabbitMQ routing key"
```

-----------
**NOTE**
If you're struggling and just need the answer, simply copy the file from our
answers directory:
```shell
cp /opt/stackstorm/packs/tutorial/etc/answers/actions/nasa_apod_rabbitmq_publish.yaml /opt/stackstorm/packs/tutorial/actions/nasa_apod_rabbitmq_publish.yaml
```
-----------

We need to tell StackStorm about our new action metadata file:

```shell
st2ctl reload --register-actions
```

### Create the workflow

StackStorm has several different Workflow engines including
[ActionChain](https://docs.stackstorm.com/actionchain.html),
[Mistral](https://docs.stackstorm.com/mistral.html),
and the upcoming [Orchestra](https://github.com/StackStorm/orchestra).
We're going to be using Mistral for this example.

In our workflow we want to call `tutorial.nasa_apod` to retrieve our image URL.
Next we'll publish this as a message to RabbitMQ using the `twitter.update_status` action.

**Note** The name of the workflow within the workflow file, **MUST** be the same
as the name of the StackStorm `pack.action`:

Edit `/opt/stackstorm/packs/tutorial/actions/workflows/nasa_apod_rabbitmq_publish.yaml`

Content:

``` yaml
version: '1.0'

description: A workflow that gets the apod and posts to rabbitmq.

input:
  - date
  - message
  - host
  - exchange
  - exchange_type
  - routing_key

tasks:
  get_apod_url:
    action: tutorial.nasa_apod
    input:
      date: "<% ctx().date %>"
    next:
      - when: <% succeeded() %>
        publish:
          - apod_url: <% result().result %>
        do: publish_to_rabbitmq

  publish_to_rabbitmq:
    action: rabbitmq.publish_message
    input:
      host: "<% ctx().host %>"
      exchange: "<% ctx().exchange %>"
      exchange_type: "<% ctx().exchange_type %>"
      routing_key: "<% ctx().routing_key %>"
      message: "<% ctx().apod_url.url %>"
```

-----------
**NOTE**
If you're struggling and just need the answer, simply copy the file from our
answers directory:
```shell
cp /opt/stackstorm/packs/tutorial/etc/answers/actions/workflows/nasa_apod_rabbitmq_publish.yaml /opt/stackstorm/packs/tutorial/actions/workflows/nasa_apod_rabbitmq_publish.yaml
```
-----------

### Test

Run our action, creating a new message!

``` shell
st2 run tutorial.nasa_apod_rabbitmq_publish date="2018-07-04"
```

Read from the queue to see if our message was delivered:

```shell
rabbitmqadmin get queue=demoqueue count=99
```
**NOTE**
There is a lot going on in this work flow. Lets break it down for a little better understanding.

1. The first thing we have to do is import the variables we will need for this work flow.
These are passed from the corresponding YAML file that's in the actions directory.

![Workflow - Import variables](/img/import-vars.png)

2. Next step in to run a st2 action to get the picture of the day from nasa.

![Workflow - Get picture from website](/img/get-pic.png)

3. Now we have to assign the data we get back from nasa to a variable.

![Workflow - Assign the picture URL](/img/assign-vars.png)

4. We finish up the workflow by publishing the picture URL to the rabbitmq bus.

![Workflow - Publish to the bus](/img/import-vars.png)
