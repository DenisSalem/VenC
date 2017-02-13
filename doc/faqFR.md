![](https://framagit.org/denissalem/VenC/raw/master/doc/logo.png "")

# FAQ

1. [Pourquoi VenC n'est officiellement supporté que par Linux](#)
2. [Commande introuvable](#commande introuvable)

## Pourquoi VenC n'est officiellement supporté que par Linux?

Et bien c'est très simple camarade, comme dirait Jean-Pierre Coffe, _Les autres système d'exploitations, c'est de la merde!_

## Commande introuvable

VenC devrait être installé avec [pip](https://pypi.python.org/pypi/pip), dans l'environment python, côté utilisateur (pas dans le système donc). De cette façon le système à besoin de connaître l'emplacement de VenC, dont le l'exécutable devrait se trouver dans _~/.local/bin_.

Sur certaine distribution Linux, comme [Archlinux](https://www.archlinux.org/) et [Gentoo](https://www.gentoo.org/), la variable d'environnement _PATH_ peut être incomplète par défaut, ce qui produit en effet une erreur type _commande introuvable_.

Dans ce cas, vous pouvez ajouter à votre _~/.bashrc_ la ligne suivante:

> export PATH=$PATH:~/.local/bin

Si le fichier n'existe pas déjà cependant, il faudra le créer.


