import random
import time
import json


ZONES = ["Zone-A-Coke-Oven", "Zone-B-Blast-Furnace", "Zone-C-Storage", "Zone-D-Maintenance"]

GAS_PROFILES = {
    "Zone-A-Coke-Oven": (30, 90),
    "Zone-B-Blast-Furnace": (10, 60),
    "Zone-C-Storage": (5, 30),
    "Zone-D-Maintenance": (5, 25),
}


def add_noise(value, noise_range=1.5):
    return round(value + random.uniform(-noise_range, noise_range), 1)


def generate_reading(zone, scenario="normal"):
    base_gas_min, base_gas_max = GAS_PROFILES.get(zone, (5, 40))

    if scenario == "critical":
        gas_lel = round(random.uniform(65, 85), 1)
        oxygen = round(random.uniform(17.5, 19.0), 1)
        co_ppm = round(random.uniform(40, 70), 1)
        temperature = round(random.uniform(380, 500), 1)
    elif scenario == "warning":
        gas_lel = round(random.uniform(35, 64), 1)
        oxygen = round(random.uniform(19.0, 20.0), 1)
        co_ppm = round(random.uniform(20, 39), 1)
        temperature = round(random.uniform(280, 379), 1)
    else:
        gas_lel = add_noise(random.uniform(base_gas_min, base_gas_max * 0.4))
        oxygen = add_noise(random.uniform(20.5, 21.0))
        co_ppm = add_noise(random.uniform(2, 18))
        temperature = add_noise(random.uniform(180, 270))

    return {
        "zone": zone,
        "timestamp": round(time.time()),
        "gas_lel_percent": gas_lel,
        "oxygen_percent": oxygen,
        "co_ppm": co_ppm,
        "temperature_celsius": temperature,
        "pressure_kpa": add_noise(random.uniform(95, 115)),
    }


def get_all_zone_readings(inject_critical_zone=None):
    readings = []
    for zone in ZONES:
        if zone == inject_critical_zone:
            readings.append(generate_reading(zone, scenario="critical"))
        else:
            readings.append(generate_reading(zone, scenario="normal"))
    return readings


def stream_readings(interval=3, cycles=5, inject_critical_zone=None):
    for _ in range(cycles):
        batch = get_all_zone_readings(inject_critical_zone=inject_critical_zone)
        print(json.dumps(batch, indent=2))
        time.sleep(interval)


if __name__ == "__main__":
    stream_readings(interval=2, cycles=3, inject_critical_zone="Zone-A-Coke-Oven")
