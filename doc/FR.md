![](https://raw.githubusercontent.com/DenisSalem/VenC/master/doc/logo.png "")

1. [Présentation](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#pr%C3%A9sentation)
2. [Installation](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#installation)
3. [Désinstallation](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#désinstallation)
4. [Prise en main](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#prise-en-main)
  1. [Arborescence](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#arborescence)
  2. [Structure des fichiers](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#structure-des-fichiers)
    1. [Fichier de configuration principal](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#fichier-de-configuration-principal)
    2. [Les Templates](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#les-templates)
    3. [Les Publications](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#les-publications)
    4. [Les Thèmes](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#les-thèmes)
  3. [Pattern Processor](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#pattern-processor)
    1. [Motifs de Templates](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#motifs-de-templates)
    2. [Motifs Super Globaux](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#motifs-super-globaux)
    3. [Motifs de Publications](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#motifs-de-publications)
    4. [Motifs Spéciaux](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#motifs-sp%C3%A9ciaux)
  4. [Variables d'environnement](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#variables-denvironnement)
    1. [blog_configuration.yaml](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#blog_configurationyaml)
    2. [Variables de motifs](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#variables-de-motifs)
  5. [Commandes](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#commandes)
    1. [Afficher la version de VenC](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#afficher-la-version-de-venc)
    2. [Nouveau Blog](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#nouveau-blog)
    3. [Nouvelle publication](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#nouvelle-publication)
    4. [Exporter le blog](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#exporter-le-blog)
6. [Astuces](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#astuces)
7. [Thèmes](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#thèmes)
  1. [Installation](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#installation-1)
  2. [Greffons](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#greffons)
    1. [Défilement infini](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#d%C3%A9filement-infini)
    2. [Moteur de recherche côté client](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#moteur-de-recherche-c%C3%B4t%C3%A9-client)

# Présentation

VenC est une application python conçue pour linux et similaire à [Octopress](http://octopress.org)/[Jekyll](http://jekyllrb.com) pour gérer et créer vos blogs statiques via la console. Avec VenC, tout est fichier texte, pas de base de données. La configuration de chaque blog repose sur un unique et petit fichier Yaml, les thèmes consistent en une poignée de templates HTML à modifier ou créer soi même, les publications quant à elles, se présentent sous la forme d'une partie YAML et d'une autre Markdown.

Les blogs statiques sont tout à fait adaptés aux darknets ou ceux qui veulent un contrôle total sur leur site sans s'embarrasser de CMS lourds et potentiellement vulnérables en terme de sécurité. Par ailleurs, l'extrême simplicité de l'organisation des sources des blogs issues de VenC garantit une prise en main rapide et efficace.

En outre, voilà ce que VenC propose:

- Création de blog statique (HTML/CSS ).
- Mise en page simple à personnaliser directement en HTML/CSS.
- Possibilité de créer un agencement en nombre arbitraire de colonne ( comme sur mon site ).
- Module de défilement infinie simple et facile à mettre en oeuvre ( comme sur mon site ).
- Les publications peuvent être organisées par catégories et sous catégories.
- Les publications peuvent être organisées par période de dates.
- Publication chronologique ascendante ou descendante.
- Flux RSS pour chaque fils de publications.
- Permaliens.
- Gestion et édition du blog entièrement en ligne de commande.
- VenC est conçu pour GNU/Linux spécifiquement.
- Rédaction des publications en markdown.

# Installation

En premier lieu il convient de s'assurer que python 3.x est installé. VenC a également des dépendances qu'il faut satisfaire:

_Pour une installation plus facile vous pourriez vouloir utiliser pip. Cependant, n'utilisez surtout pas pip en étant root, vous risqueriez de casser votre système._

__Python-Markdown__
Vous pouvez jeter un oeil à la [page officielle](https://pythonhosted.org/Markdown/index.html) ou directement tapez la commande _pip install markdown_ dans un terminal.

__PyYaml__
Vous pouvez jeter un oeil à la [page_officielle](http://pyyaml.org/) ou directement taper la commande _pip install pyyaml_ dans un terminal.

Ceci étant fait, clonez le repository de VenC

`git clone https://github.com/DenisSalem/VenC`

Déplacez vous à présent dans le répertoire de VenC

`cd VenC`

Puis lancez le script d'installation en étant root.

`./install.sh`

Voilà, VenC est normalement correctement installé sur votre système.

# Désinstallation

Dans le cas peu probable où vous voudriez supprimer VenC de votre système tapez successivement les commandes suivantes dans un
terminal en étant root

`rm -rfv /usr/lib/python< votre version >/VenC`

`rm -rfv /usr/share/VenC`

`rm -v /usr/bin/venc`

# Prise en main

1. [Arborescence](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#arborescence)
2. [Structure des fichiers](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#structure-des-fichiers)
3. [Pattern Processor](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#pattern-processor)
4. [Variables d'environnement](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#variables-denvironnement)

## Arborescence

Lorsque vous créez un nouveau projet, VenC produit un certain nombre de répertoires. La racine du projet porte le nom du blog, par exemple, "MooFooBar". Ce répertoire en contient cinq autres.

* __blog__: Le dossier où est exporté le projet.
* __extra__: Un dossier contenant des ressources quelquonques copiées vers __blog/__ au moment de l'exportation.
* __entries__: Contient toutes les publications sous forme de fichiers texte numérotés et datés.
* __theme__: Contient les templates html, les feuilles de style et éventuellement les scripts JS.
* __templates__: Contient des modèles vierges de publication.

![](https://github.com/DenisSalem/VenC/raw/master/doc/folders.png "")

## Structure des fichiers

1. [Fichier de configuration principal](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#fichier-de-configuration-principal)
2. [Les Templates](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#les-templates)
3. [Les Publications](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#les-publications)
4. [Les Thèmes](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#les-thèmes)

### Fichier de configuration principal

__blog_configuration.yaml__

![](https://raw.githubusercontent.com/DenisSalem/VenC/master/doc/blog_configuration.png "")

Il s'agit d'un document Yaml à la racine du projet définissant les propriétés du blog, comme son titre, le nom de son auteur, ainsi que des détails fonctionnels comme le nombre de publications par pages ou l'ordre d'affichage de celles-ci. Immédiatement après avoir créé votre blog, il s'agira sans doute du premier fichier que vous éditerez. Après avoir rempli ces champs dont l'usage est détaillé ci-dessous, vous n'aurez normalement plus besoin d'y retoucher.


* __blog_name__ : Sans surprise, il s'agit du titre de votre blog.
* __textEditor__ : L'éditeur de texte choisi pour éditer une nouvelle publication du blog.
* __date_format__ : "%A %d. %B %Y" par défaut. Définit le format de date utilisé à l'intérieur du blog. Le format des dates est en fait le même que celui utilisé par python. Pour en savoir plus sur ce format rendez vous [ici](http://strftime.org).
* __author_name__: Le nom de l'administrateur ou l'auteur du blog.
* __blog_description__ : Un très court résumé de ce dont parle votre site.
* __blog_keywords__ : Les mots clefs associés au site.
* __author_description__ : Un court texte à propos de l'auteur du blog.
* __license__ : La licence appliquée au contenu de votre site.
* __url__ : L'url du blog. Peut être laissée vide, selon le thème utilisé.
* __blog_language__ : Définit la langue du site.
* __email__ : Votre adresse e-mail.
* __entries_per_pages__ : "10" par défaut. Définit évidemment le nombre de publications par page.
* __columns__ : "1" par défaut. Ce champ définit le nombre de colonnes dans une page.
* __rss_thread_lenght__ : "5" par défaut. Définit le nombre de publications à afficher dans le flux RSS.
* __thread_order__ : "latest first" par défaut. Définit l'ordre de publication. Du plus anciens au plus récent, ou l'inverse. Ce champ peut prendre comme valeur soit "oldest first", soit "latest first".
* __path__ : Il s'agit d'une variable contenant différents chemins, vous ne devriez normalement pas avoir besoin d'y toucher. La liste de ces chemins est détaillé ci-dessous
* __index_file_name__ : "index{page_number}.html" par défaut. Le nom de fichier formaté des pages du fil principal de publications. Devrait toujours contenir la variable {page_number}.
* __category_directory_name__ : "{category}" par défaut. Définit le répertoire où sera exporté un fil de publication spécifique à une catégorie de publication. Ce champ devrait donc toujours contenir la variable {category}.
* __dates_directory_name__ : "%Y-%m" par défaut. Définit le format de date utilisé pour les noms de répertoires de fils de publications associés à des dates. Le format des dates est en fait le même que celui utilisé par python. Pour en savoir plus sur ce format rendez vous [ici](http://strftime.org).
* __entry_file_name__ : "entry{entry_id}.html" par défaut. Définit le nom de fichier d'une publication unique. Ce champ devrait toujours contenir la variable {entry_id}.
* __rss_file_name__ : "feed.xml" par défaut. Définit le nom de fichier du flux rss.

### Les Templates

Un template est en fait une publication vierge qui a cependant été préformatée pour contenir des informations souvent utilisées pour lesquels on ne veut pas perdre du
temps à réécrire ou mettre en forme. Un fichier template contient donc des [motifs](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#motifs-de-templates)
pouvant être interprétés. Il n'y a pas de template par défaut, c'est à l'utilisateur de créer les siens. Lorsqu'aucun template n'est utilisé VenC produit une publication
totalement vierge.

### Les Publications

Une publication est un fichier similaire à un template mais dont le propos est d'être remplit par l'utilisateur manuellement en y rédigeant le contenu désiré.
Cela peut-être un billet d'humeur, un article de fond, une galerie d'image, etc. Pour faciliter l'édition de votre blog avec VenC vous êtes fortement encouragé à utiliser des
templates.

Une publication contient un premier partie au format [Yaml](http://yaml.org) contenant les métadonnées de la publication, puis une seconde au format [Markdown](https://daringfireball.net/projects/markdown/) qui elle contiendra la publication à proprement parler.

Finalement une publication vierge se présente de la façon suivante:

![](https://github.com/DenisSalem/VenC/blob/master/doc/newEntryFR.png?raw=true "")

On a donc trois champs à compléter, ou pas.

- __authors__ : C'est la liste des auteurs de la publication, séparés par une virgule. Pas exemple _Denis Salem, Benjamin Bayard, Richard Stallman_.
- __categories__ : C'est la liste des categories de la publication, séparées par une virgule. Vous pouvez également avoir des sous categories pour une publication qui définiront ensuite un arbre de categories. Pour définir une sous catégories il faut séparer la categorie parente de la categorie fille par ' > '. Ce procédé peut-être répété autant de fois que nécessaire. Par exemple _Metal > Copper, Metal > Steel > Properties, Materials_.
- __entry_name__ : C'est le nom de votre publication tel que vous l'avez définit au moment de créer la publication avec `venc -ne <titre de la publication>`.
- __tags__ : C'est la liste des mots clefs de la publication, séparées par une virgule. Par exemple _Libre, Open-source, Linux_.


Les deux parties sont séparées par trois tirets (ceux du six). Sur la capture d'écran la partie contenant la syntaxe Markdown est vide. On parle bien d'une publication vierge.

Notons également que le nom de fichier d'une publication est formaté d'une façon particulière.

`<id>__<mois>-<jour>-<année>-<heure>-<minute>__<titre>`

Pour créer une nouvelle publication rendez vous [ici](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#nouvelle-publication)


### Les Thèmes

Un thème est l'ensemble des fragments qui seront assemblés et interprétés par VenC pour former votre blog, c'est dans un thème que sera définie la mise en page de votre site.
Typiquement, un thème est un repertoire contenant au moins le dossier __chunks__ et un autre, optionel __assets__.

- __assets__ : Contient des ressources nécessaires à la mise en page ou au fonctionnement du blog. Cela peut-être des images, des feuilles de style CSS ou des script JS. Vous pouvez également y entreposer des librairies comme JQuery ou bootstrap.

- __chunks__ : Doit contenir les fichiers suivant
  - header.html
  - entry.html
  - footer.html
  - rssHeader.html
  - rssEntry.html
  - rssFooter.html

Comme vous l'avez sans doute compris VenC met bout à bout les morceaux de votre blog en formattant l'entête (header.html) et en répétant un certain nombre de fois l'operation qui consiste à formater le morceau qui définit une publication (entry.html) pour la publication courante. La page courante est alors terminée en y ajoutant le morceau pied de page (footer.html) également formatté.

C'est exactement le même principe pour le flux RSS qui est construit de façon identique.

Il n'est pas forcément évident de créer un thème de toute pièce et vous n'avez peut-être pas envie de perdre trop de temps à tester le fonctionnement de tout ça. Le meilleur
moyen de créer un thème soi même c'est de jeter un oeil au thème [dummy](https://github.com/DenisSalem/VenC/tree/master/src/share/themes/dummy). Ce thème en l'état n'est pas
utilisable, mais c'est une solide base pour créer le votre. Le style CSS reste à définir, et vous pourriez vouloir réorganiser les éléments de la page. Si vous avez déjà installé VenC sur votre système vous pourrez trouver ce thème dans 

`/usr/share/VenC/themes/dummy`

Une autre approche est de regarder comment sont construits d'autres thèmes. Ceux là seront ajoutés au fur et à mesure sur le repository github de VenC.

Vous pouvez également vous aider de la partie [Astuces](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#astuces) dans laquelle sont décrites
des techniques pour réaliser des mises en pages très spécifiques et pour lesquelles l'utilisation peut-être un peu obscure des motifs de VenC sera illustrée.

## Pattern Processor

1. [Motifs de Templates](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#motifs-de-templates)
2. [Motifs Super Globaux](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#motifs-super-globaux)
3. [Motifs de Publications](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#motifs-de-publications)
4. [Motifs Spéciaux](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#motifs-spéciaux)

VenC utilise un moteur de reconnaissance de motif permettant une mise en page facilitée et automatisée. Ce système devrait permettre dans de futures versions d'utiliser des modules externes. La création et l'ajout de greffons sera détaillé dans une autre partie.

_Les motifs pouvant être reconnus dépendent du contexte dans lequel ils sont trouvés._

Les motifs sont définis de la façon suivante dans VenC

* Chaque motifs commence par '.:'
* Chaque motifs se termine par ':.'
* Le ou les séparateurs à l'intérieur d'un motif sont représentés par '::'

Un motif est une fonction pouvant prendre des paramètres. L'objectif est de remplacer un motif par une chaine de caractères formatée. Typiquement, les motifs
permettent d'accéder aux données du blog ou de faire de la mise en page spécifique pour faire, par exemple, un menu déroulant, ou une barre de navigation.

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

À ces motifs s'ajoutent les super globaux généralement disponibles quelque soit le contexte.

### Motifs Super Globaux

Ces motifs sont généralement disponibles quelque soit le contexte et sont définis
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

* __.:Get::EntryUrl:.__ : Permet de récuper le permalien de la publication.
* __.:Get::EntryContent:.__ : Permet de récuper le corps de la publication.
* __.:Get::EntryDate:.__ : Permet de récuper la date de la publication formatée.
* __.:Get::EntryDateUrl:.__ : Permet de récuper le chemin de la période correspondant à la date de la publication.

### Motifs spéciaux

Il est possible dans certains cas d'accéder à des données itérativement, quand celles-ci se présentent sous la forme d'une liste ou d'un arbre

* __.:For:: liste :: blah blah {0[item]} blah :: séparateur :.__ : Permet d'itérer à travers une liste. 
* __.:RecursiveFor:: arbre :: ouverture :: blah {0[item]} blah blah :: séparateur :: fermeture :.__ : Permet d'itérer à travers un arbre, un type particulier de liste.

Notons qu'en général le second paramètre pour la fonction _For_ est en fait du texte libre, pour accéder à l'item de l'itération courante on utilise la variable de contexte {0[item]}.
Idem pour le troisième paramètre, le séparateur. Le séparateur permet d'insérer du texte après le texte libre de l'itération courante.

De façon identique, pour la fonction _RecursiveFor_, le second, le quatrième et cinquième paramètre constituent du texte libre.

* __.:GetPreviousPage:: texte libre :.__ : Quand appelé dans un fil d'exportation, ce motif permet de récupérer l'url de la page précédente, si elle existe. Pour accéder à l'url de la page précédente utilisez la variable contextuelle __{0[destinationPageUrl]}__ à l'intérieur du texte libre.
* __.:GetNextPage:: texte libre :.__ : Quand appelé dans un fil d'exportation, ce motif permet de récupérer l'url de la page suivante si elle existe. Pour accéder à l'url de la page suivante utilisez la variable contextuelle __{0[destinationPageUrl]}__ à l'intérieur du texte libre.
* __.:PageList:: taille :.__ : Permet de récupérer une liste des publications antérieurs et postérieurs à la publication. La taille de cette liste est determinée par __taille__, qui doit être un nombre entier.
* __.:IfInThread:: text libre :.__ : Motif conditionnel qui permet d'afficher le texte libre ou non selon que l'on se trouve dans un fil de publication ou sur une publication. Cela permet par exemple d'avoir une mise en page particulière pour une publication unique et pour un fil de publications.

## Variables d'environnement

1. [blog_configuration.yaml](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#blog_configurationyaml)
2. [Variables de motifs](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#variables-de-motifs)

### blog_configuration.yaml

Comme dans d'autres contextes de VenC. Le fichier de configuration du blog fait appel à des variables d'environnnement, dont l'utilisation est détaillée ci-dessous.

* __{page_number}__ : Définit le numéro de la page courante.
* __{category}__ : Définit la categorie courante de publication.
* __{entry_id}__ : Définit l'id de la publication courante.

### Variables de motifs

Il existe également des variables particulières sous la forme de listes. Ces variables peuvent être parcourues itérativement et récursivement pour en extraire le contenu et le mettre en forme. Cette extraction se fait grace aux motifs spéciaux _For_ et _RecursiveFor_ dont le fonctionnement est détaillé dans la partie [Motifs Spéciaux](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#motifs-spéciaux). Mais avant voici les listes disponibles:

* __EntryTags__ : La liste de mot clefs de la publication courante. Pour accéder au mot clé de l'itération courante utilisez la variable contextuelle {0[tag]}.
* __EntryAuthors__ : La liste des auteurs de la publication courante. Pour accéder à l'item courant utiliser la variable de contexte {0[author]}.
* __BlogDates__ : La liste des liens vers les publications groupées par dates tel que défini dans [blog_configuration.yaml](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#fichier-de-configuration-principal). Il y a plusieurs items disponibles pour une itération courante; __{0[date]}__, __{0[dateUrl]}__. Respectivement la période tel que formatée dans [blog_configuration.yaml](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#fichier-de-configuration-principal) et le chemin vers le repertoire associé à cette période.

On arrive maintenant au cas particulier des categories. Les categories forment un arbre comme illustré ci-dessous

![](https://raw.githubusercontent.com/DenisSalem/VenC/master/doc/treesFR.png "")

Plus bas on désigne par "_feuille_" l'extrémité d'une branche, une "_branche complète_" désigne le chemin complet depuis la racine d'un arbre jusqu'à une feuille de cette arbre.

* __EntryCategories__ : La liste des categories (branche complète) de la publication courante. Se présente sous la forme de listes imbriquées. Il y a plusieurs items disponibles pour une itération courante; __{0[relativeOrigin]}__, __{0[categoryPath]}__ et __{0[item]}__. Respectivement le chemin relatif de la page courante vers la racine du blog, le chemin relatif vers la sous-categorie courante et le nom de la sous-categorie courante.
* __EntryCategoriesTop__ : La liste des categories (feuilles) de la publication courante. Il y a plusieurs items disponibles pour une itération courante; __{0[relativeOrigin]}__, __{0[categoryLeaf]}__ et __{0[categoryLeafUrl]}__. Respectivement le chemin relatif de la page courante vers la racine du blog, le nom de la categorie feuille et l'url vers la categorie feuille.
* __BlogCategories__ : La liste des categories (branche complète) du blog. Se présente sous la forme de listes imbriquées. Il y a plusieurs items disponibles pour une itération courante ; __{0[relativeOrigin]}__, __{0[categoryPath]}__ et __{0[item]}__. Respectivement le chemin relatif de la page courante vers la racine du blog, le chemin relatif vers la sous-categorie courante et le nom de la sous-categorie courante.

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

Vous ne pouvez pas créer un blog sans en spécifier le nom. Une fois que vous avez créé votre blog, la première chose à faire est en général d'éditer le fichier __blog_configuration.yaml__. Pour en savoir plus sur ce fichier de configuration, rendez vous [ici](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#fichier-de-configuration-principal).

## Nouvelle publication

`$ venc -ne "<nom de la publication>" [nom du template]`

Pour créer une nouvelle publication vous __devez__ être dans le répertoire de votre blog.

Vous ne pouvez pas créer une publication sans spécifier le titre de celle-ci.

Si vous ne spécifiez pas de nom de template, VenC produira une publication totalement vierge. Le nom de template est en fait le nom de fichier du template désiré se trouvant dans le répertoire __templates__.

À l'issue de cette commande VenC essaiera d'ouvrir la nouvelle publication avec l'éditeur de texte spécifié dans le fichier de configuration principal __blog_configuration.yaml__.

## Exporter le blog

`$ venc -xb`

Pour exporter votre blog vous __devez__ être dans le répertoire de votre blog.

Dans celui-ci se trouve un répertoire sobrement intitulé blog. C'est dans ce repertoire que ce sera exporté votre site. Une fois l'exportation terminée vous pouvez copier le contenu de ce répertoire vers votre serveur.

Pour en savoir plus sur l'arborescence rendez vous [ici](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#arborescence).

# Astuces

À compléter

# Thèmes

1. [Installation](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#installation-1)
2. [Greffons](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#greffons)

## Installation

Pour installer un thème sur votre blog copiez le répertoire __chunks__ et __assets__ (si ce dernier existe) dans le sous répertoire __theme__ de votre blog.

## Greffons

1. [Défilement infini](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#d%C3%A9filement-infini)
2. [Moteur de recherche côté client](https://github.com/DenisSalem/VenC/blob/master/doc/FR.md#moteur-de-recherche-c%C3%B4t%C3%A9-client)

### Défilement infini

Il s'agit d'un script AJAX qui va automatiquement charger le contenu des pages suivantes dans la page courante. Ce module est idéal pour les galeries d'images, par exemple.
Pour installer ce module il suffit de copier

`VenC-Infinite-Scroll-<version>.js`

depuis

`/usr/share/VenC/themes/dummy/assets

dans 

`<blog>/themes/assets`

Puis ajoutez dans __header.html__ 
    
`<script type="text/javascript" src=".:Get::RelativeOrigin:.VenC-Infinite-Scroll-<version>.js"></script>`

Voilà, maintenant la magie opère. Attention cependant. Assurez vous que les contraintes suivantes sont respectées dans votre thème.

- L'élément contenant votre publication doit avoir le nom de classe "entry" sinon le module ne parviendra pas à détecter et récupérer les publications de votre blog.
- Vous pouvez avoir une image de chargement n'importe où dans votre page, mais si vous voulez la faire interagir avec le module il doit avoir pour nom d'id "__VENC_LOADING__".
- Vous pouvez vouloir supprimer un élément contenant des liens de navigations, pour cela il faut que cet élément porte le nom d'id "__VENC_NAVIGATION__"

### Moteur de recherche côté client

Non implémenté
