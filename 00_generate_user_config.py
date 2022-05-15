import json
import numpy as np
import random as rd
import uuid


def gen_bat_config(prosumer_id, user_type):
    device_id = str(uuid.UUID(int=rd.getrandbits(128)))
    if user_type == "residential":
        min_cap, max_cap, chr_dis_power = 1, 5, 0.5
    elif user_type == "business":
        min_cap, max_cap, chr_dis_power = 5, 10, 1
    elif user_type == "industrial":
        min_cap, max_cap, chr_dis_power = 10, 20, 2
    else:
        raise ValueError
    return {"deviceType": "battery", "deviceID": device_id, 'capacity': rd.uniform(min_cap, max_cap), "chargePower": chr_dis_power}


def gen_load_config(prosumer_id, user_type):
    device_id = str(uuid.UUID(int=rd.getrandbits(128)))
    if user_type == "residential":
        min_con, max_con, time_offset_range = 1.5, 3, 1
    elif user_type == "business":
        min_con, max_con, time_offset_range = 5, 15, 0.5
    elif user_type == "industrial":
        min_con, max_con, time_offset_range = 15, 25, 0.2
    else:
        raise ValueError
    return {"deviceType": "load", "deviceID": device_id, 'peakPower': rd.uniform(min_con, max_con), "timeOffsetRange": time_offset_range, "pred_filename": prosumer_id + "-" + device_id + "-pred.csv", "filename": prosumer_id + "-" + device_id + ".csv"}


def gen_pv_config(prosumer_id, user_type):
    device_id = str(uuid.UUID(int=rd.getrandbits(128)))
    if user_type == "residential":
        min_powr, max_power, turbulance_factor = 0.5, 1, 1
    elif user_type == "business":
        min_powr, max_power, turbulance_factor = 1, 3, 0.5
    elif user_type == "industrial":
        min_powr, max_power, turbulance_factor = 15, 25, 0.2
    else:
        raise ValueError
    return {"deviceType": "solar", "deviceID": device_id, 'maxPower': rd.uniform(min_powr, max_power), "turbulenceFactor": turbulance_factor, "pred_filename": prosumer_id + "-" + device_id + "-pred.csv", "filename": prosumer_id + "-" + device_id + ".csv"}


def gen_wind_config(prosumer_id, user_type):
    device_id = str(uuid.UUID(int=rd.getrandbits(128)))
    if user_type == "residential":
        min_powr, max_power, turbulance_factor = 0.5, 1, 1
    elif user_type == "business":
        min_powr, max_power, turbulance_factor = 1, 3, 0.5
    elif user_type == "industrial":
        min_powr, max_power, turbulance_factor = 15, 25, 0.2
    else:
        raise ValueError
    return {"deviceType": "wind", "deviceID": device_id, 'maxPower': rd.uniform(min_powr, max_power), "turbulenceFactor": turbulance_factor, "pred_filename": prosumer_id + "-" + device_id + "-pred.csv", "filename": prosumer_id + "-" + device_id + ".csv"}


NUM_USERS = 20
NUM_GRID_ZONE = 5
# residential: haushalt, business: gewerbe-agmeine, industrial: landwirtschaft
USER_TYPE_RATIO = {"residential": 0.6, "business": 0.2, "industrial": 0.2}
AVAILABLE_DEVCES = {"load": gen_load_config, "battery": gen_bat_config, "wind": gen_wind_config, "solar": gen_pv_config}
DEVICE_PROB = {
    "residential": {
        "load": 1,
        "battery": 1,
        "wind": 0.2,
        "solar": 0.5
    },
    "business": {
        "load": 1,
        "battery": 1,
        "wind": 0.2,
        "solar": 0.8
    },
    "industrial": {
        "load": 1,
        "battery": 1,
        "wind": 0.2,
        "solar": 0.8
    }
}

if __name__ == '__main__':
    rd.seed(0)
    np.random.seed(0)
    configs = []
    for usr_idx in range(NUM_USERS):
        user = {}

        # Prosumer ID
        user["prosumerID"] = str(uuid.UUID(int=rd.getrandbits(128)))  # reproducible deterministic

        # Grid location
        user["gridLocation"] = "N0" + str(rd.choice(list(range(1, NUM_GRID_ZONE + 1))))

        # User Type
        if usr_idx < NUM_USERS * USER_TYPE_RATIO["residential"]:
            user["userType"] = "residential"
        elif usr_idx < NUM_USERS * (USER_TYPE_RATIO["residential"] + USER_TYPE_RATIO["business"]):
            user["userType"] = "business"
        else:
            user["userType"] = "industrial"

        # Device
        devices = []
        for device in AVAILABLE_DEVCES.keys():
            if rd.random() < DEVICE_PROB[user["userType"]][device]:
                devices.append(AVAILABLE_DEVCES[device](user["prosumerID"], user["userType"]))
        user["devices"] = devices

        configs.append(user)

    print(configs)
    with open('community_config.json', 'w') as f:
        json.dump(configs, f, indent=4)
