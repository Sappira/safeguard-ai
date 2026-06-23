import json
import os
import random

RISK_RULES = {
    "gas_lel_warning": 25,
    "gas_lel_critical": 50,
    "oxygen_low": 19.5,
    "co_ppm_warning": 25,
    "co_ppm_critical": 50,
}

DANGEROUS_PERMIT_COMBINATIONS = {
    "HOT_WORK": ["gas_lel_high", "oxygen_low"],
    "CONFINED_SPACE_ENTRY": ["oxygen_low", "co_high"],
    "ELECTRICAL_ISOLATION": ["gas_lel_high"],
}

DEMO_ALERTS = {
    "CRITICAL": [
        "CRITICAL ALERT: Compound risk detected in {zone}. Gas LEL at {gas}% with active HOT_WORK permit in the same zone during shift changeover. Immediate actions required: 1. Suspend all hot work operations immediately. 2. Evacuate non-essential personnel from the zone. 3. Notify shift supervisor and safety officer. 4. Do not resume operations until gas levels drop below 10% LEL and permit is re-evaluated.",
        "CRITICAL ALERT: Dangerous compound condition identified in {zone}. Elevated gas concentration combined with active work permit and reduced supervision during changeover matches pre-incident pattern from Visakhapatnam 2025. Initiate emergency protocol: evacuate zone, isolate ignition sources, alert emergency response team.",
    ],
    "WARNING": [
        "WARNING: Elevated sensor readings detected in {zone}. Gas LEL at {gas}% is above warning threshold. Monitor closely and prepare to suspend active work permits if levels rise further. Ensure supervisor is present and all personnel are briefed on evacuation routes.",
        "WARNING: Abnormal atmospheric conditions in {zone}. CO levels and oxygen readings require attention. Recommend immediate re-testing and increased monitoring frequency. Shift supervisor should review active permits for this zone.",
    ],
    "SAFE": [
        "All parameters within safe operating limits.",
    ]
}


def evaluate_sensor_flags(reading):
    flags = []
    if reading["gas_lel_percent"] >= RISK_RULES["gas_lel_critical"]:
        flags.append("gas_lel_critical")
    elif reading["gas_lel_percent"] >= RISK_RULES["gas_lel_warning"]:
        flags.append("gas_lel_high")
    if reading["oxygen_percent"] < RISK_RULES["oxygen_low"]:
        flags.append("oxygen_low")
    if reading["co_ppm"] >= RISK_RULES["co_ppm_critical"]:
        flags.append("co_high")
    elif reading["co_ppm"] >= RISK_RULES["co_ppm_warning"]:
        flags.append("co_warning")
    return flags


def find_active_permit(zone, permits):
    for p in permits:
        if p["zone"] == zone and p["status"] == "ACTIVE":
            return p
    return None


def find_shift_info(zone, shifts):
    for s in shifts:
        if s["zone"] == zone:
            return s
    return None


def calculate_compound_risk(sensor_reading, permits, shifts):
    zone = sensor_reading["zone"]
    sensor_flags = evaluate_sensor_flags(sensor_reading)
    active_permit = find_active_permit(zone, permits)
    shift_info = find_shift_info(zone, shifts)

    compound_triggers = []
    risk_level = "SAFE"

    if active_permit:
        work_type = active_permit["work_type"]
        dangerous_flags = DANGEROUS_PERMIT_COMBINATIONS.get(work_type, [])
        matched = [f for f in sensor_flags if f in dangerous_flags]
        if matched:
            compound_triggers.append({
                "type": "permit_sensor_conflict",
                "permit": work_type,
                "sensor_flags": matched
            })
            risk_level = "CRITICAL"

    if shift_info and shift_info["changeover_in_progress"] and sensor_flags:
        compound_triggers.append({
            "type": "changeover_with_hazard",
            "sensor_flags": sensor_flags
        })
        if risk_level != "CRITICAL":
            risk_level = "WARNING"

    if not shift_info or not shift_info["supervisor_on_site"]:
        if "gas_lel_critical" in sensor_flags or "co_high" in sensor_flags:
            compound_triggers.append({"type": "no_supervisor_critical_gas"})
            risk_level = "CRITICAL"

    if not compound_triggers and sensor_flags:
        risk_level = "WARNING" if "gas_lel_critical" not in sensor_flags else "CRITICAL"

    return {
        "zone": zone,
        "risk_level": risk_level,
        "sensor_flags": sensor_flags,
        "active_permit": active_permit,
        "shift_changeover": shift_info["changeover_in_progress"] if shift_info else False,
        "compound_triggers": compound_triggers,
        "sensor_reading": sensor_reading,
    }


def generate_ai_alert(risk_result):
    risk_level = risk_result["risk_level"]
    zone = risk_result["zone"]
    gas = risk_result["sensor_reading"]["gas_lel_percent"]

    if risk_level == "SAFE" and not risk_result["sensor_flags"]:
        return {"alert": "All parameters within safe limits.", "recommendation": "Continue normal monitoring."}

    templates = DEMO_ALERTS.get(risk_level, DEMO_ALERTS["SAFE"])
    alert_text = random.choice(templates).format(zone=zone, gas=gas)

    return {
        "alert": alert_text,
        "risk_level": risk_level,
        "zone": zone
    }


def run_risk_scan(sensor_readings, permits, shifts):
    results = []
    for reading in sensor_readings:
        risk = calculate_compound_risk(reading, permits, shifts)
        if risk["risk_level"] != "SAFE" or risk["sensor_flags"]:
            alert = generate_ai_alert(risk)
            risk["ai_alert"] = alert
        else:
            risk["ai_alert"] = {"alert": "Safe", "recommendation": "Normal monitoring."}
        results.append(risk)
    return results
