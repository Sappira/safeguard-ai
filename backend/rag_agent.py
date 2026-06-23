import os

REGULATION_FILES = [
    "data/regulations/oisd_sample.txt",
    "data/regulations/incidents_sample.txt"
]

DEMO_RESPONSES = {
    "oxygen": "According to OISD Standard 105 and the Factory Act 1948, the safe oxygen level for confined space entry must be between 19.5% and 23.5%. Entry is strictly prohibited if oxygen falls below 19.5%. Continuous atmospheric monitoring is mandatory throughout the confined space operation, not just at the point of entry. Source: OISD Standard 105 / Factory Act 1948 Section 36.",
    "gas": "OISD Standard 105 specifies that no hot work shall be carried out in areas where gas concentration exceeds 10% LEL without explicit written authorization from the site safety officer. Hot work permits must be suspended immediately if gas readings rise above 25% LEL in the permitted zone. First alarm threshold is set at 20% LEL and evacuation alarm at 40% LEL per OISD Standard 116. Source: OISD Standard 105 and 116.",
    "hot work": "Hot work permits must not be issued within 15 metres of any active gas release point or any area where gas readings exceed 25% LEL. Any sudden increase in gas readings during an active hot work permit must result in immediate suspension of all ignition sources and evacuation of the area. The Tata Steel Jamshedpur near-miss incident of November 2024 demonstrated that permit systems must integrate with live sensor data to automatically flag dangerous combinations. Source: OISD Standard 105 / Near Miss Report 1.",
    "confined space": "Confined space entry requires atmospheric testing prior to entry. Oxygen levels must be between 19.5% and 23.5%. Gas concentrations must be below 10% LEL. Continuous monitoring is mandatory throughout the operation. No worker shall enter a confined space where the atmosphere has not been tested within the preceding one hour. Re-testing is mandatory after any process change. Source: OISD Standard 105 / Factory Act 1948 Section 37.",
    "shift": "OISD regulations require that shift changeovers in hazardous zones be documented with both incoming and outgoing supervisors signing the handover log. No shift handover is considered complete without a physical walkthrough of all active work permits. The Bhilai Steel Plant incident of August 2023 showed that incomplete permit communication during shift handover led to gas levels rising to 74% LEL undetected for 22 minutes. Source: OISD Standard 105 / Incident Report 3.",
    "permit": "A work permit system is mandatory for all non-routine maintenance and operational activities in hazardous areas per OISD Standard 105. Active permits must be cross-checked against live sensor readings before work begins. The Digital Permit Intelligence system flags dangerous simultaneous operations such as hot work permits issued in proximity to elevated gas readings. Source: OISD Standard 105.",
    "default": "Based on OISD Standards 105 and 116, and Factory Act 1948 provisions, industrial safety in hazardous zones requires continuous atmospheric monitoring, mandatory permit-to-work systems, and documented shift handover procedures. SafeGuard AI correlates these data sources to detect compound risk conditions before they escalate. For specific regulatory guidance, please refer to OISD Standard 105 (Work Permit System) or OISD Standard 116 (Fire Protection Facilities). Source: OISD / Factory Act 1948."
}


def answer_safety_query(user_question):
    question_lower = user_question.lower()

    if "oxygen" in question_lower or "o2" in question_lower:
        answer = DEMO_RESPONSES["oxygen"]
    elif "hot work" in question_lower or "welding" in question_lower or "ignition" in question_lower:
        answer = DEMO_RESPONSES["hot work"]
    elif "gas" in question_lower or "lel" in question_lower or "explosive" in question_lower:
        answer = DEMO_RESPONSES["gas"]
    elif "confined space" in question_lower or "entry" in question_lower:
        answer = DEMO_RESPONSES["confined space"]
    elif "shift" in question_lower or "changeover" in question_lower or "handover" in question_lower:
        answer = DEMO_RESPONSES["shift"]
    elif "permit" in question_lower or "ptw" in question_lower:
        answer = DEMO_RESPONSES["permit"]
    else:
        answer = DEMO_RESPONSES["default"]

    return {
        "question": user_question,
        "answer": answer,
        "source": "OISD / Factory Act 1948 / Incident Reports"
    }
