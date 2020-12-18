authors: 'Denis Salem'
categories: ''
tags: ''
title: Foire aux questions
chapter: 7
---VENC-BEGIN-PREVIEW---
---VENC-END-PREVIEW---

## Pourquoi VenC n'est officiellement supporté que par GNU/Linux ?

Et bien c'est très simple camarade, comme dirait Jean-Pierre Coffe, _Les systèmes d'exploitations propriétaires, c'est de la merde !_

## Commande introuvable

VenC devrait être installé avec [pip](https://pypi.python.org/pypi/pip), dans l'environnement Python, côté utilisateur (pas dans le système donc). De cette façon, le système a besoin de connaître l'emplacement de VenC, dont l'exécutable devrait se trouver dans _~/.local/bin_.

Sur certaines distributions GNU/Linux, comme [Archlinux](https://www.archlinux.org/) ou [Gentoo](https://www.gentoo.org/), la variable d'environnement _PATH_ peut être incomplète par défaut, ce qui produit en effet une erreur type _commande introuvable_.

Dans ce cas, vous pouvez ajouter à votre _~/.bashrc_ la ligne suivante :

> export PATH=$PATH:~/.local/bin

Si le fichier n'existe pas déjà cependant, il faudra le créer.

Après ça, tapez dans le terminal actif :

> source ~/.bashrc

Et voilà, ça devrait être bon :)

## Erreurs Python

Normalement VenC gère toutes les erreurs et exceptions de sorte à ne pas interrompre le programme, ou de vous aviser du problème de façon commode.

Si malgré tout vous obtenez des erreurs, c'est probablement que votre installation n'est pas correcte.

Cela arrive lorsque VenC est installé avec la version de Python 2 de [pip](https://pypi.python.org/pypi/pip). VenC fonctionne avec Python 3, il faut donc installer VenC avec pip3.
En général, la version de [pip](https://pypi.python.org/pypi/pip) que vous utilisez par défaut correspond à la version de Python également utilisée par défaut sur votre système.

En particulier sur les système basés sur Debian, vous devrez installer pip3 :

> sudo apt-get install python3-pip

Après ça, désinstallez VenC avec la version Python 2 de [pip](https://pypi.python.org/pypi/pip), et réinstallez VenC avec la version Python 3 de [pip](https://pypi.python.org/pypi/pip).

> pip3 install venc --user

Ça devrait le faire !

## latex2mathml semble incomplet ou ne fonctionne pas correctement.

C'est fort possible en effet, mais ce n'est pas du ressort de VenC dans la mesure où cette fonctionnalité dépend d'une [tierce librairie](https://github.com/Code-ReaQtor/latex2mathml), développée indépendamment de VenC. Cette librairie est jeune et encore en développement. Son développeur étant très réactif, si quelque chose ne fonctionne pas correctement, signalez le problème sur [la page Github du projet](https://github.com/Code-ReaQtor/latex2mathml), cela devrait être alors résolu relativement rapidement !

## Je n'arrive pas à créer de sous-catégories dans ma publication !

Il se peut qu'il s'agisse d'une erreur de syntaxe. Le séparateur de sous-catégorie est " > ", et non pas ">".

Par exemple, vous devriez avoir quelque chose comme :

> categories: 'Acteurs > Jean Rochefort'

Au lieu de  :

> categories: 'Acteurs>Jean Rochefort'

## Les sous-répertoires que j'ai définis ne fonctionnent pas.

Vérifiez qu'aucun de vos sous-répertoires définis manuellement dans *blog_configuration.yaml* ne commence par '/'.

Par exemple :

.:CodeHighlight::Yaml::False::
path:
  category_directory_name: '/{category}' # Incorrect
  archives_directory_name: '%m-%Y' # Correct
  archives_sub_folders: '/' # Incorrect
  categories_sub_folders: '' # Correct
  entries_sub_folders: '{entry_title}' # Correct
:.


## Unsupported locale setting

Si l'environnement système est mal configuré, vous pourriez avoir quelque chose comme ça :

> .:SetColor::denissalem@nonagon::green:. .:SetColor::~/hd_storage/works/VenC/VenC-site $::cyan:. venc -xb;

> .:SetColor::VenC: unsupported locale setting::yellow:.

Cela signifie que vos locales ne sont pas correctement configurées, la résolution de ce problème est spécifique à chaque distribution GNU/Linux.

## Où trouver le code source ?

Sur [Github](https://github.com/DenisSalem/VenC) ou sur [Framagit](https://framagit.org/denissalem/VenC/).
