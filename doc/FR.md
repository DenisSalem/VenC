![](https://raw.githubusercontent.com/DenisSalem/VenC/master/doc/logo.png "")

1. Présentation
2. Installation
3. Prise en main
4. Commandes
5. Thémes

# Présentation

VenC est une application python conçu pour linux et similaire à Octopress/Jekyll pour gérer et créer vos blogs statique via la console. Avec VenC, tout est fichier texte, pas de base de donnée. La configuration de chaque blog repose sur un unique et petit fichier Yaml, les thèmes consistent en une poignée de templates html à modifier ou créer soit même, les publications quant à elles, se présentent sous la forme d'une partie YAML et d'une autre Markdown.

Les blogs statiques sont tout à fait adaptés aux darknets ou ceux qui veulent un controle totale sur leur site sans s'embarrasser de CMS lourd et potentiellement vulnérable en terme de sécurité. Par ailleurs, l'extrême simplicité de l'organisation des sources des blogs issus de VenC garantie une prise en main rapide et efficace.

# Installation

En premier lieu il convient de s'assurer que python 3.x est installé. VenC a également des dépendances qu'il faut satisfaire:

_Pour une installation plus facile vous pourriez vouloir utiliser pip_

__Python-Markdown__
Vous pouvez jeter un oeil à la [page officiel](https://pythonhosted.org/Markdown/index.html) ou directement tapez la commande _pip install markdown_ dans un terminal en étant root.

# Prise en main

1. Arborescence
2. Structure des fichiers
3. Variables d'environnement

## Arborescence

Lorsque vous créez un nouveau projet, VenC produit un certains nombre de répertoire. La racine du projet porte le nom du blog, par exemple, "MooFooBar". Ce répertoire en contient cinq autres.

* __blog__: le dossier où est exporté le projet.
* __extra__: un dossier contenant des ressources quelquonque copiées vers blog/ au moment de l'exportation.
* __entries__: Contient toutes les publications sous forme de fichiers texte numérotés et datés.
* __theme__: Contient les templates html, les feuilles de style et éventuellement les scripts JS.
* __templates__: Contient des modèles vierge de publication.

![](https://github.com/DenisSalem/VenC/raw/master/doc/folders.png "")

## Structure des fichiers

__blog_configuration.yaml__

![](https://raw.githubusercontent.com/DenisSalem/VenC/master/doc/blog_configuration.png "")

Il s'agit d'un document Yaml à la racine du projet définissant les propriétés du blog, comme son titre, le nom de son auteur, ainsi que des détails fonctionnels comme le nombre de publications par pages ou l'ordre d'affichage de celles-ci. Immédiatement après avoir crée votre blog, il s'agira sans doute du premier fichier que vous éditerez. Une fois avoir remplit ses champs dont l'usage est détaillé ci-dessous, vous n'aurez normalement plus besoin d'y retoucher.


* __blog_name__ : Sans surprise, il s'agit du titre de votre blog.
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

* __root__ : "./" par défaut. Le chemins où sera exporté tout le blog à l'intérieur du répertoire blog/.
* __index_file_name__ : "index{page_number}.html" par défaut. Le nom de fichier formaté des pages du fil principale de publication. Devrait toujours contenir la variable {page_number}.
* __categories_directory_name__ : "{category}" par défaut. Définit le répertoire où sera exporté un fil de publication spécifique à une catégorie de publication. Ce champ devrait donc toujours contenir la variable {category}.
* __tags_directory_name__ : "{tag}" par défaut. Définit le répertoire où sera exporté un fil de publication spécifique à un mot clef. Ce champ devrait donc toujours contenir la variable {tag}.
* __authors_directory_name__ : "{author}" par défaut. Définit le répertoire où sera exporté un fil de publication spécifique à un auteur. Ce champ devrait donc toujours contenir la variable {auteur}.
* __dates_directory_name__ : "%Y-%m" par défaut. Définit le format de date utilisé pour les nom de répertoires de fils de publications associés à des dates.
* __entry_file_name__ : "entry{entry_id}.html" par défaut. Définit le nom de fichier d'une publication unique. Ce champ devrait toujours contenir la variable {entry_id}.
* __rss_file_name__ : "feed.xml" par défaut. Définit le nom de fichier du flux rss. 

## Variables d'environnement
Comme dans d'autres contexte de VenC. Le fichier de configuration du blog fait appelle à des variable d'environnnement, dont l'utilisation est détaillé dans la section approprié.
