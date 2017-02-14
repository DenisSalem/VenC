![VenC](http://download.tuxfamily.org/dsalem/img/2017_-_Denis_Salem_-_CC_By_SA_-_VenC-logo.svg "VenC")

# Tutoriels

1. [Installer VenC et créer son blog en moins de 5 minutes!](#installer-venc-et-cr%C3%A9er-son-blog-en-moins-de-5-minutes)
2. [Créer une nouvelle publication](#créer-une-nouvelle-publication)

## Installer VenC et créer son blog en moins de 5 minutes!

Et ouais, c'est possible!

Dabord, il faut installer [pip](https://pypi.python.org/pypi/pip), si ce n'est pas déjà le cas! VenC utilise la version 3 de python, assurez vous donc d'avoir la version de [pip](https://pypi.python.org/pypi/pip) correspondante!

Une fois que c'est fait on install VenC. Pour de vrai.

> pip install venc --user

Vous pouvez maintenant créer votre blog!

> venc --new-blog "MonSuperBlog"

Après cette commande, VenC a créer un répertoire appelé "MonSuperBlog" à l'endroit où vous avez lancé la commande. Ce repertoire contient toutes les informations de votre blog. Il faut donc le garder préciseument, et même en faire des sauvegardes de temps à autres!

La prochaine étape consiste à paramétrer un peu le blog. Pour ça il suffit d'éditer le fichier *blog_configuration.yaml* à la racine de ce repertoire. Vous pourrez notamment y définir le nom de votre blog, sa langue, ses mots clef, etc. Pour plus d'informations sur la configuration du blog, rendez-vous [ici](https://framagit.org/denissalem/VenC/blob/master/doc/FR.md#fichier-de-configuration-principal)

Et voilà, c'est terminé! Votre blog est prêt à l'emploi!

_Si vous avez rencontré une difficulté durant ce tutoriel, jetez un oeil à la [FAQ](https://framagit.org/denissalem/VenC/blob/master/doc/faqFR.md), la solution s'y trouvera certainement!_

## Créer une nouvelle publication

Pour créer une nouvelle publication, placez vous dans le répertoire de votre blog et tapez la commande suivante

> venc --new-entry "Ma Première Publication"

Cette commande crée la publication et la stock dans le repertoire *entries* de votre blog.

__Astuce : L'éditeur de texte par défaut définit dans votre fichier de configuration devrait être _nano_. Quand vous créez une nouvelle publication VenC l'ouvre pour vous dans l'éditeur de texte ainsi définit. Vous pouvez changer votre éditeur de texte dans *blog_configuration.yaml*.__

Une publication vierge ressemble à ça

	CSS: ''
	authors: ''
	categories: ''
	entry_name: Ma Première Publication
	tags: ''
	---

C'est un document découpé en deux parties à l'aide de la ligne _triple tiret du six_

La premiére partie contient les méta-données de la publication au format [yaml](http://www.yaml.org/) et la seconde contient la publication à proprement parler au format [Markdown](https://daringfireball.net/projects/markdown/).

__Astuce : Par défaut VenC utilise la syntax [Markdown](https://daringfireball.net/projects/markdown/), vous pouvez cependant désactiver [Markdown](https://daringfireball.net/projects/markdown/) en ajoutant le champ _doNotUseMarkdown_ à la liste des méta-données du document. Oui, le champ est vide, il n'a pas besoin de valeur particulière.__

Pour en savoir plus sur les méta-données des publications rendez vous [ici](/denissalem/VenC/blob/master/doc/FR.md#les-publications)

La rédaction de la publication se fait dans la seconde partie du document donc, après les trois tiret.

Une fois que vous avez terminé d'écrire le meilleur billet de blog de tous les internets, enregistrez, et c'est finis! Il n'y à plus qu'à publier!






