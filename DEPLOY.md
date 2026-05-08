# 部署指南

## 1. 创建 GitHub 远程仓库

1. 访问 https://github.com/new
2. 仓库名称填写：`thyroid-cancer-kb`
3. 选择 **Public**
4. **不要** 勾选 "Add a README file"
5. 点击 "Create repository"

## 2. 关联远程仓库

```bash
cd /Users/wangxiaodong/WorkBuddy/thyroid-cancer-kb
git remote set-url origin git@github.com:lockwang127/thyroid-cancer-kb.git
```

## 3. 推送到 GitHub

```bash
git push -u origin main
```

## 4. 验证

推送成功后，访问 https://github.com/lockwang127/thyroid-cancer-kb 确认仓库内容完整。

## 后续更新

```bash
# 修改知识文件后
python3 scripts/build_kb.py
python3 scripts/tests/test_kb_format.py
git add -A
git commit -m "update: 更新描述"
git push origin main
```

## 注意事项

- 确保已配置 SSH key 到 GitHub 账户
- 确保本地 git 用户名和邮箱已配置
- 如使用 HTTPS，将 `git@github.com:` 替换为 `https://github.com/`
