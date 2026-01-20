import argparse
import os

from api.db import get_conn


def main():
    parser = argparse.ArgumentParser(description="Update SOC codes for a data version")
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
            cur.execute(
                """
                UPDATE occupation_master
                SET soc_code = LEFT(onetsoc_code, 7)
                WHERE data_version = %s
                  AND (soc_code IS NULL OR soc_code = '')
                """,
                (args.data_version,),
            )
        conn.commit()


if __name__ == "__main__":
    main()
