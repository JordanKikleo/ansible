# Configurer et déployer

Sur EC2, se mettre dans le dossier Creation-and-Deployment/configure_device :

bash -e execute_creation.sh num_port

# Flasher une carte SD

- Télécharger la dernière version de l'image Kikleo **backup_image.img.gz**, disponible sur S3 : misc-kikleo/Jetson-images/
- Installer balenaEtcher : https://etcher.balena.io/
- Insérer la carte SD dans l'ordinateur
- "Flash from file" -> Sélectionner l'image kikleo téléchargée
- "Select target" -> Sélectionner la carte sd
- Vérifier que l'espace de stockage de la carte SD (~64.1GB) est plus grande que l'image (~63.9GB)
- Cliquer sur "Flash!"

Un flash peut durer entre 15 min et 1h30

# Créer une image / dupliquer un boitier Jetson Nano

Tutoriel disponible [ici](https://jetsonhacks.com/2020/08/08/clone-sd-card-jetson-nano-and-xavier-nx/)