from __future__ import annotations

from typing import Sequence

from chanta_core.personal_runtime.default_personal_work_session import main as _release_main


def main(argv: Sequence[str] | None = None) -> int:
    return _release_main(argv)


__all__ = ["main"]


if __name__ == "__main__":
    raise SystemExit(main())
