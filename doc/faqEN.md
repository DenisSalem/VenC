![](https://framagit.org/denissalem/VenC/raw/master/doc/logo.png "")

# FAQ

1. [I Get Unknown command](#i-get-unknown-command)

# I get Unknown command

VenC should be installed with [pip](https://pypi.python.org/pypi/pip) in the user side, not in the system. With this way your environment need to be aware of the paths of VenC. For instance, VenC is located in _~/.local/bin_. 

On some linux distribution, like [Archlinux](https://www.archlinux.org/) or [Gentoo](https://www.gentoo.org/), _PATH_ environment variable might be incomplete so indeed, _venc_ is an unknown command.

What you can do is to add an extra path in your environment variable by writing the following at the end of your _~/.bashr_. If the file doesn't exists, juste create it.

> export PATH=$PATH:~/.local/bin
