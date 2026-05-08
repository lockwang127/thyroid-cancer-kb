# 甲状腺癌知识库 (Thyroid Cancer Knowledge Base)

基于知识三元组（head-relation-tail）的甲状腺癌结构化知识图谱，支持 RAG/LLM/AI 应用集成。

## 知识覆盖

| 知识域 | 文件 | 描述 |
|--------|------|------|
| 流行病学 | `epidemiology.json` | 发病率、死亡率、病理类型分布 |
| 分期与生物标志物 | `biomarkers.json` | TNM分期、ATA风险分层、基因突变 |
| CSCO 2024指南 | `csco_2024.json` | CSCO指南推荐方案 |
| 治疗方案 | `treatment.json` | 手术、碘131、TSH抑制、随访 |

## 数据格式

每条知识以三元组形式存储：

```json
{
  "head": "实体/概念",
  "relation": "关系",
  "tail": "值/描述",
  "source": "数据来源",
  "evidence": "证据/解释",
  "domain": "知识域",
  "confidence": 0.95,
  "pmid": "PubMed ID（可选）"
}
```

## 快速开始

```bash
# 构建知识库
python3 scripts/build_kb.py

# 运行格式验证测试
python3 scripts/tests/test_kb_format.py

# 同步到 GitHub（需先配置远程仓库）
python3 scripts/sync_to_github.py
```

## 构建产物

- `data/kb.json` — 合并后的完整知识图谱
- `data/kb_meta.json` — 知识库元数据和统计信息

## 技术栈

- 数据格式：JSON（知识三元组）
- 构建工具：Python 3
- 验证：JSON Schema + 自定义测试
- 版本管理：Git + GitHub

## 许可证

MIT License
