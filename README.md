# genpark-agentic-commerce-freight-density-nmfc-class-reclassification-skill

[![GenPark AI](https://img.shields.io/badge/GenPark-AI%20Ecosystem-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-0077b5)](https://www.linkedin.com/company/92955550)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](https://www.python.org/)

LTL freight shipment density (PCF), stowability, handling & liability evaluation for NMFC commodity class dispute defense.

## Overview

Part of the **GenPark Industrial Multi-Agent Skill Matrix**. Zero external pip dependencies; built purely with standard Python library modules for instant deterministic orchestration.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate LinkedIn**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## Tool Specification

- **Tool Name**: `evaluate_nmfc_density_classification`
- **Category**: `agentic_commerce`

### Method Documentation
Evaluate Less-Than-Truckload (LTL) freight shipment density (pounds per cubic foot, PCF) and determine statutory NMFC freight class.
Defends shippers against carrier post-audit re-classification inspection charges (e.g. upgrading Class 70 to Class 125 due to low density packaging).

## JSON-RPC 2.0 Integration

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "evaluate_nmfc_density_classification",
    "arguments": {
    "weight_lbs": 680.0,
    "length_inches": 48.0,
    "width_inches": 40.0,
    "height_inches": 52.0,
    "billed_class": 70
}
  }
}
```

## Running Self Tests

```bash
python skills.py --test
```
