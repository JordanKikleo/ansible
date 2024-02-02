import sys
import shared
import variables
import requests

# API credentials
api_url = shared.api_url
headers = shared.headers
thingsboard = shared.thingsboard
customer_id_ops = shared.customer_id_ops

# Variables
device_name = variables.device_name
restaurant_name = variables.restaurant_name
device_port = variables.device_port
device_type = variables.device_type

# Configurer un device pour Thingsboard
thingsboard_config = {
    "customerId": {"id": customer_id_ops, "entityType": "CUSTOMER"},
    "name": device_name,
    "type": "Prod - AWS",
    "label": device_port,
}


if __name__ == "__main__":
    print("Configuration du device dans Thingsboard et MongoDB ...")
    try:
        thingsboard_device = thingsboard.create_device(thingsboard_config)
        thingsboard_device.raise_for_status()
        thingsboard_device_id = thingsboard_device.json()["id"]["id"]
        thingsboard_token = thingsboard.get_device_credentials(thingsboard_device_id)

        # Ajouter des server attributs à ce device
        server_attributes = {"inactivityTimeout": 300000}
        create_server_attributes = thingsboard.create_device_attributes(
            thingsboard_device_id, server_attributes, "SERVER_SCOPE"
        )
        create_server_attributes.raise_for_status()

        config = {
            "port": device_port,
            "name": device_name,
            "restaurant": restaurant_name,
            "type": device_type,
            "thingsboard_token": thingsboard_token,
        }

        # Créer un device dans la table devices de MongoDB
        create_device = requests.post(f"{api_url}/device", headers=headers, json=config)
        create_device.raise_for_status()

        # Récupérer l'identifiant de ce device dans table devices
        get_device_by_name = requests.get(
            f"{api_url}/device/byName?name={device_name}", headers=headers
        )
        get_device_by_name.raise_for_status()
        device_id = get_device_by_name.json()["id"]

        # Créer une clé API unique dans la table authorizationkeys
        create_authorization_key = requests.post(
            f"{api_url}/authorization/{device_id}", headers=headers
        )
        create_authorization_key.raise_for_status()

    except requests.HTTPError as err:
        print(err)
        sys.exit(1)
