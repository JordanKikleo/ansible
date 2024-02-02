import json
import shared
import variables
import requests

# API credentials
api_url = shared.api_url
headers = shared.headers
thingsboard = shared.thingsboard
customer_id_ops = shared.customer_id_ops

# Paths
old_config_path = shared.old_config_path
device_config_path = shared.device_config_path

# Variables
device_name = variables.device_name
restaurant_name = variables.restaurant_name
device_port = variables.device_port
device_type = variables.device_type

shared_attributes = [
    "port",
    "name",
    "restaurant",
    "type",
    "TOP_LIMIT",
    "BOTTOM_LIMIT",
    "LEFT_LIMIT",
    "RIGHT_LIMIT",
    "DIST_THRESHOLD",
    "sleeping",
]

upper_shared_attributes = [
    "LUMINOSITY",
]

# Récupérer les informations de ce device dans la table devices
get_device_by_name = requests.get(
    f"{api_url}/device/byName?name={device_name}", headers=headers
)
get_device_by_name.raise_for_status()
get_device_by_name = get_device_by_name.json()
device_id = get_device_by_name["id"]
thingsboard_token = get_device_by_name["thingsboard_token"]
thingsboard_device = next(
    (
        item
        for item in thingsboard.get_all_devices(customer_id_ops)
        if item["label"] == device_port
    ),
    False,
)
thingsboard_device_id = thingsboard_device["id"]["id"]

# Récupérer le token de ce device dans la table authorizationkeys
get_authorization_key = requests.get(
    f"{api_url}/authorization/byDeviceId?deviceId={device_id}", headers=headers
)
get_authorization_key.raise_for_status()
device_api_key = get_authorization_key.json()["apiKey"]


def create_device_config():
    json_config = {}

    json_config["port"] = device_port
    json_config["name"] = device_name
    json_config["restaurant"] = restaurant_name
    json_config["type"] = device_type

    json_config["TOP_LIMIT"] = 100
    json_config["BOTTOM_LIMIT"] = 700
    json_config["LEFT_LIMIT"] = 260
    json_config["RIGHT_LIMIT"] = 1060

    json_config["schedule"] = [
        {"type": "noon", "start_time": "11:30", "stop_time": "14:00"}
    ]

    json_config["DIST_THRESHOLD"] = 50
    json_config["sleeping"] = "false"
    json_config["LUMINOSITY"] = 100

    json_config["id"] = device_id
    json_config["thingsboard_token"] = thingsboard_token
    json_config["api_key"] = device_api_key

    # Enregistrer les données dans deviceConfig.json
    with open(device_config_path, "w") as f:
        json.dump(json_config, f)

    return json_config


if __name__ == "__main__":
    print("Création de deviceConfig.json et des shared attributes ...")
    device_config = create_device_config()
    thingsboard_schedule = {}

    for element in device_config["schedule"]:
        type = element["type"]
        start_time = element["start_time"]
        stop_time = element["stop_time"]
        thingsboard_schedule["dc_" + type + "_start_time"] = start_time
        thingsboard_schedule["dc_" + type + "_stop_time"] = stop_time

    thingsboard_shared_attributes_config = {
        f"dc_{shared_key.lower()}": device_config[shared_key]
        for shared_key in shared_attributes
    }
    thingsboard_upper_shared_attributes_config = {
        f"dc_{shared_key.upper()}": device_config[shared_key]
        for shared_key in upper_shared_attributes
    }
    thingsboard_shared_attributes_config.update(
        **thingsboard_upper_shared_attributes_config, **thingsboard_schedule
    )

    # Insérer les données dans les shared attributes de Thingsboard
    create_shared_attributes = thingsboard.create_device_attributes(
        thingsboard_device_id, thingsboard_shared_attributes_config, "SHARED_SCOPE"
    )
    create_shared_attributes.raise_for_status()
