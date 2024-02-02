import pytest
import json

old_config_path = "/home/kikleo/kikleo/config.json"
device_config_path = "/home/kikleo/deviceConfig.json"
dist_threshold_path = "/home/kikleo/kikleo/traynet/video/video.py"


@pytest.fixture
def fake_files(fs):
    fs.create_file(
        old_config_path,
        contents=json.dumps(
            {
                'port': 1024,
                'name': 'restest',
                'restaurant': 'RESTEST',
                'mode': 'tray',
                'StartTime': '11:30',
                'StopTime': '14:00',
                'TOP_LIMIT': 100,
                'BOTTOM_LIMIT': 700,
                'LEFT_LIMIT': 260,
                'RIGHT_LIMIT': 1060
            }
        ),
    )
    fs.create_file(
        dist_threshold_path,
        contents="""
            import numpy as np
            skipRatio = 2
            total_dist = 0
            cutter = Cutter

            # Threshold over which keypoints don't need to be computed
            DIST_THRESHOLD = 50
        """
    )
    yield fs


def test_config_creation(fake_files):
    with open(old_config_path) as json_data_file:
        config = json.load(json_data_file)
    
    assert len(config) == 10

def test_get_threshold(fake_files):
    """Get the threshold from the old video.py file.
    The threshold is the value of the variable "DIST_THRESHOLD" in the old video.py file.
    """
    with open(dist_threshold_path) as f:
        content = f.readlines()

    for line in content:
        line = line.strip()
        if "DIST_THRESHOLD" in line:
            threshold = line.split("=")[1].strip()
            break
    
    assert int(threshold) == 50

def test_update_config(fake_files):
    port = "1000"
    name = "test"
    device_type = "classic"

    with open(old_config_path) as json_data_file:
        config = json.load(json_data_file)
        
    config["port"] = port
    config["name"] = name
    config["restaurant"] = name.upper()
    config["type"] = device_type
    config.pop("mode", None)

    assert len(config) == 10

def test_device_config_creation(fake_files):
    port = "1000"
    name = "test"
    device_type = "classic"
    device_id = "id"
    thingsboard_token = "token"
    api_key = "apiKey"

    def get_threshold(dist_threshold_path):
        """Get the threshold from the old video.py file.
        The threshold is the value of the variable "DIST_THRESHOLD" in the old video.py file.
        """
        with open(dist_threshold_path) as f:
            content = f.readlines()

        for line in content:
            line = line.strip()
            if "DIST_THRESHOLD" in line:
                threshold = line.split("=")[1].strip()
                return int(threshold)
            
    with open(old_config_path) as json_data_file:
        config = json.load(json_data_file)
        
    config["port"] = port
    config["name"] = name
    config["restaurant"] = name.upper()
    config["type"] = device_type
    config["schedule"] = [{
        'type': 'noon',
        'start_time': config['StartTime'],
        'stop_time': config['StopTime']
    }]
    keys_to_remove = ['mode', 'StartTime', 'StopTime']
    for key in keys_to_remove:
        config.pop(key, None)
    
    config["DIST_THRESHOLD"] = get_threshold(dist_threshold_path)
    config["sleeping"] = False
    config["LUMINOSITY"] = 100

    config["id"] = device_id
    config["thingsboard_token"] = thingsboard_token
    config["api_key"] = api_key
    
    assert len(config) == 15