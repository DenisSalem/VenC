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

Pour une installation plus facile vous pourriez vouloir utiliser pip

__Python-Markdown__
Vous pouvez jeter un oeil à la [page officiel](https://pythonhosted.org/Markdown/index.html) ou directement tapez la commande _pip install markdown_ dans un terminal en étant root.

