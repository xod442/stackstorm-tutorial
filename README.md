# StackStorm tutorial pack

This pack provides resources for a high-level tutorial on several key features
in [StackStrom](https://stackstorm.com/). For in-depth details, please visit
the excellent [StackStorm documentation](https://docs.stackstorm.com/) page.

## Prep Instructions

You will need a workstation:

You can follow these steps outlined [This Guide](https://www.wookieware.com/st2.PPTX). Clicking this link
will download the guide.

## Tutorial

In this tutorial we will build a stackstorm action that will get the Astronomical Picture of the Day (apod)
from a nasa website. Once we get the data from the nasa server we will assign it to a local variable and
post a message in the rabbitmq bus.

To do this we will load the rabbitmq pack and test writing messages to it.

Finally we will write a sensor that monitors the rabbitmq looking for new messages, if found, we will
call another stackstorm action to write the link to an html index file.

If you find any problems or bugs in this tutorial, please leave me an issue on github at:
[My Github Repo](https://github.com/xod442/stackstorm-tutorial)

0. [Initialization](doc/00_init.md)
1. [Script Actions](doc/01_actions_script.md)
2. [Native Python Actions](doc/02_actions_native.md)
3. [Packs](doc/03_packs.md)
4. [Context](doc/04_context.md)
5. [Workflows](doc/05_workflows.md)
6. [Event Driven Automation](doc/06_event_driven.md)
