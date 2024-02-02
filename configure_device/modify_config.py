import sys
import json

# Paths
old_config_path = "/home/kikleo/kikleo/config.json"

# Variables
device_name = sys.argv[1]
restaurant_name = sys.argv[2]
device_port = sys.argv[3]
device_type = sys.argv[4]


if __name__ == "__main__":
    try:
        with open(old_config_path) as json_data_file:
            json_config = json.load(json_data_file)

        print("Modification de config.json ...")
        json_config["port"] = int(device_port)
        json_config["name"] = device_name
        json_config["restaurant"] = restaurant_name
        json_config["mode"] = device_type

        with open(old_config_path, "w") as f:
            json.dump(json_config, f)
        print("Modification de config.json terminée")

    except FileNotFoundError:
        print(
            f"Attention : Le fichier spécifié n'a pas été trouvé dans le chemin : '{old_config_path}'"
        )
