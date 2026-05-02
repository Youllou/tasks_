"""add columns table, drop task status enum

Revision ID: 0002
Revises: 0001
Create Date: 2026-05-02

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

DEFAULT_COLUMNS = [
    {"name": "Inbox",   "color": "#4a9eff", "position": 0, "is_inbox": True},
    {"name": "Backlog", "color": "#8b8b9a", "position": 1, "is_inbox": False},
    {"name": "To Do",   "color": "#f5a623", "position": 2, "is_inbox": False},
    {"name": "Done",    "color": "#4caf50", "position": 3, "is_inbox": False},
]


def upgrade() -> None:
    op.create_table(
        "columns",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("color", sa.String(20), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("is_inbox", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        # partial unique index: only one inbox per user
        sa.UniqueConstraint("user_id", "is_inbox", name="uq_columns_user_inbox",
                            postgresql_where=sa.text("is_inbox = true")),
    )
    op.create_index("ix_columns_user_id", "columns", ["user_id"])

    # Seed default columns for all existing users and map their tasks
    conn = op.get_bind()
    users = conn.execute(sa.text("SELECT id FROM users")).fetchall()

    for (user_id,) in users:
        import uuid
        from datetime import datetime, timezone

        col_ids = {}
        now = datetime.now(timezone.utc).isoformat()

        for col in DEFAULT_COLUMNS:
            col_id = str(uuid.uuid4())
            col_ids[col["name"].lower().replace(" ", "")] = col_id
            conn.execute(sa.text("""
                INSERT INTO columns (id, user_id, name, color, position, is_inbox, created_at)
                VALUES (:id, :user_id, :name, :color, :position, :is_inbox, :created_at)
            """), {
                "id": col_id,
                "user_id": user_id,
                "name": col["name"],
                "color": col["color"],
                "position": col["position"],
                "is_inbox": col["is_inbox"],
                "created_at": now,
            })

        # Map old status values to new column ids
        status_map = {
            "inbox":   col_ids["inbox"],
            "backlog": col_ids["backlog"],
            "todo":    col_ids["todo"],
            "done":    col_ids["done"],
        }
        for status, col_id in status_map.items():
            conn.execute(sa.text("""
                UPDATE tasks SET column_id = :col_id
                WHERE user_id = :user_id AND status = :status
            """), {"col_id": col_id, "user_id": user_id, "status": status})

    # Add column_id to tasks (nullable first to allow the UPDATE above on existing rows)
    op.add_column("tasks", sa.Column("column_id", sa.String(), nullable=True))
    op.create_foreign_key("fk_tasks_column_id", "tasks", "columns", ["column_id"], ["id"], ondelete="RESTRICT")
    op.create_index("ix_tasks_column_id", "tasks", ["column_id"])

    # Make column_id non-nullable now that all rows are filled
    op.alter_column("tasks", "column_id", nullable=False)

    # Drop the old status column and enum
    op.drop_index("ix_tasks_status", table_name="tasks")
    op.drop_column("tasks", "status")
    op.execute("DROP TYPE IF EXISTS task_status")


def downgrade() -> None:
    op.execute("CREATE TYPE task_status AS ENUM ('inbox', 'backlog', 'todo', 'done')")
    op.add_column("tasks", sa.Column("status", sa.Enum("inbox", "backlog", "todo", "done", name="task_status"), nullable=True))

    # Best-effort restore: map by column name
    conn = op.get_bind()
    name_to_status = {"Inbox": "inbox", "Backlog": "backlog", "To Do": "todo", "Done": "done"}
    for col_name, status in name_to_status.items():
        conn.execute(sa.text("""
            UPDATE tasks t
            SET status = :status
            FROM columns c
            WHERE t.column_id = c.id AND c.name = :col_name
        """), {"status": status, "col_name": col_name})

    op.alter_column("tasks", "status", nullable=False)
    op.create_index("ix_tasks_status", "tasks", ["status"])

    op.drop_constraint("fk_tasks_column_id", "tasks", type_="foreignkey")
    op.drop_index("ix_tasks_column_id", table_name="tasks")
    op.drop_column("tasks", "column_id")
    op.drop_table("columns")