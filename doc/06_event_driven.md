# Event Driven Demo

This demo will setup a pipeline that will listen for messages on specific RabbitMQ queues
words and then write the specific URL as a `hyperlink` to an etc/index.html, a file inside this pack.
In order to accomplish this we're going to use the following components:

* Sensor - Will query the RabbitMQ API for message on a specific queue
* Trigger - Events that are emitted from the Sensor when a new message is received on the queue
* Rule - Will match the triggers from the Sensor and invoke an action
* Action - Metadata describing the workflow to execute in order to write URL to file
* Workflow - Series of steps (actions) to get the APOD from the NASA site, extract the URL and
  .write that URL to etc/index.

## Configure the Sensor

We're going to reuse an existing sensor from the `rabbitmq` pack called `rabbitmq.queues_sensor`.
This sensor uses information from the `rabbitmq` pack configuration located in:
`/opt/stackstorm/configs/rabbitmq.yaml`. The config file contains a `queues` parameter
that tells `rabbitmq.queues_sensor` what queues to listen for messages on.

You can use the shortcut below or......carry on!

Copy `/opt/stackstorm/packs/rabbitmq/rabbitmq.yaml.example` to `/opt/stackstorm/configs/rabbitmq.yaml`:

```yaml
sudo cp /opt/stackstorm/packs/rabbitmq/rabbitmq.yaml.example /opt/stackstorm/configs/rabbitmq.yaml
```

Edit the file, changing `host` to `127.0.0.1` and add the `demoqueue` to the `queues` parameter:

**NOTE** You'll need to edit this file with `sudo /opt/stackstorm/configs/rabbitmq.yaml`

``` yaml
---
sensor_config:
  host: "127.0.0.1"
  username: "guest"
  password: "guest"
  rabbitmq_queue_sensor:
    queues:
      - "demoqueue"
    deserialization_method: "json"
```

-----------
**NOTE**
If you're struggling and just need the answer, simply copy the file from our
answers directory:
```shell
sudo cp /opt/stackstorm/packs/tutorial/etc/answers/configs/rabbitmq.yaml /opt/stackstorm/configs/rabbitmq.yaml
```
-----------

Next we'll reload the pack's configuration so that the database contains
the new values: **NOTE** Follow very closely, st2ctl only the configs at this point.
If you simply st2ctl reload, you will wipe out the rabbitmq bus config from module 3.

``` shell
st2ctl reload --register-configs
```

Then we'll need to restart the Sensor so it uses the new configuration:

``` shell
sudo systemctl restart st2sensorcontainer
```

### Sensor Testing

Publish a new message to RabbitMQ

```shell
st2 run tutorial.nasa_apod_rabbitmq_publish
```

Check StackStorm to ensure a new trigger instance was created.

``` shell
$ st2 trigger-instance list --trigger rabbitmq.new_message
+--------------------------+----------------+-----------------+-----------+
| id                       | trigger        | occurrence_time | status    |
+--------------------------+----------------+-----------------+-----------+
| 5b5dce8e587be00afa97911f | rabbitmq.new_m | Sun, 29 Jul     | processed |
|                          | essage         | 2018 14:26:22   |           |
|                          |                | UTC             |           |
| 5b5dce8e587be00afa979120 | rabbitmq.new_m | Sun, 29 Jul     | processed |
|                          | essage         | 2018 14:26:22   |           |
|                          |                | UTC             |           |
| 5b5dce8e587be00afa97912b | rabbitmq.new_m | Sun, 29 Jul     | processed |
|                          | essage         | 2018 14:26:22   |           |
|                          |                | UTC             |           |
+--------------------------+----------------+-----------------+-----------+
```


## Some good news!!!!!!!!

There is an easier way to see what's going on in stackstorm. You can log into the web interface. Point a browser at 127.0.0.1 of you stackstorm workstation and login with st2admin/`password you used when you installed stackstorm`

I know its late in the training to tell you about the GUI but I think you need to know both.
It's difficult to develop actions and rules using the GUI but it's excellent for seeing the execution
history.

![Watching - Getting feedback](/img/watching.png)

## Configure the Rule

