Challenge Triple A - Dashboard de Monitoring

 Description

Ce projet consiste à créer un dashboard de monitoring système accessible via un serveur web Apache.
Un script Python collecte les informations de la machine (CPU, RAM, processus, fichiers…) et génère automatiquement une page dashboard.html.

Prérequis

Linux (Debian recommandé)
Python 3
Apache2
Modules Python : psutil, distro

Installation

1. Installer Apache2
sudo apt update
sudo apt install apache2

3. Installer les dépendances
pip install psutil distro

Utilisation
Lancer le script
python3 monitor.py

Accéder au dashboard
http://localhost/index.html

Depuis une autre machine :
http://<IP-machine>/dashboard.html

Fonctionnalités

Monitoring CPU
Monitoring RAM 
Infos système
Top processus
Statistiques fichiers




