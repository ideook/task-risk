import argparse
import os
import re

from api.db import get_conn


def version_key(version: str) -> tuple[int, ...]:
    parts = [int(x) for x in re.findall(r"\d+", version)]
    if not parts:
        return (0,)
    return tuple(parts)


def main():
    parser = argparse.ArgumentParser(description="Archive old O*NET data versions")
    parser.add_argument("--keep-latest", type=int, default=4)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, is_active FROM data_version")
            rows = cur.fetchall()

        versions = [row[0] for row in rows]
        active = {row[0] for row in rows if row[1]}

        sorted_versions = sorted(versions, key=version_key, reverse=True)
        keep = set(sorted_versions[: args.keep_latest]) | active
        to_delete = [v for v in versions if v not in keep]

        print(f"keep: {sorted(keep)}")
        print(f"delete: {sorted(to_delete)}")

        if args.dry_run or not to_delete:
            return

        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM data_version WHERE id = ANY(%s) AND is_active = FALSE",
                (to_delete,),
            )
        conn.commit()


if __name__ == "__main__":
    main()
