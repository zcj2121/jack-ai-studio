# Alembic Migration

Day 29 建立数据库结构版本管理边界：

- `env.py` 读取服务端 `JACK_DATABASE_URL`，并绑定 `Base.metadata`。
- `versions/20260902_0001_create_users_table.py` 创建初始 `users` 表。
- `--sql` 会生成 SQL 但不连接数据库，适合在没有 PostgreSQL 的环境检查 Migration。

在仓库根目录执行：

```bash
JACK_DATABASE_URL=postgresql://user:password@localhost:5432/jack \
  uv run alembic upgrade head --sql
```

真实执行 `upgrade head` 前必须提供可用 PostgreSQL，并由部署环境注入连接配置；不要把密码写入 Git。
