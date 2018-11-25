#! /usr/bin/python3

#    Copyright 2016, 2018 Denis Salem
# 
#    This file is part of VenC.
#
#    VenC is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    VenC is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with VenC.  If not, see <http://www.gnu.org/licenses/>.

class Messages:
    blog_created = "Votre blog a été crée!"
    theme_installed = "Le thème à bien été installé!"
    entry_written = "La publication a bien été ajouté!"
    file_not_found = "{0} : Ce fichier ou ce dossier n'existe pas."
    file_already_exists = "{0} : {1}: Le fichier existe déjà."
    invalid_entry_filename = "{0} : Nom de fichier invalide pour une publication"
    blog_name = "Nom du blog"
    your_name = "Votre nom"
    blog_description = "Courte description du blog"
    blog_keywords = "Quelques mots clefs qui définissent votre blog"
    about_you = "À propos de vous"
    license = "La licence appliquée à votre contenu"
    blog_url = "L'url du blog"
    blog_language = "La langue du blog"
    your_email = "Votre adresse email"
    missing_params = "{0} : Paramètres manquants."
    cannot_read_in = "{0} : Impossible de lire dans {1}."
    nothing_to_do = "Rien à faire."
    unknown_command = "{0} : Commande inconnue."
    no_blog_configuration = "Le fichier de configuration du blog n'existe pas ou vous n'avez pas les bonnes permissions."
    missing_mandatory_field_in_blog_conf = "Attention, le champ \"{0}\" est manquant dans le fichier de configuration principal du blog."
    username="Nom d'utilisateur: "
    user_passwd="Mot de passe utilisateur: "
    ftp_host="Nom d'hôte FTP"
    ftp_path="Chemin absolu de votre blog sur l'hôte FTP."
    clean_ftp_directory="Nettoyage du repertoire FTP de destination..."
    copy_to_ftp_directory="Copie du blog vers le repertoire FTP de destination..."
    possible_malformed_entry="La publication {0} est probablement mal formée... {1} Abandon."
    possible_malformed_blog_configuration="Le fichier de configuration du blog est probablement mal formée... Abandon."
    blog_recompilation="Recompilation du blog locale..."
    export_single_entries="Exportation locale des publications individuelles..."
    export_archives="Exportation locale des publications triées par dates..."
    export_main_thread="Exportation locale du fil de publications principal."
    export_main_rhread_rss="Exportation locale du flux RSS du fil de publications principal."
    export_categories="Exportation locale des publications triées par categories..."
    export_categories_rss="Exportation locale du flux RSS du fil de publications de la categorie '{0}'."
    missing_mandatory_field_in_entry="Le champ '{0}' dans l'entrée numéro {1} est manquant."
    recursive_for_unknown_value="RecursiveFor: La valeur {0} n'existe pas."
    not_enough_args="Paramétres manquants."
    unknown_pattern="Le motif '{0}' n'existe pas."
    unknown_contextual="La variable contextuel {0} n'existe pas."
    in_ressource="Dans la ressource '{0}'."
    something_goes_wrong_return_empty_string="Une erreur s'est produite. Remplacement pas une chaine de caractère vide."
    arg_blog_name="Nom du blog {0}"
    arg_entry_name="Nom de la publication"
    arg_template_name="Nom du template"
    arg_input_filename="Nom de fichier"
    blog_folder_doesnt_exists="Le dossier de destination n'existe pas... VenC s'en fiche et va en faire un nouveau."
    theme_description_dummy = "Le thème vide. Il donne une bonne base pour concevoir le votre."
    theme_description_gentle = "Thème mono colonne, très clair, aéré et élégant. Idéal pour un blog."
    theme_description_tessellation = "Thème comportant trois colonnes, très clair, aéré et élégant. Idéal pour une galerie."
    theme_doesnt_exists = "{0} : Ce thème n'existe pas."
    unknown_text_editor = "{0} : Éditeur de texte inconnu."
    theme_name = "Nom du thème"
    entry_is_empty = "{0} : Le contenu de la publication est vide."
    missing_entry_content_inclusion="Thème invalide. Il manque l'inclusion du contenu de la publication dans entry.html et/ou rssEntry.html"
    unknown_language="Pygments: {0} : Langage inconnu."
    pre_process="Pré-traitement du théme et des publications..."
    directory_not_copied="Le dossier ne peut être copié. Erreur: %s"
    variable_error_in_filename="Erreur de variable dans le fichier de configuration principal où les chemins et noms de fichier sont définis: {0} n'existe pas."
    wrong_pattern_argument="L'argument '{0}' = '{1}' du motif '{2}' n'est pas correct."
    pattern_argument_must_be_integer="L'argument doit être un entier positif."
    wrong_permissions = "{0} : Vous n'avez pas les bonnes permissions d'accès sur ce fichier."
    unknown_markup_language = "{0}: Langage de balisage non supporté dans {1}."
    tex_math_error = "Chaine mal formé ou balise non supporté par latex2mathml."
    missing_separator_in_entry = "Il manque le séparateur {0}."
    pattern_is_forbidden_here = "Le motif '{0}' n'est pas autorisé ici."
    unknown_provider = "{0} est un fournisseur oembed inconnu."
    connectivity_issue = "Une erreur de connexion est survenue:"
    ressource_unavailable = "{0}: Ressource non disponible."
    response_is_not_json = "{0}: La reponse HTTP n'est pas du JSON."
    server_port_is_invalid = "\"{0}\" n'est pas un numéro de port valide."
    serving_blog = "Serveur actif sur le port : {0}."
    invalid_or_missing_metadata = "\"{0}\": Valeur de meta-donnée invalide ou abstente dans la publication \"{1}\"."
    generating_rss = "Génération du flux RSS..."
    generating_atom = "Génération du flux Atom..."


