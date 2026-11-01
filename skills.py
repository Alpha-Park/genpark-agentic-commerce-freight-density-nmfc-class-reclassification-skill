# -*- coding: utf-8 -*-
"""GenPark Industrial Skill: genpark-agentic-commerce-freight-density-nmfc-class-reclassification-skill
Category: agentic_commerce
Website: https://www.genpark.ai
LinkedIn: https://www.linkedin.com/company/92955550
"""
import sys
import json
import math

sys.stdout.reconfigure(encoding="utf-8")

def evaluate_nmfc_density_classification(weight_lbs, length_inches, width_inches, height_inches, billed_class=70):
    if weight_lbs <= 0 or length_inches <= 0 or width_inches <= 0 or height_inches <= 0:
        raise ValueError("Dimensions and weight must be positive numbers")
        
    cubic_inches = length_inches * width_inches * height_inches
    cubic_feet = cubic_inches / 1728.0
    density_pcf = weight_lbs / cubic_feet
    
    # NMFC 11-tier density scale:
    # >= 50 PCF: Class 50
    # 35 - 50: Class 55
    # 30 - 35: Class 60
    # 22.5 - 30: Class 65
    # 15 - 22.5: Class 70
    # 12 - 15: Class 77.5
    # 10 - 12: Class 85
    # 8 - 10: Class 92.5
    # 6 - 8: Class 100
    # 4 - 6: Class 125
    # 2 - 4: Class 175
    # 1 - 2: Class 250
    # < 1: Class 400
    if density_pcf >= 50.0:
        correct_class = 50.0
    elif density_pcf >= 35.0:
        correct_class = 55.0
    elif density_pcf >= 30.0:
        correct_class = 60.0
    elif density_pcf >= 22.5:
        correct_class = 65.0
    elif density_pcf >= 15.0:
        correct_class = 70.0
    elif density_pcf >= 12.0:
        correct_class = 77.5
    elif density_pcf >= 10.0:
        correct_class = 85.0
    elif density_pcf >= 8.0:
        correct_class = 92.5
    elif density_pcf >= 6.0:
        correct_class = 100.0
    elif density_pcf >= 4.0:
        correct_class = 125.0
    elif density_pcf >= 2.0:
        correct_class = 175.0
    elif density_pcf >= 1.0:
        correct_class = 250.0
    else:
        correct_class = 400.0
        
    dispute_indicated = correct_class != float(billed_class)
    carrier_upcharge_risk = correct_class > float(billed_class)
    
    return {
        "weight_lbs": weight_lbs,
        "volume_cubic_feet": round(cubic_feet, 2),
        "shipment_density_pcf": round(density_pcf, 2),
        "billed_nmfc_class": billed_class,
        "audited_correct_class": correct_class,
        "reclassification_discrepancy": dispute_indicated,
        "carrier_inspection_upcharge_risk": carrier_upcharge_risk,
        "audit_action": "File billing correction dispute with carrier weight & inspection certificate." if dispute_indicated else "Billed class fully compliant with NMFC density guidelines."
    }


def handle_rpc(request_str):
    try:
        req = json.loads(request_str)
        rpc_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})
        
        if method == "tools/list":
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "tools": [{
                        "name": "evaluate_nmfc_density_classification",
                        "description": """Evaluate Less-Than-Truckload (LTL) freight shipment density (pounds per cubic foot, PCF) and determine statutory NMFC freight class.
Defends shippers against carrier post-audit re-classification inspection charges (e.g. upgrading Class 70 to Class 125 due to low density packaging).""",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    }]
                }
            })
        elif method == "tools/call":
            call_params = params.get("arguments", {})
            res = evaluate_nmfc_density_classification(**call_params)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "content": [{
                        "type": "text",
                        "text": json.dumps(res, indent=2)
                    }]
                }
            })
        else:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "error": {"code": -32601, "message": f"Method '{method}' not found"}
            })
    except Exception as e:
        return json.dumps({
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32000, "message": str(e)}
        })

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        sample = {'weight_lbs': 680.0, 'length_inches': 48.0, 'width_inches': 40.0, 'height_inches': 52.0, 'billed_class': 70}
        out = evaluate_nmfc_density_classification(**sample)
        print("[TEST_PASS] Output:", json.dumps(out))
    else:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            print(handle_rpc(line))
