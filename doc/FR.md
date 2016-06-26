![](https://raw.githubusercontent.com/DenisSalem/VenC/master/doc/logo.png "")

1. [Présentation](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#pr%C3%A9sentation)
2. [Installation](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#installation)
3. [Prise en main](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#prise-en-main)
4. [Commandes](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#commandes)
5. [Thémes](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#th%C3%A9mes)

# Présentation

VenC est une application python conçu pour linux et similaire à Octopress/Jekyll pour gérer et créer vos blogs statique via la console. Avec VenC, tout est fichier texte, pas de base de donnée. La configuration de chaque blog repose sur un unique et petit fichier Yaml, les thèmes consistent en une poignée de templates html à modifier ou créer soit même, les publications quant à elles, se présentent sous la forme d'une partie YAML et d'une autre Markdown.

Les blogs statiques sont tout à fait adaptés aux darknets ou ceux qui veulent un controle totale sur leur site sans s'embarrasser de CMS lourd et potentiellement vulnérable en terme de sécurité. Par ailleurs, l'extrême simplicité de l'organisation des sources des blogs issus de VenC garantie une prise en main rapide et efficace.

# Installation

En premier lieu il convient de s'assurer que python 3.x est installé. VenC a également des dépendances qu'il faut satisfaire:

_Pour une installation plus facile vous pourriez vouloir utiliser pip. Cependant, n'utilisez surtout pas pip en étant root, vous risqueriez de casser votre système._

__Python-Markdown__
Vous pouvez jeter un oeil à la [page officiel](https://pythonhosted.org/Markdown/index.html) ou directement tapez la commande _pip install markdown_ dans un terminal.

__PyYaml__
Vous pouvez jeter un oeil à la [page_officiel](http://pyyaml.org/) ou directement taper la commande _pip install pyyaml_ dans un terminal.

# Prise en main

1. [Arborescence](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#arborescence)
2. [Structure des fichiers](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#structure-des-fichiers)
3. [Pattern Processor](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#pattern-processor)
4. [Variables d'environnement](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#variables-denvironnement)

## Arborescence

Lorsque vous créez un nouveau projet, VenC produit un certains nombre de répertoire. La racine du projet porte le nom du blog, par exemple, "MooFooBar". Ce répertoire en contient cinq autres.

* __blog__: le dossier où est exporté le projet.
* __extra__: un dossier contenant des ressources quelquonque copiées vers blog/ au moment de l'exportation.
* __entries__: Contient toutes les publications sous forme de fichiers texte numérotés et datés.
* __theme__: Contient les templates html, les feuilles de style et éventuellement les scripts JS.
* __templates__: Contient des modèles vierge de publication.

![](https://github.com/DenisSalem/VenC/raw/master/doc/folders.png "")

## Structure des fichiers

1. [Fichier de configuration principal](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#fichier-de-configuration-principal)

### Fichier de configuration principal

__blog_configuration.yaml__

![](https://raw.githubusercontent.com/DenisSalem/VenC/master/doc/blog_configuration.png "")

Il s'agit d'un document Yaml à la racine du projet définissant les propriétés du blog, comme son titre, le nom de son auteur, ainsi que des détails fonctionnels comme le nombre de publications par pages ou l'ordre d'affichage de celles-ci. Immédiatement après avoir crée votre blog, il s'agira sans doute du premier fichier que vous éditerez. Une fois avoir remplit ses champs dont l'usage est détaillé ci-dessous, vous n'aurez normalement plus besoin d'y retoucher.


* __blog_name__ : Sans surprise, il s'agit du titre de votre blog.
* __textEditor__ : L'éditeur de texte choisit pour éditer une nouvelle publication du blog.
* __author_name__: Le nom de l'administrateur ou l'auteur du blog.
* __blog_description__ : Un très cours résumé de ce dont parle votre site.
* __blog_keywords__ : Les mots clefs associés au site.
* __author_description__ : Un cours texte à propos de l'auteur du blog.
* __license__ : La licence appliquée au contenu de votre site.
* __url__ : L'url du blog.
* __blog_language__ : Définit la langue du site.
* __email__ : Votre adresse e-mail.
* __entries_per_pages__ : "10" par défaut. Définit évidément le nombre de publication par page.
* __columns__ : "1" par défaut. Propriété interessante de VenC détaillé plus loin dans la documentation. Ce champ définit le nombre de colunm dans une page.
* __rss_thread_lenght__ : "5" par défaut. Définit le nombre de publication à afficher dans le flux RSS.
* __thread_order__ : "oldest first" par défaut. Définit l'ordre de publication. Du plus anciens au plus récent, ou l'inverse. Ce champ ne peut prendre comme valeur "oldest first" ou "latest first".
* __path__ : Il s'agit d'une variables contenant différents chemins, vous ne devriez normalement pas avoir besoin d'y toucher. La liste de ces chemins est détaillé ci-dessous
* __root__ : "./" par défaut. Le chemins où sera exporté tout le blog à l'intérieur du répertoire _blog_.
* __index_file_name__ : "index{page_number}.html" par défaut. Le nom de fichier formaté des pages du fil principale de publication. Devrait toujours contenir la variable {page_number}.
* __categories_directory_name__ : "{category}" par défaut. Définit le répertoire où sera exporté un fil de publication spécifique à une catégorie de publication. Ce champ devrait donc toujours contenir la variable {category}.
* __tags_directory_name__ : "{tag}" par défaut. Définit le répertoire où sera exporté un fil de publication spécifique à un mot clef. Ce champ devrait donc toujours contenir la variable {tag}.
* __authors_directory_name__ : "{author}" par défaut. Définit le répertoire où sera exporté un fil de publication spécifique à un auteur. Ce champ devrait donc toujours contenir la variable {auteur}.
* __dates_directory_name__ : "%Y-%m" par défaut. Définit le format de date utilisé pour les nom de répertoires de fils de publications associés à des dates.
* __entry_file_name__ : "entry{entry_id}.html" par défaut. Définit le nom de fichier d'une publication unique. Ce champ devrait toujours contenir la variable {entry_id}.
* __rss_file_name__ : "feed.xml" par défaut. Définit le nom de fichier du flux rss. 

## Pattern Processor

VenC utilise un moteur de reconnaissance de motif permettant une mise en page facilitée et automatisée. Ce système permet également d'utiliser des modules externes. La création et l'ajout de greffons sera détaillé dans une autre partie.

_Les motifs pouvant être reconnues dépendent du contexte dans lesquel ils sont trouvé._

Les motifs dans sont définis dans la façon suivante dans VenC

* Chaque motifs commencent par '.:'
* Chaque motifs se terminent par ':.'
* Le ou les séparateurs à l'intérieur d'un motif sont représentés par '::'

## Variables d'environnement

1. [blog_configuration.yaml]()
2. [Templates]()
2. [Super Globaux]()

### blog_configuration.yaml

Comme dans d'autres contexte de VenC. Le fichier de configuration du blog fait appelle à des variable d'environnnement, dont l'utilisation est détaillé ci-dessous.

* __{page_number}__ : Définit le numéro de la page courante.
* __{category}__ : Définit la categorie courante de publication.
* __{tag}__ : Définit le tag courant de publication.
* __{author}__ : Définit l'auteur courant de la publication.
* __{entry_id}__ : Définit l'id de la publication courante.

### Templates

Un template peut contenir un certains nombre de motifs que VenC peut interpréter.

* __.:Get::EntryID:.__ : Retourne l'identifiant unique de la publication.
* __.:Get::EntryName:.__ : Retourne le nom de la publication.
* __.:Get::EntryMonth:.__ : Retourne le mois de création de la publication.
* __.:Get::EntryYear:.__ : Retourne l'année de création de la publication.
* __.:Get::EntryDay:.__ : Retourne le jour de création de la publication.
* __.:Get::EntryHour:.__ : Retourne l'heure de création de la publication.
* __.:Get::EntryMinute:.__ : Retourne la minute de création de la publication.

À ces motifs s'ajoutes les super globaux généralement disponible quelque soit le contexte.

### Super Globaux

Ces motifs sont généralement disponibles quelque soit le contexte et sont définit
dans [blog_configuration.yaml](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#fichier-de-configuration-principal).

* __.:Get::AuthorName:.__ : Retourne le nom de l'auteur du blog.
* __.:Get::BlogName:.__ : Retourne le titre du blog.
* __.:Get::BlogDescription:.__ : Retourne la description du blog.

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

`$ venc -ne <nom de la publication> [nom du template]`

Pour créer une nouvelle publication vous __devez__ être dans le répertoire de votre blog.

Vous ne pouvez pas créer une publication sans spécifier le titre de celle-ci.

Si vous ne spécifiez pas de nom de template, VenC produira une publication totalement vierge.

À l'issu de cette commande VenC essaiera d'ouvrir la nouvelle publication avec l'éditeur de texte spécifié dans le fichier de configuration principal __blog_configuration.yaml__.

## Exporter le blog

`$ venc -xb`

Pour exporter votre blog vous __devez__ être dans le répertoire de votre blog.

Dans celui-ci se trouve un répertoire sobrement intitulé blog. C'est dans ce repertoire que ce sera exporté votre site. Une fois l'exportation terminée vous pouvez copier le contenu de ce répertoire vers votre serveur.

Pour en savoir plus sur l'arborescence rendez vous [ici](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#arborescence).

# Thémes

1. [Installation](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#installation-1)
2. [Greffons](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#greffons)

## Installation

## Greffons

1. [Défilement infini](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#d%C3%A9filement-infini)
2. [Moteur de recherche côté client](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#moteur-de-recherche-c%C3%B4t%C3%A9-client)

### Défilement infini
### Moteur de recherche côté client
