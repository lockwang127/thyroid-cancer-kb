#!/usr/bin/env python3
"""Test thyroid cancer knowledge base format validation."""

import json
import os
import sys

# Resolve project root: scripts/tests/ -> scripts/ -> project_root/
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

KG_DIR = os.path.join(_PROJECT_ROOT, "data", "knowledge-graph")
DATA_DIR = os.path.join(_PROJECT_ROOT, "data")
SCHEMA_PATH = os.path.join(_PROJECT_ROOT, "schemas", "triplet_schema.json")

REQUIRED_FIELDS = ["head", "relation", "tail", "source", "evidence", "domain", "confidence", "pmid"]
VALID_DOMAINS = ["epidemiology", "biomarkers", "csco_2024", "treatment"]


def test_json_files_exist():
    """Test that all expected JSON files exist."""
    print("\n[TEST] JSON files exist...")
    expected_files = ["epidemiology.json", "csco_2024.json", "biomarkers.json", "treatment.json"]
    for f in expected_files:
        path = os.path.join(KG_DIR, f)
        assert os.path.exists(path), f"Missing file: {path}"
    print("  [PASS] All expected JSON files exist")


def test_json_valid():
    """Test that all JSON files are valid JSON."""
    print("\n[TEST] JSON format validation...")
    for f in os.listdir(KG_DIR):
        if not f.endswith(".json"):
            continue
        filepath = os.path.join(KG_DIR, f)
        with open(filepath, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        assert isinstance(data, list), f"{f}: root must be a JSON array"
    print("  [PASS] All JSON files are valid")


def test_triplet_fields():
    """Test that all triplets have required fields."""
    print("\n[TEST] Required triplet fields...")
    for f in os.listdir(KG_DIR):
        if not f.endswith(".json"):
            continue
        filepath = os.path.join(KG_DIR, f)
        with open(filepath, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        for i, t in enumerate(data):
            for field in REQUIRED_FIELDS:
                assert field in t, f"{f}[{i}]: missing field '{field}'"
    print("  [PASS] All triplets have required fields")


def test_domain_values():
    """Test that domain values are valid."""
    print("\n[TEST] Domain value validation...")
    for f in os.listdir(KG_DIR):
        if not f.endswith(".json"):
            continue
        filepath = os.path.join(KG_DIR, f)
        with open(filepath, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        for i, t in enumerate(data):
            assert t["domain"] in VALID_DOMAINS, f"{f}[{i}]: invalid domain '{t['domain']}'"
    print("  [PASS] All domain values are valid")


def test_confidence_range():
    """Test that confidence scores are in valid range."""
    print("\n[TEST] Confidence score range...")
    for f in os.listdir(KG_DIR):
        if not f.endswith(".json"):
            continue
        filepath = os.path.join(KG_DIR, f)
        with open(filepath, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        for i, t in enumerate(data):
            assert 0 <= t["confidence"] <= 1, f"{f}[{i}]: confidence {t['confidence']} out of range [0,1]"
    print("  [PASS] All confidence scores are valid")


def test_minimum_triplets():
    """Test that each file has at least 10 triplets."""
    print("\n[TEST] Minimum triplet count (>=10 per file)...")
    for f in os.listdir(KG_DIR):
        if not f.endswith(".json"):
            continue
        filepath = os.path.join(KG_DIR, f)
        with open(filepath, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        assert len(data) >= 10, f"{f}: has {len(data)} triplets, minimum is 10"
        print(f"  {f}: {len(data)} triplets [OK]")
    print("  [PASS] All files have >= 10 triplets")


def test_no_duplicate_triplets():
    """Test that there are no duplicate triplets within a file."""
    print("\n[TEST] No duplicate triplets...")
    for f in os.listdir(KG_DIR):
        if not f.endswith(".json"):
            continue
        filepath = os.path.join(KG_DIR, f)
        with open(filepath, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        seen = set()
        for i, t in enumerate(data):
            key = (t["head"], t["relation"], t["tail"])
            assert key not in seen, f"{f}[{i}]: duplicate triplet ({t['head']}, {t['relation']}, {t['tail']})"
            seen.add(key)
    print("  [PASS] No duplicate triplets found")


def test_kb_build_output():
    """Test that build_kb.py produces valid output."""
    print("\n[TEST] Build output validation...")
    kb_path = os.path.join(DATA_DIR, "kb.json")
    meta_path = os.path.join(DATA_DIR, "kb_meta.json")

    if not os.path.exists(kb_path):
        print("  [SKIP] kb.json not found (run build_kb.py first)")
        return
    if not os.path.exists(meta_path):
        print("  [SKIP] kb_meta.json not found (run build_kb.py first)")
        return

    with open(kb_path, "r", encoding="utf-8") as f:
        kb = json.load(f)
    assert "meta" in kb, "kb.json missing 'meta' key"
    assert "triplets" in kb, "kb.json missing 'triplets' key"
    assert kb["meta"]["total_triplets"] == len(kb["triplets"]), "Triplet count mismatch"

    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)
    assert "version" in meta, "kb_meta.json missing 'version' key"
    assert "total_triplets" in meta, "kb_meta.json missing 'total_triplets' key"

    print(f"  kb.json: {kb['meta']['total_triplets']} triplets [OK]")
    print(f"  kb_meta.json: version {meta['version']} [OK]")
    print("  [PASS] Build output is valid")


def test_schema_exists():
    """Test that the triplet schema file exists and is valid JSON."""
    print("\n[TEST] Schema file validation...")
    assert os.path.exists(SCHEMA_PATH), f"Schema file not found: {SCHEMA_PATH}"
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema = json.load(f)
    assert "required" in schema, "Schema missing 'required' field"
    assert "properties" in schema, "Schema missing 'properties' field"
    print("  [PASS] Schema file is valid")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Thyroid Cancer KB - Format Validation Tests")
    print("=" * 60)

    tests = [
        test_schema_exists,
        test_json_files_exist,
        test_json_valid,
        test_triplet_fields,
        test_domain_values,
        test_confidence_range,
        test_minimum_triplets,
        test_no_duplicate_triplets,
        test_kb_build_output,
    ]

    failed = 0
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"  [FAIL] {e}")
            failed += 1
        except Exception as e:
            print(f"  [ERROR] {e}")
            failed += 1

    print("\n" + "=" * 60)
    if failed == 0:
        print(f"All {len(tests)} tests PASSED")
    else:
        print(f"{failed}/{len(tests)} tests FAILED")
    print("=" * 60)

    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    main()
