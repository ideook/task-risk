import argparse
import os

from api.db import get_conn


def main():
    parser = argparse.ArgumentParser(description="Set active O*NET data version")
    parser.add_argument(
        "--data-version",
        default=os.getenv("ONET_DATA_VERSION")
        or os.getenv("DEFAULT_DATA_VERSION")
        or "30.1",
        help="O*NET data version label",
    )
    args = parser.parse_args()

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE data_version SET is_active = FALSE WHERE is_active = TRUE")
            cur.execute(
                """
                INSERT INTO data_version (id, is_active)
                VALUES (%s, %s)
                ON CONFLICT (id) DO UPDATE SET is_active = EXCLUDED.is_active
                """,
                (args.data_version, True),
            )
        conn.commit()


if __name__ == "__main__":
    main()
