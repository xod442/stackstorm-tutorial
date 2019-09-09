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

# Learning stackstorm is not easy!!

You are going to need an editor. This training is hands on deep into the workings of stackstorm.
You will have to edit files and examine them. To accomplish this you will need some sort of an editor.

If you have been following along, you can open up a terminal window and install **ATOM**

1. `sudo add-apt-repository ppa:webupd8team/atom`
2. `sudo apt-get update`
3. `sudo apt-get install atom`
4. `cd /opt/stackstorm`
5. `atom .`

![Atom editor - now you can see what youre working on](/img/atom-answers.png)

As we go through this training you have the option of typing out all of the rules, actions and workflows.
If you want to take the short-cut, you can copy from the answer folder to the corresponding stackstorm folder.

# Cheating.....it's OK!
The answers are located in:`/opt/stackstorm/packs/tutorial/etc/answers`
