#!/usr/bin/env python3
"""Build thyroid cancer knowledge base from JSON triplet files."""

import json
import os
import sys
from datetime import datetime

KG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "knowledge-graph")
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

SCHEMA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "schemas", "triplet_schema.json")


def load_schema():
    """Load triplet JSON schema."""
    try:
        import jsonschema
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except ImportError:
        print("Warning: jsonschema not installed, skipping schema validation")
        return None


def load_triplet_file(filepath):
    """Load and validate a single triplet JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        print(f"Error: {filepath} must contain a JSON array")
        sys.exit(1)
    return data


def validate_triplets(triplets, schema):
    """Validate triplets against schema."""
    errors = []
    for i, t in enumerate(triplets):
        required_fields = ["head", "relation", "tail", "source", "evidence", "domain", "confidence", "pmid"]
        for field in required_fields:
            if field not in t:
                errors.append(f"Triplet #{i}: missing required field '{field}'")
        if "confidence" in t and not (0 <= t["confidence"] <= 1):
            errors.append(f"Triplet #{i}: confidence must be between 0 and 1")
        if "domain" in t and t["domain"] not in ["epidemiology", "biomarkers", "csco_2024", "treatment"]:
            errors.append(f"Triplet #{i}: invalid domain '{t['domain']}'")
    return errors


def build_kb():
    """Build the knowledge base from all triplet files."""
    print("=" * 60)
    print("Thyroid Cancer Knowledge Base Builder")
    print("=" * 60)

    # Load schema
    schema = load_schema()
    if schema:
        print(f"[OK] Schema loaded from {SCHEMA_PATH}")
    else:
        print("[WARN] Schema validation disabled")

    # Find and load all triplet files
    triplet_files = sorted([f for f in os.listdir(KG_DIR) if f.endswith(".json")])
    if not triplet_files:
        print("Error: No JSON files found in knowledge-graph directory")
        sys.exit(1)

    all_triplets = []
    domain_counts = {}
    source_counts = {}

    for filename in triplet_files:
        filepath = os.path.join(KG_DIR, filename)
        print(f"\n[LOAD] {filename}")
        triplets = load_triplet_file(filepath)

        # Validate
        errors = validate_triplets(triplets, schema)
        if errors:
            print(f"[ERROR] {filename} has validation errors:")
            for e in errors:
                print(f"  - {e}")
            sys.exit(1)

        all_triplets.extend(triplets)
        print(f"  -> {len(triplets)} triplets loaded")

        # Count domains
        for t in triplets:
            d = t.get("domain", "unknown")
            domain_counts[d] = domain_counts.get(d, 0) + 1
            s = t.get("source", "unknown")
            source_counts[s] = source_counts.get(s, 0) + 1

    # Build kb.json
    kb = {
        "meta": {
            "name": "thyroid-cancer-kb",
            "description": "甲状腺癌结构化知识库",
            "version": "1.0.0",
            "build_time": datetime.now().isoformat(),
            "total_triplets": len(all_triplets),
            "domains": list(domain_counts.keys()),
            "domain_counts": domain_counts
        },
        "triplets": all_triplets
    }

    kb_path = os.path.join(DATA_DIR, "kb.json")
    with open(kb_path, "w", encoding="utf-8") as f:
        json.dump(kb, f, ensure_ascii=False, indent=2)
    print(f"\n[OK] Knowledge base written to {kb_path}")

    # Build kb_meta.json
    kb_meta = {
        "name": "thyroid-cancer-kb",
        "version": "1.0.0",
        "build_time": datetime.now().isoformat(),
        "total_triplets": len(all_triplets),
        "domains": domain_counts,
        "source_files": triplet_files,
        "triplets_per_file": {f: len(load_triplet_file(os.path.join(KG_DIR, f))) for f in triplet_files},
        "confidence_distribution": _compute_confidence_distribution(all_triplets)
    }

    meta_path = os.path.join(DATA_DIR, "kb_meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(kb_meta, f, ensure_ascii=False, indent=2)
    print(f"[OK] Metadata written to {meta_path}")

    # Summary
    print("\n" + "=" * 60)
    print("BUILD SUMMARY")
    print("=" * 60)
    print(f"Total triplets: {len(all_triplets)}")
    print(f"Knowledge domains: {len(domain_counts)}")
    for d, c in sorted(domain_counts.items()):
        print(f"  - {d}: {c} triplets")
    print(f"Source files: {len(triplet_files)}")
    print(f"Build time: {kb['meta']['build_time']}")
    print("\n[DONE] Build successful!")


def _compute_confidence_distribution(triplets):
    """Compute confidence score distribution."""
    dist = {"high (>=0.9)": 0, "medium (0.7-0.89)": 0, "low (<0.7)": 0}
    for t in triplets:
        c = t.get("confidence", 0)
        if c >= 0.9:
            dist["high (>=0.9)"] += 1
        elif c >= 0.7:
            dist["medium (0.7-0.89)"] += 1
        else:
            dist["low (<0.7)"] += 1
    return dist


if __name__ == "__main__":
    build_kb()
