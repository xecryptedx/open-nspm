from __future__ import annotations

import time

from .tasks import pull_snapshot_task

__all__ = ["pull_snapshot_task"]


def main() -> None:
    print("Worker started. Waiting for tasks...")
    while True:
        time.sleep(60)


if __name__ == "__main__":
    main()
