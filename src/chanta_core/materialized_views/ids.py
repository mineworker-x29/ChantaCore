from __future__ import annotations

from uuid import uuid4


def new_materialized_view_id() -> str:
    return f"materialized_view:{uuid4()}"
