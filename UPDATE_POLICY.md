# 知识库更新策略

## 更新原则

1. **循证优先**：所有新增知识必须有明确来源（指南、文献、临床试验）
2. **结构化录入**：严格遵循三元组 schema（head-relation-tail）
3. **版本追溯**：每次更新需记录在 CHANGELOG.md
4. **质量保证**：更新后必须通过 `test_kb_format.py` 全部测试

## 更新流程

```bash
# 1. 编辑对应领域的 JSON 文件
vim data/knowledge-graph/xxx.json

# 2. 运行格式验证
python3 scripts/tests/test_kb_format.py

# 3. 重新构建知识库
python3 scripts/build_kb.py

# 4. 提交更新
git add -A
git commit -m "update: 简要描述更新内容"

# 5. 推送到 GitHub
git push origin main
```

## 更新频率建议

| 内容类型 | 建议更新频率 |
|----------|-------------|
| 指南推荐 | 指南更新后（如 CSCO 年度更新） |
| 流行病学数据 | 每年（跟随国家癌症中心统计） |
| 生物标志物 | 每季度（跟随研究进展） |
| 治疗方案 | 新药获批或指南更新后 |

## Confidence 评分标准

| 评分 | 含义 |
|------|------|
| 0.95-1.00 | 高级别证据（RCT、权威指南、meta分析） |
| 0.85-0.94 | 中高级别证据（大型队列研究、专家共识） |
| 0.70-0.84 | 中级别证据（回顾性研究、病例报告） |
| < 0.70 | 低级别证据（专家意见、初步研究） |

## 新增知识域

如需新增知识域（domain），需要：
1. 更新 `schemas/triplet_schema.json` 中的 domain enum
2. 在 `docs/domain_guide.md` 中记录域定义和边界
3. 创建新的 JSON 文件到 `data/knowledge-graph/`
4. 更新 `scripts/tests/test_kb_format.py` 中的 VALID_DOMAINS
