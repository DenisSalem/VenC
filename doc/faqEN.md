![](https://framagit.org/denissalem/VenC/raw/master/doc/logo.png "")

# FAQ

1. [Why VenC is only supported by Linux?](#why-venc-is-only-supported-by-linux)
2. [I Get Unknown command](#i-get-unknown-command)
3. [Python errors](#python-errors)

## Why VenC is only supported by Linux?

That's quite simple my friend, because all other operating systems are crap!

## I get Unknown command

VenC should be installed with [pip](https://pypi.python.org/pypi/pip) in the user side, not in the system. This way your environment need to be aware of the paths of VenC. For instance, VenC is located in _~/.local/bin_. 

On some linux distribution, like [Archlinux](https://www.archlinux.org/) or [Gentoo](https://www.gentoo.org/), _PATH_ environment variable might be incomplete so indeed, _venc_ is an unknown command.

What you can do is to add an extra path in your environment variable by writing the following at the end of your _~/.bashr_. If the file doesn't exists, juste create it.

> export PATH=$PATH:~/.local/bin

## Python errors

It should not happen but if so that's maybe you install VenC the wrong way, because most of the time VenC handle errors and exception nicely.

> AttributeError: 'NoneType' object has no attribute 'split'

What's going on is that your installation was probably done with the python2 version of pip which is wrong for VenC since it's rely on python 3. Since pip use the same version of python setup on your system, that's mean that the default version of python is 2.7. This is often the case on debian based OS.

So what you want to do now is to uninstall venC with pip, the same you used for the installation. Then install the proper version of pip (or try to change the default version of python used on your system), and finaly reinstall VenC with your fresh pip!

For debian system install pip3 this way

> sudo apt-get install python3-pip

and then

> pip3 install venc --user

It should do the trick!
