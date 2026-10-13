# LocalQuant V1.0 — 项目初始化

这是 LocalQuant 的第一阶段：本地 SQLite 数据库 + 自动化测试。
当前版本不联网、不下单、不提供实时投资信号；测试使用模拟数据。

## 环境要求
- Windows 10/11
- Python 3.10 或更新版本（建议使用 python.org 的稳定版）
- Git（可选）

## 1. 解压并打开项目
将 `localquant_v1.zip` 解压到你方便找到的位置，例如：
`C:\Users\你的用户名\Projects\localquant_v1`

在该文件夹空白处打开终端，或在 VS Code 中选择“文件 → 打开文件夹”。

## 2. 检查 Python
```powershell
python --version
```
如果提示找不到 Python，可以尝试：
```powershell
py --version
```

## 3. 初始化数据库
在项目根目录运行：
```powershell
python init_db.py
```
成功后会创建 `data/localquant.db`。

## 4. 运行测试
```powershell
python -m unittest discover -s tests -v
```
预期看到 3 个测试通过，结尾显示 `OK`。

## 5. 检查数据库表
运行：
```powershell
python -c "from src.database import get_table_names; print(get_table_names())"
```
应该看到 assets、market_prices、portfolio_snapshots、cash_flows、decision_logs、backtest_runs。

## 项目目录
```text
localquant_v1/
├── data/                  # 本地数据库（运行后生成）
├── src/
│   ├── __init__.py
│   └── database.py        # 数据库连接、建表函数
├── tests/
│   └── test_database.py   # 自动化测试
├── init_db.py             # 初始化入口
├── .gitignore
└── README.md
```

## 当前数据库表说明
- `assets`: 资产基本信息
- `market_prices`: 历史行情或基金净值
- `portfolio_snapshots`: 组合快照
- `cash_flows`: 入金、出金和交易现金流记录
- `decision_logs`: 系统建议及人工确认记录
- `backtest_runs`: 回测任务摘要

## 注意
- 不要把真实账户密码、验证码、API 密钥或交易凭证写入项目。
- `data/localquant.db` 是本地生成的数据文件，不建议提交到公开 GitHub 仓库。
- 这个版本只是软件基础设施，不会自动买卖资产，也不代表投资建议。
