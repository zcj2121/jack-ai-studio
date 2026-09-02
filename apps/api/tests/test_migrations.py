"""Alembic Migration 配置和初始 revision 测试。"""

import os
import subprocess
import sys
from pathlib import Path
from unittest import TestCase

from app.db.base import Base
from app.models.user import User


PROJECT_ROOT = Path(__file__).resolve().parents[3]


class MigrationContractTest(TestCase):
    """验证 Migration 可发现 Model 并生成预期 PostgreSQL SQL。"""

    def run_alembic(self, *arguments: str, database_url: str | None) -> subprocess.CompletedProcess[str]:
        """在独立进程中运行 Alembic，避免污染当前 Settings 缓存。"""

        environment = os.environ.copy()
        if database_url is None:
            environment.pop("JACK_DATABASE_URL", None)
        else:
            environment["JACK_DATABASE_URL"] = database_url

        return subprocess.run(
            [
                sys.executable,
                "-m",
                "alembic",
                "-c",
                str(PROJECT_ROOT / "alembic.ini"),
                *arguments,
            ],
            cwd=PROJECT_ROOT,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_registers_user_model_in_shared_metadata(self) -> None:
        self.assertIs(Base.metadata.tables["users"], User.__table__)

    def test_generates_users_sql_in_offline_mode(self) -> None:
        result = self.run_alembic(
            "upgrade",
            "head",
            "--sql",
            database_url="postgresql://user:password@localhost:5432/jack",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("CREATE TABLE users", result.stdout)
        self.assertIn("UNIQUE (email)", result.stdout)
        self.assertIn("CREATE INDEX ix_users_email", result.stdout)
        self.assertIn("INSERT INTO alembic_version", result.stdout)

    def test_generates_users_sql_in_downgrade_mode(self) -> None:
        result = self.run_alembic(
            "downgrade",
            "20260902_0001:base",
            "--sql",
            database_url="postgresql://user:password@localhost:5432/jack",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("DROP INDEX ix_users_email", result.stdout)
        self.assertIn("DROP TABLE users", result.stdout)
        self.assertIn("DELETE FROM alembic_version", result.stdout)

    def test_requires_database_url_for_migrations(self) -> None:
        result = self.run_alembic(
            "upgrade",
            "head",
            "--sql",
            database_url=None,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("JACK_DATABASE_URL is required", result.stderr)