The rule that we're going to write will match the `rabbitmq.new_message` trigger
and invoke an action to write the NASA APOD URL to the tutorial/etc/index.html file.
which is part of the tutorial. (**note**: the action doesn't exist
yet, but we'll be creating it in the upcoming steps).

Rules live in a pack's `rules` directory and are defined as YAML metadata files.

Create a new rule file in `/opt/stackstorm/packs/tutorial/rules/write_url_to_index.yaml`:
with following content:

``` yaml
---
name: "write_url_to_index"
description: "Write the APOD URL to the etc/index.html file."
enabled: true

trigger:
  type: "rabbitmq.new_message"
  parameters: {}

action:
  ref: "tutorial.write_html"
  parameters:
    link: "{{ trigger.body }}"

```

-----------
**NOTE**
If you're struggling and just need the answer, simply copy the file from our
answers directory:
```shell
cp /opt/stackstorm/packs/tutorial/etc/answers/rules/write_url_to_index.yaml /opt/stackstorm/packs/tutorial/rules/write_url_to_index.yaml
```
-----------

Next we'll load the rule into the database so that it begins matching messages.

``` shell
st2ctl reload --register-rules
```


## Create the Action to write the tutorial/etc/index.html file

Our action will be a standard action that will leverage a python script to write
the formatted URL to the etc/index.html file.

First we will create our action metadata file
`/opt/stackstorm/packs/tutorial/actions/write_html.yaml` with the
following conent:

``` yaml
---
name: write_html
pack: tutorial
description: "Writes the NASA APOD URL link to a index.html as a hyperlink"
runner_type: "python-script"
enabled: true
entry_point: write_html.py
parameters:
  link:
    type: string
    description: "The URL for the NASA Astronomical Picture of the Day."
```

-----------
**NOTE**
If you're struggling and just need the answer, simply copy the file from our
answers directory:
```shell
cp /opt/stackstorm/packs/tutorial/etc/answers/actions/write_html.yaml /opt/stackstorm/packs/tutorial/actions/write_html.yaml
```
-----------

Next we will create our python script
`/opt/stackstorm/packs/tutorial/actions/write_html.py`
with the following content:

``` python
#!/usr/bin/env python
#
# Description:
#   a stackstorm action that takes a link string and formats as a hypelink and
#   writes to the /etc/index.html.
# Author:
#   Rick Kauffman wookieware.com
import os
import json
import requests
from st2common.runners.base_action import Action


class WriteHtml(Action):

    def run(self,link):
        if link is not None:
            # write to a index file
            file1=open("/opt/stackstorm/packs/tutorial/etc/index.html","a")
            line = "<p><a href="+link+">"+link+"</a></p>\n"

            file1.write(line)
            file1.close()

        else:
            error = 'Failed to write link to index file'
            return error
        return link
```

-----------
**NOTE**
If you're struggling and just need the answer, simply copy the file from our
answers directory:
```shell
cp /opt/stackstorm/packs/tutorial/etc/answers/workflows/write_html.py /opt/stackstorm/packs/tutorial/actions/write_html_py
```
-----------

Next we'll tell StackStorm about our action, so that our rule can invoke it:

``` shell
st2ctl reload --register-actions
```


### Testing our Action

Post another message

```shell
st2 run tutorial.nasa_apod_rabbitmq_publish
```

Check to ensure our action executed: **Note** remember you can use the GUI ....and the **force**!

``` shell
$ st2 rule-enforcement list --rule tutorial.write_url_to_index
+--------------------------+--------------------+---------------------+-------------------+---------------------+
| id                       | rule.ref           | trigger_instance_id | execution_id | enforced_at              |
+--------------------------+--------------------+---------------------+-------------------+---------------------+
| 5b5dd288587be00afa97914c | tutorial.write_html| 5b5dd287587be00afa9 | 5b5dd288587be00afa | 2018-07-29T14:43:1 |
|                          |                    | 79147               | 97914a             | 9.870669Z          |
+--------------------------+--------------------+---------------------+--------------------+--------------------+
```

Check the rule-enforcement

``` shell
$ st2 rule-enforcement get 5b5dd288587be00afa97914c
+---------------------+---------------------------------+
| Property            | Value                           |
+---------------------+---------------------------------+
| id                  | 5b5dd288587be00afa97914c        |
| rule.ref            | tutorial.write_url_to_index     |
| trigger_instance_id | 5b5dd287587be00afa979147        |
| execution_id        | 5b5dd288587be00afa97914a        |
| failure_reason      |                                 |
| enforced_at         | 2018-07-29T14:43:19.870669Z     |
+---------------------+---------------------------------+

```

Check the tutorial/etc/index.html: You should see at least one link to the HASA APOD picture.
