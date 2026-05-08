#!/usr/bin/env python3
"""甲状腺癌知识库构建脚本"""
import json, os
from datetime import datetime

SRC = "data/knowledge-graph"
OUT = "data/kb.json"
META = "data/kb_meta.json"

DOMAIN_RULES = [
    (["筛查", "流行病学", "发病率", "死亡率", "病死"], "流行病学"),
    (["分期", "TNM", "AJCC", "分级"], "分期系统"),
    (["基因", "突变", "BRAF", "RET", "分子"], "分子分型"),
    (["手术", "切除", "甲状腺"], "外科治疗"),
    (["化疗", "靶向", "免疫", "碘131", "TSH"], "系统治疗"),
    (["放疗"], "放射治疗"),
    (["随访", "监测", "预后"], "随访与预后"),
]

def infer_domain(head, existing=""):
    if existing.strip(): return existing.strip()
    for kws, d in DOMAIN_RULES:
        if any(kw in head for kw in kws): return d
    return "治疗方案"

def build():
    entries, seen = [], set()
    stats = {"by_file": {}}
    for f in sorted(os.listdir(SRC)):
        if not f.endswith('.json'): continue
        data = json.load(open(f"{SRC}/{f}"))
        added = 0
        for e in data:
            n = {
                "head": e.get("head", ""),
                "relation": e.get("relation", ""),
                "tail": e.get("tail", ""),
                "source": e.get("source", ""),
                "evidence": e.get("evidence", "专家共识"),
                "domain": infer_domain(e.get("head",""), e.get("domain","")),
                "confidence": e.get("confidence", 0.8),
                "update_date": datetime.now().strftime("%Y-%m-%d"),
            }
            key = (n["head"], n["relation"], n["tail"])
            if key not in seen:
                seen.add(key); entries.append(n); added += 1
        stats["by_file"][f] = added
        print(f"  {f}: {added}条")
    
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
    
    domains = {}
    for e in entries:
        d = e.get("domain", "未分类")
        domains[d] = domains.get(d, 0) + 1
    
    meta = {"version": "1.0.0", "date": datetime.now().strftime("%Y-%m-%d"), 
            "total": len(entries), "domains": domains}
    with open(META, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 完成: {len(entries)}条 | 域: {len(domains)}个")

if __name__ == "__main__":
    build()
