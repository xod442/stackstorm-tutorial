# Initialization

In this part of the tutorial we're going to login to our StackStorm box,
authenticate with StackStorm and finally install this tutorial pack.

# Objective
![Objective - what success looks like](/img/objective.png)

## Provisioning

If you're doing this at home, you'll need to provision a StackStorm node.
This can be done by getting acces to a clean installation of Ubuntu Mate: (https://ubuntu-mate.org/blog/ubuntu-mate-xenial-final-release/)

To setup your workstation check out the guide here(http://www.wookieware.com/st2-workstation.pptx)

# Using the workstation
Open a terminal window and enter the following command to install a stackstorm server.

In the terminal elevate privileges by using `sudo su -`

At the prompt update Ubuntu with `apt-get update`

Make sure `curl` is up to date with `apt-get install curl`

Now install stackstorm with ` curl -sSL https://stackstorm.com/packages/install.sh | bash -s -- --user=st2admin --password='Ch@ngeMe'`

**NOTE** Please change the password to something you will remember.

## Login

You should now be able to log into stackstorm:
`st2 login -w st2admin` then enter the **password** you used in the install above.

Verify you have logged into stackstorm by issuing `st2 action list`

You should see a list of available stackstorm actions.


**NOTE** This is  **NOT** recommended for production.

## Install the tutorial pack

Next, we want to install this tutorial on the system so we can use the content
in upcoming sections. Packs are simply git repos and can be installed like so:

```shell
st2 pack install https://github.com/xod442/stackstorm-tutorial.git
```

Our code should now be present in: `/opt/stackstorm/packs/tutorial/`

```shell
ls -l /opt/stackstorm/packs/tutorial/
```

You can copy the answers from the answer folder up the the corresponding folder if needed.

The answers are located in:`/opt/stackstorm/packs/tutorial/etc/answers`
