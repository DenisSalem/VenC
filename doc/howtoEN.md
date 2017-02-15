![VenC](https://download.tuxfamily.org/dsalem/img/2017_-_Denis_Salem_-_CC_By_SA_-_VenC-logo.svg "VenC")

# How to

1. [Install VenC and create your blog in 5 minutes!](#install-venc-and-create-your-blog-in-5-minutes)
2. [Create a new publication](#create-a-new-publication)
3. [Publish](#publish)
4. [Put online](#put-online)

## Install VenC and create your blog in 5 minutes!

That's right!

First you must install [pip](https://pypi.python.org/pypi/pip) if it's not already the case! VenC rely on python 3 so you want to use the version of [pip](https://pypi.python.org/pypi/pip) that match.

Once it's done, we can install VenC. For real.

	pip install venc --user

And that's it! You can now create your blog!

	venc --new-blog "MyAwesomeBlog"

After issue this command VenC create a folder named "MyAwesomeBlog" that hold everything related to your blog. This folder is located in the place where you issue the command. It's strongly advised to take of this folder and even perfom some backup sometimes!

The next step is to setup your blog. It's quick and easy, just edit the file named *blog_configuration.yaml* at the root of the folder of your blog. The main idea there is to define some informations about the blog as well as some options. The configuration file is explained [there](EN.md#main-config-file) so be sure to have a look!

That's it, your done! The blog is ready to use!

_In case your face somes troubles during the process check out the [FAQ](https://framagit.org/denissalem/VenC/blob/master/doc/faqEN.md). No doubt there you'll find a solution!_

## Create a new publication

To create a new publication, set the current working directory to the root of your blog folder and issue the following command

	venc --new-entry "My First Post"

Then your post is created and stored in the *entries* directory located at the root of your blog folder.

__Tips: VenC set the text editor in *blog_configuration* to _nano_ by default. So when you create a new entry it will be opened with the text editor defined this way in your blog configuration file. One may want to change the default text editor to something else.__

So a fresh new entry look's like this

	CSS: ''
	authors: ''
	categories: ''
	entry_name: Ma Première Publication
	tags: ''
	---

It's a document split in two part with the _triple dash_.

The first part of the entry hold metadata describing your entry in [yaml](http://www.yaml.org/). The second part hold the actual content of the entry in [Markdown](https://daringfireball.net/projects/markdown/) syntax.

__Tips: By default VenC parse the content of a publication as a [Markdown](https://daringfireball.net/projects/markdown/) document. It is allowed to disable this feature for the current entry you're writting by adding the field _doNotUseMarkdown_ to the metadatas. Yes, this field is empty, it does not require any particular value.__

To learn more about entry's metadatas check out the related documentation [there](EN.md#publications).

So the writting of the content of your publication is done below the triple dash.

Once you've done the best post of the entire internet and beyond save your entry, then you're ready to publish!

## Publish

So that's it, you wrote one or more entries, and you want to see how beautiful it look's like! Go to the root directory of your blog and issue the following

	venc --export-blog gentle

This will create all the HTML pages of your blog by using the theme known as __*gentle*__. To know which available themes we do have you can issue the following

	venc --themes

Then you can recompile your blog by passing the name of the desired theme, printed in green with the previous command.

You may want to do your own HTML/CSS theme. A good way to achieve that is to use __*dummy*__ as a base. Just copy this theme into your local theme folder known as _theme_. The source of dummy should be located in _~/.local/share/VenC/themes/_.

To recompile the blog with this theme of your own just run

	venc --export-blog

By default, VenC use the local theme located in the root folder of your blog when you do not specify any theme name.

You may want to learn more about themes so be sure to have a look to [this](EN.md#themes).

So now, the content of yout blog is available in _blog_ directory. To have a look, just open in your browser the _index.html_ located in.

There it is! You did it like a rock star!

## Put online

So now everything look's good, you wan't to share your work with the world wide web!

There is many ways to achieve that. You can manually copy all the content of the blog folder to the remote server of your choice. But it might be a little bit anoying since VenC can do it for you.

The first step is to edit *blog_configuration.yaml* so you can define the ftp destination server with the field *ftp_host*, then define the path where the content of your blog will be located in the server with the subfield _ftp_, in _path_.


__Careful: Special attention on the ftp directory that you define. VenC will erase it's content, so be sure about what you're doing!__

After filling the previous you can run

	venc --remote-copy

It will ask for the user and the password of the target ftp server. Once you give the right answer, VenC performs the transfer. Take a coffee and wait a little bit!

You can also recompile and copy the blog online in one commande with

	venc --export-via-ftp [theme]

It will prompt you as well as the previous command.

__Tips: You can pass a theme name to the command above so it will compile the blog with. If none theme are specified it will compile with the local theme.__

Once it's done, congratulation, your blog should be online, spread the news!

