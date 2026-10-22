Python
import json
import os
import pytest
from jsonschema import validate, ValidationError

def test_ecosystem_schema_exists():
    assert os.path.exists("schemas/beast_ecosystem_dispatch_schema.json"), "Master dispatch schema missing!"

def test_valid_cross_division_dispatch():
    schema_path = "schemas/beast_ecosystem_dispatch_schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    valid_payload = {
        "transaction_id": "d1a2b3c4-5e6f-7a8b-9c0d-1e2f3a4b5c6d",
        "timestamp": "2026-10-22T14:40:00Z",
        "origin_division": "DIV_001_EXECUTIVE",
        "target_division": "DIV_004_INFRASTRUCTURE",
        "directive_payload": {
            "action": "PROVISION_NODE_CLUSTER",
            "resource_amount": 100,
            "target_entity": "NODE_CLUSTER_IND_01"
        },
        "judicial_compliance_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "sentinel_verification_sig": "a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890"
    }

    # Should validate cleanly
    validate(instance=valid_payload, schema=schema)

def test_missing_judicial_hash_fails():
    schema_path = "schemas/beast_ecosystem_dispatch_schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    invalid_payload = {
        "transaction_id": "d1a2b3c4-5e6f-7a8b-9c0d-1e2f3a4b5c6d",
        "timestamp": "2026-10-22T14:40:00Z",
        "origin_division": "DIV_001_EXECUTIVE",
        "target_division": "DIV_004_INFRASTRUCTURE",
        "directive_payload": {
            "action": "PROVISION_NODE_CLUSTER",
            "resource_amount": 100,
            "target_entity": "NODE_CLUSTER_IND_01"
        },
        "sentinel_verification_sig": "a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890"
        # Fails because judicial_compliance_hash is omitted
    }

    with pytest.raises(ValidationError):
        validate(instance=invalid_payload, schema=schema)
