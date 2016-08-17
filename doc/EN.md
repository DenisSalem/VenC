![](https://raw.githubusercontent.com/DenisSalem/VenC/master/doc/logo.png "")

1. [Presentation](https://github.com/DenisSalem/VenC/blob/master/doc/EN.md#presentation)
2. [Installing](https://github.com/DenisSalem/VenC/blob/master/doc/EN.md#installating)
3. [Uninstalling](https://github.com/DenisSalem/VenC/blob/master/doc/EN.md#unsinstalling)
4. [Taking your marks](https://github.com/DenisSalem/VenC/blob/master/doc/EN.md#taking-your-marks)
  1. [File Tree](https://github.com/DenisSalem/VenC/blob/master/doc/EN.md#file-tree)
  2. [Files structure](https://github.com/DenisSalem/VenC/blob/master/doc/EN.md#files-structure)
    1. [Main config file](https://github.com/DenisSalem/VenC/blob/master/doc/EN.md#main-config-file)
    2. [Templates](https://github.com/DenisSalem/VenC/blob/master/doc/EN.md#templates)
    3. [Publications](https://github.com/DenisSalem/VenC/blob/master/doc/EN.md#publications)
    4. [Themes](https://github.com/DenisSalem/VenC/blob/master/doc/EN.md#themes)
  3. [Pattern Processor](https://github.com/DenisSalem/VenC/blob/master/doc/EN.md#pattern-processor)
    1. [Templates Patterns](https://github.com/DenisSalem/VenC/blob/master/doc/EN.md#templates-patterns)
    2. [Over Global Patterns](https://github.com/DenisSalem/VenC/blob/master/doc/EN.md#over-gloabal-patterns)
    3. [Publications Patterns](https://github.com/DenisSalem/VenC/blob/master/doc/EN.md#publications-patterns)
    4. [Special Patterns](https://github.com/DenisSalem/VenC/blob/master/doc/EN.md#special-patterns)
  4. [Environment variables](https://github.com/DenisSalem/VenC/blob/master/doc/EN.md#environment-variables)
    1. [blog_configuration.yaml](https://github.com/DenisSalem/VenC/blob/master/doc/EN.md#blog_configurationyaml)
    2. [Pattern variables](https://github.com/DenisSalem/VenC/blob/master/doc/EN.md#pattern-variables)
  5. [Commands](https://github.com/DenisSalem/VenC/blob/master/doc/EN.md#commands)
    1. [Print VenC's version](https://github.com/DenisSalem/VenC/blob/master/doc/EN.md#print-vencs-version)
    2. [New Blog](https://github.com/DenisSalem/VenC/blob/master/doc/EN.md#new-blog)
    3. [New publication](https://github.com/DenisSalem/VenC/blob/master/doc/EN.md#new-publication)
    4. [Exporting the blog](https://github.com/DenisSalem/VenC/blob/master/doc/EN.md#exporting-the-blog)
6. [Tips](https://github.com/DenisSalem/VenC/blob/master/doc/EN.md#tips)
7. [Themes](https://github.com/DenisSalem/VenC/blob/master/doc/EN.md#themes-1)
  1. [Installing](https://github.com/DenisSalem/VenC/blob/master/doc/EN.md#installing-1)
  2. [Plugins](https://github.com/DenisSalem/VenC/blob/master/doc/EN.md#plugins)
    1. [Infinite scrolling](https://github.com/DenisSalem/VenC/blob/master/doc/EN.md#infinite-scrolling)
    2. [Clientside search engine](https://github.com/DenisSalem/VenC/blob/master/doc/EN.md#clientside-search-engine
# Presentation

VenC is a python application written for linux and similar to Octopress/Jekyll to create and administrate your static blogs using the commandline. Using VenC, everything is text file, no database. Every blog's configuration is based on one unique and small Yaml file, themes consist in a handful of HTML templates to modify or to create yourself, on publications' side, they have one YAML part and one Markdown part.

Static blogs are fully adapted for darknets or for those who want a full control on their website without having to deal with heavy and potentially vulnerables CMS in security matter. Moreover, the extreme simplicity of the organisation of blogs' sources outcome from VenC guaranties a fast and efficient handling.

# Installing

First of all, you should verify that python 3.x is installed. VenC also has dependances that we need to satisfy:

_For an easier installation, you may want to use pip. However, don't use pip as root, you may break your system._

__Python-Markdown__
You can take a peak at the [official page](https://pythonhosted.org/Markdown/index.html) or just type in _pip install markdown_ in a terminal.

__PyYaml__
You can take a peak at the [official page](http://pyyaml.org/) or just type in _pip install pyyaml_ in a terminal.

Having this done, clone the VenC repository

`git clone https://github.com/DenisSalem/VenC`

Change directory to VenC's

`cd VenC`

Then start the installation script as root.

`./install.sh`

Voilà, VenC should be correctly installed on your system.

# Uninstalling

In the not-so-likely-to-happen case where you'd like to uninstall VenC from your system type consecutively the following commands in a root terminal

`rm -rfv /usr/lib/python< yourversion >/VenC`

`rm -rfv /usr/share/VenC`

`rm -v /usr/bin/venc`

# Taking your marks

1. [File Tree](https://github.com/DenisSalem/VenC/blob/master/doc/EN.md#file-tree)
2. [Files structure](https://github.com/DenisSalem/VenC/blob/master/doc/EN.md#files-structure)
3. [Pattern Processor](https://github.com/DenisSalem/VenC/blob/master/doc/EN.md#pattern-processor)
4. [Environmen Variables](https://github.com/DenisSalem/VenC/blob/master/doc/EN.md#environment-variables)

## File Tree

When you create a new project, VenC creates a certain amount of directories. The project's root takes the name of the blog, for example, "MooFooBar". This directory contains five others.

* __blog__: The folder where is exported the blog.
* __extra__: A folder containing whatever ressources copied to __blog/__ when exportating.
* __entries__: Contains every publication in the form of numbered and dated text files.
* __theme__: Contains html templates, stylesheets and optionally JS scripts.
* __templates__: Contains blank publication models.

![](https://github.com/DenisSalem/VenC/raw/master/doc/folders.png "")

## Structure des fichiers

1. [Main config file](https://github.com/DenisSalem/VenC/blob/master/doc/EN.md#main-config-file)
2. [Templates](https://github.com/DenisSalem/VenC/blob/master/doc/EN.md#templates)
3. [Publications](https://github.com/DenisSalem/VenC/blob/master/doc/EN.md#publications)
4. [Themes](https://github.com/DenisSalem/VenC/blob/master/doc/EN.md#themes)

### Main config file

__blog_configuration.yaml__

![](https://raw.githubusercontent.com/DenisSalem/VenC/master/doc/blog_configuration.png "")

It is a Yaml document in the project's root which defines blog's properties, such as it's title, it's author name, or functionnal details such as the number of by page publications or the printing order of those. Immediately after creating your blog, it will probably be the first file you'll edit. After fulfilling those fields (detailed below), you normally won't have to touch it again.


* __blog_name__ : Obviously your blog's name.
* __textEditor__ : Chosen text editor to edit your publications.
* __date_format__ : "%A %d. %B %Y" by default. Défines the date format used within the blog.
* __author_name__: Name of the administrator or author of the blog.
* __blog_description__ : A quick summary of what your site's about.
* __blog_keywords__ : Keywords associated to the website.
* __author_description__ : A short text about the author.
* __license__ : Your content's license.
* __url__ : Blog's URL.
* __blog_language__ : Blog's language.
* __email__ : Your e-mail address.
* __entries_per_pages__ : "10" by default. Obviously defines the per page publications number.
* __columns__ : "1" by default. This field defines the number of columns in a page.
* __rss_thread_lenght__ : "5" by default. Defines the number of publications to print in the RSS feed.
* __thread_order__ : "latest first" by default. Defines the order of publications. Oldest to newest, or the other way around. This field can be set to "oldest first", or "latest first".
* __path__ : A variable containing various paths, you normally shouldn't need to touch it. Those paths list is detailed below.
* __index_file_name__ : "index{page_number}.html" by default. Main thread of publications' fomratted filename. Should always contain the variable {page_number}.
* __category_directory_name__ : "{category}" by default. Defines the directory where will be exported a publication thread specific to a category of publication. This field should always contain the variable {category}.
* __dates_directory_name__ : "%Y-%m" by default. Defines the date format used for directories' names of publications threads associated to dates.
* __entry_file_name__ : "entry{entry_id}.html" by default. Defines the filename of a unique publication. This field should always contain the variable {entry_id}.
* __rss_file_name__ : "feed.xml" by default. Defines the rss feed's filename.

### Templates

A template actually is a blank publication which has been preformatted to contain information informations often used for which we don't want to lose time to rewrite or to shape. So a template file contains [patterns](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#motifs-de-templates)
which can be called. There is no template by default, it up to the user to create theirs. When no template is used VenC creates a fully blank publication.

### Publications

A publication is a file similar to a template but which the purpose is to be filled by the user manually by redacting the desired content.
It can be a mood note, a documented article, an image galery, etc. To ease the edition of your blog with VenC you are strongly encouraged to use
templates.

A publication contains a firts part in [Yaml](http://yaml.org) format contening publication's metadatas, An another one in [Markdown](https://daringfireball.net/projects/markdown/) format which will contain the said publication.

Finaly a blank publication looks like this:


![](https://github.com/DenisSalem/VenC/blob/master/doc/newEntryFR.png?raw=true "")

Les deux partie sont séparé par trois tirets (ceux du six). Sur la capture d'écran la partie contenant la syntax Markdown est vide. On parle bien d'une publication vierge.

Notons également que le nom de fichier d'une publication est formatté d'une façon particulière.

`<id>__<mois>-<jour>-<année>-<heure>-<minute>__<titre>`

Pour créer une nouvelle publication rendez vous [ici](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#nouvelle-publication)

### Les Thémes

Un théme est l'ensemble des fragment qui seront assemblés et interprétés par VenC pour former votre blog, c'est dans un thème que sera définit la mise en page de votre site.
Typiquement, un thème est un repertoire contenant au moins le dossier __chunks__ et un autre, optionel __assets__.

- __assets__ : Contient des ressources nécessaires à la mise en page ou au fonctionnement du blog. Cela peut-être des images, des feuilles de style CSS ou des script JS. Vous pouvez également y entreposer des librairies JQuery ou bootstrap.

- __chunks__ : Doit contenir les fichiers suivant
  - header.html
  - entry.html
  - footer.html
  - rssHeader.html
  - rssEntry.html
  - rssFooter.html

Comme vous l'avez sans doute compris VenC met bout à bout les morceaux de votre blog en formattant l'entête (header.html) et en répétant un certain nombre de fois l'operation qui consiste à formatté le morceau qui définit une publication (entry.html) pour la publication courante. La page courante est alors terminé en y ajoutant le morceau pied de page (footer.html) également formatté.

C'est exactement le même principe pour le flux RSS qui est construit de façon identique.

Il n'est pas forcément évident de créer un théme de toute pièce et vous n'avez peut-être pas envie de perdre trop de temps à tester le fonctionnement de tout ça. Le meilleur
moyen de créer un thème soit même c'est de jeter un oeil au thème [dummy](https://github.com/DenisSalem/VenC/tree/master/src/share/themes/dummy). Ce théme en l'état n'est pas
utilisable, mais c'est une solide base pour créer le votre. Le style CSS reste à définir, et vous pourriez vouloir réorganiser les éléments de la page. Si vous avez déjà installé VenC sur votre système vous pourrez trouver ce thème dans 

`/usr/share/VenC/themes/dummy`

Une autre approche est de regarder comment sont construit d'autres thémes. Ceux là seront ajoutés au fur et à mesure sur le repository github de VenC.

Vous pouvez également vous aider de la partie [Astuces](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#astuces) dans laquelle sont décrites
des techniques pour réaliser des mises en pages très spécifiques et pour laquelle l'utilisation peut-être un peu obscure des motifs de VenC sera illustrées.

## Pattern Processor

1. [Motifs de Templates](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#motifs-de-templates)
2. [Motifs Super Globaux](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#motifs-super-globaux)
3. [Motifs de Publications](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#motifs-de-publications)
4. [Motifs Spéciaux](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#motifs-spéciaux)

VenC utilise un moteur de reconnaissance de motif permettant une mise en page facilitée et automatisée. Ce système devrait permettre dans de futur version d'utiliser des modules externes. La création et l'ajout de greffons sera détaillé dans une autre partie.

_Les motifs pouvant être reconnues dépendent du contexte dans lesquel ils sont trouvé._

Les motifs sont définis de la façon suivante dans VenC

* Chaque motifs commencent par '.:'
* Chaque motifs se terminent par ':.'
* Le ou les séparateurs à l'intérieur d'un motif sont représentés par '::'

Un motif est une fonction pouvant prendre des paramétres. L'objectif est de remplacer un motif par une chaine de caractére formattée. Typiquement, les motifs
permettent d'accéder aux données du blog ou de faire de la mise en page spécifique pour faire, par exemple, un menu déroulant, ou une bar de navigation.

### Motifs de Templates

Pour en savoir plus sur les templates, rendez vous [ici](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#templates)
Un template peut contenir un certains nombre de motifs que VenC peut interpréter.

* __.:Get::EntryID:.__ : Retourne l'identifiant unique de la publication.
* __.:Get::EntryName:.__ : Retourne le nom de la publication.
* __.:Get::EntryMonth:.__ : Retourne le mois de création de la publication.
* __.:Get::EntryYear:.__ : Retourne l'année de création de la publication.
* __.:Get::EntryDay:.__ : Retourne le jour de création de la publication.
* __.:Get::EntryHour:.__ : Retourne l'heure de création de la publication.
* __.:Get::EntryMinute:.__ : Retourne la minute de création de la publication.

À ces motifs s'ajoutent les supers globaux généralement disponibles quelque soit le contexte.

### Motifs Super Globaux

Ces motifs sont généralement disponibles quelque soit le contexte et sont définit
dans [blog_configuration.yaml](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#fichier-de-configuration-principal).

* __.:Get::AuthorName:.__ : Retourne le nom de l'auteur du blog.
* __.:Get::BlogName:.__ : Retourne le titre du blog.
* __.:Get::BlogDescription:.__ : Retourne la description du blog.
* __.:Get::BlogKeywords:.__ : Retourne les mots clefs décrivant le blog.
* __.:Get::AuthorDescription:.__ : Retourne la description de l'auteur du blog.
* __.:Get::License:.__ : Retourne la licence appliquée au contenu du blog.
* __.:Get::BlogUrl:.__ : Retourne l'URL du blog.
* __.:Get::BlogLanguage:.__ : Retourne le language du blog.
* __.:Get::AuthorEmail:.__ : Retourne l'adresse email de l'auteur du blog.

### Motifs de Publications

Une publication peut contenir les mêmes motifs qu'un template. En plus de ceux là s'ajoutent:

* __.:Get::EntryUrl:.__ : Permet de récuper le permaliens de la publication.
* __.:Get::EntryContent:.__ : Permet de récuper le corps de la publication.
* __.:Get::EntryDate:.__ : Permet de récuper la date de la publication formattée.
* __.:Get::EntryDateUrl:.__ : Permet de récuper le chemin de la période correspondant à date de la publication.

### Motifs spéciaux

Il est possible dans certains cas d'accéder à des données itérativement, quand celles-ci se présentent sous la forme d'une liste ou d'un arbre

* __.:For:: liste :: blah blah {0[item]} blah :: séparateur :.__ : Permet d'itérer à travers une liste. 
* __.:RecursiveFor:: arbre :: ouverture :: blah {0[item]} blah blah :: séparateur :: fermeture :.__ : Permet d'itérer à travers un arbre, un type particulier de liste.

Notons qu'en général le second paramétre pour la fonction _For_ est en fait du texte libre, pour accéder à l'item de l'itération courante on utilise la variable de context {0[item]}.
Idem pour le troisième paramétre, le séparateur. Le séparateur permet d'insérer du texte après le texte libre de l'itération courante.

De façon identique, pour la fonction _RecursiveFor_, le second, le quatriéme et cinquiéme paramétre constituent du texte libre.

* __.:GetPreviousPage:: texte libre :.__ : Quand est appelé dans un fil d'exporation, ce motif permet de récupérer l'url de la page précédente, si elle existe. Pour accéder à l'url de la page précédente utilisez la variable contextuelle __{0[destinationPageUrl]}__ à l'intérieur du texte libre.
* __.:GetNextPage:: texte libre :.__ : Quand est appelé dans un fil d'exporation, ce motif permet de récupérer l'url de la page suivante si elle existe. Pour accéder à l'url de la page suivente utilisez la variable contextuelle __{0[destinationPageUrl]}__ à l'intérieur du texte libre.
* __.:PageList:: taille :.__ : Permet de récupérer une liste des publications antérieurs et postérieurs à la publication. La taille de cette liste est determinée par __taille__, qui doit être un nombre entier.
* __.:IfInThread:: text libre :.__ : Motifs conditionnel qui permet d'afficher le texte libre ou non selon que l'on se trouve dans un fil de publication ou sur une publication. Cela permet par exemple d'avoir une mise en page particulière pour une publication unique et pour un fil de publications.

## Variables d'environnement

1. [blog_configuration.yaml](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#blog_configurationyaml)
2. [Variables de motifs](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#variables-de-motifs)

### blog_configuration.yaml

Comme dans d'autres contexte de VenC. Le fichier de configuration du blog fait appelle à des variable d'environnnement, dont l'utilisation est détaillé ci-dessous.

* __{page_number}__ : Définit le numéro de la page courante.
* __{category}__ : Définit la categorie courante de publication.
* __{entry_id}__ : Définit l'id de la publication courante.

### Variables de motifs

Il existe également des variables particulières sous la forme de listes. Ces variables peuvent être parcourue itérativement et récursivement pour en extraire le contenue et le mettre en forme. Cette extraction se fait grace aux motifs spéciaux _For_ et _RecursiveFor_ dont le fonctionnement est détaillée dans la partie [Motifs Spéciaux](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#motifs-spéciaux). Mais avant voici les listes disponibles:

* __EntryTags__ : La liste de mot clefs de la publication courante. Pour accéder au mot clé de l'itération courante utilisez la variable contextuelle {0[tag]}.
* __EntryAuthors__ : La liste des auteurs de la publication courante. Pour accéder à l'item courant utiliser la variable de contexte {0[author]}.
* __BlogDates__ : La liste des liens vers les publications groupé par dates tel que définit dans [blog_configuration.yaml](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#fichier-de-configuration-principal). Il y a plusieur items disponibles pour une itération courange; __{0[date]}__, __{0[dateUrl]}__. Respectivement la période tel que formatté dans [blog_configuration.yaml](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#fichier-de-configuration-principal) et le chemin vers le repertoire associé à cette période.

On arrive maintenant au cas particulier des categories. Les categories forment un arbres comme illustré ci-dessous

![](https://raw.githubusercontent.com/DenisSalem/VenC/master/doc/treesFR.png "")

Plus bas on désigne par "_feuille_" l'extrémité d'une branche, une "_branche compléte_" désigne le chemin complet depuis la racine d'un arbre jusqu'à une feuille de cette arbre.

* __EntryCategories__ : La liste des categories (branche complète) de la publication courante. Se présente sous la forme de listes imbriquées. Il y a plusieurs items disponibles pour une itération courante; __{0[relativeOrigin]}__, __{0[categoryPath]}__ et __{0[item]}__. Respectivement le chemin relatif de la page courante vers la racine du blog, le chemin relatif vers la sous-categorie courante et le nom de la sous-categorie courante.
* __EntryCategoriesTop__ : La liste des categories (feuille) de la publication courante. Il y a plusieur items disponibles pour une itération courante; __{0[relativeOrigin]}__, __{0[categoryLeaf]}__ et __{0[categoryLeafUrl]}__. Respectivement le chemin relatif de la page courante vers la racine du blog, le nom de la category feuille et l'url vers la category feuille.
* __BlogCategories__ : La liste des categories (branche complète) du blog. Se présente sous la forme de listes imbriqués. Il y a plusieur items disponibles pour une itération courante; __{0[relativeOrigin]}__, __{0[categoryPath]}__ et __{0[item]}__. Respectivement le chemin relatif de la page courante vers la racine du blog, le chemin relatif vers la sous-categorie courante et le nom de la sous-categorie courante.

Pour utiliser ces variables spéciales de motifs reportez vous à la partie [Motifs spéciaux](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#motifs-spéciaux)

# Commandes

1. [Afficher la version de VenC](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#afficher-la-version-de-venc)
2. [Nouveau Blog](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#nouveau-blog)
3. [Nouvelle publication](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#nouvelle-publication)
4. [Exporter le blog](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#exporter-le-blog)

## Afficher la version de VenC

`$ venc -v`

## Nouveau Blog

`$ venc -nb <nom du blog>`

VenC crée le répertoire contenant les sources du blog à l'endroit ou vous tapez la commande.

`$ venc -nb "monSuperBlog"`

`$ cd monSuperBlog`

`$ ls`

`blog  blog_configuration.yaml  entries  extra  templates  theme`

Vous ne pouvez pas créer un blog sans en spécifier le nom. Une fois que vous avez crée votre blog, la première chose à faire est en général d'éditer le fichier __blog_configuration.yaml__. Pour en savoir plus sur ce fichier de configuration, rendez vous [ici](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#fichier-de-configuration-principal).

## Nouvelle publication

`$ venc -ne "<nom de la publication>" [nom du template]`

Pour créer une nouvelle publication vous __devez__ être dans le répertoire de votre blog.

Vous ne pouvez pas créer une publication sans spécifier le titre de celle-ci.

Si vous ne spécifiez pas de nom de template, VenC produira une publication totalement vierge. Le nom de template est en fait le nom de fichier du template désiré se trouvant dans le répertoire __templates__.

À l'issu de cette commande VenC essaiera d'ouvrir la nouvelle publication avec l'éditeur de texte spécifié dans le fichier de configuration principal __blog_configuration.yaml__.

## Exporter le blog

`$ venc -xb`

Pour exporter votre blog vous __devez__ être dans le répertoire de votre blog.

Dans celui-ci se trouve un répertoire sobrement intitulé blog. C'est dans ce repertoire que ce sera exporté votre site. Une fois l'exportation terminée vous pouvez copier le contenu de ce répertoire vers votre serveur.

Pour en savoir plus sur l'arborescence rendez vous [ici](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#arborescence).

# Astuces

À compléter

# Thémes

1. [Installation](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#installation-1)
2. [Greffons](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#greffons)

## Installation

Pour installer un un théme sur votre blog copiez le repertoire __chunks__ et __assets__ (si ce dernier existe) dans le sous répertoire __theme__ de votre blog.

## Greffons

1. [Défilement infini](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#d%C3%A9filement-infini)
2. [Moteur de recherche côté client](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#moteur-de-recherche-c%C3%B4t%C3%A9-client)

### Défilement infini

Il s'agit d'un script AJAX qui va automatiquement charger le contenu des pages suivantes dans la page courante. Ce module est idéale pour les galeries d'images, par exemple.
Pour installer ce module il suffit de copier

`VenC-Infinite-Scroll-<version>.js`

depuis

`/usr/share/VenC/themes/dummy/assets

dans 

`<blog>/themes/assets`

Puis ajoutez dans __header.html__ 
    
`<script type="text/javascript" src=".:Get::RelativeOrigin:.VenC-Infinite-Scroll-<version>.js"></script>`

Voilà, maintenant la magie opère. Attention cependant. Assurez vous que les contraintes suivantes sont respectés dans votre théme.

- L'élément contenant votre publication doit avoir le nom de classe "entry" sinon le module ne parviendra pas à détecter et récupérer les publications de votre blog.
- Vous pouvez avoir une image de chargement n'importe où dans votre page, mais si vous voulez la faire interagir avec le module il doit avoir pour nom d'id "__VENC_LOADING__".
- Vous pouvez vouloir supprimer un élément contenant des liens de navigations, pour cela il faut que cet élément porte le nom d'id "__VENC_NAVIGATION__"

### Moteur de recherche côté client

Non implémenté
