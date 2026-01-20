import argparse
import csv

from api.db import get_conn


def load_oews(cur, path: str):
    with open(path, "r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = [
            (
                row.get("soc_code"),
                row.get("ref_year_month"),
                _to_int(row.get("employment")),
                _to_int(row.get("median_wage")),
                _to_int(row.get("mean_wage")),
            )
            for row in reader
        ]
    for row in rows:
        cur.execute(
            """
            INSERT INTO bls_oews_metrics
                (soc_code, ref_year_month, employment, median_wage, mean_wage)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (soc_code, ref_year_month) DO UPDATE
            SET employment = EXCLUDED.employment,
                median_wage = EXCLUDED.median_wage,
                mean_wage = EXCLUDED.mean_wage
            """,
            row,
        )


def load_proj(cur, path: str):
    with open(path, "r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = [
            (
                row.get("soc_code"),
                row.get("projection_period"),
                _to_float(row.get("growth_pct")),
                _to_int(row.get("annual_openings")),
            )
            for row in reader
        ]
    for row in rows:
        cur.execute(
            """
            INSERT INTO bls_proj_metrics
                (soc_code, projection_period, growth_pct, annual_openings)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (soc_code, projection_period) DO UPDATE
            SET growth_pct = EXCLUDED.growth_pct,
                annual_openings = EXCLUDED.annual_openings
            """,
            row,
        )


def _to_int(value):
    if value in (None, ""):
        return None
    return int(float(value))


def _to_float(value):
    if value in (None, ""):
        return None
    return float(value)


def main():
    parser = argparse.ArgumentParser(description="Load optional BLS metrics")
    parser.add_argument("--oews")
    parser.add_argument("--projections")
    parser.add_argument("--truncate", action="store_true")
    args = parser.parse_args()

    with get_conn() as conn:
        with conn.cursor() as cur:
            if args.truncate:
                cur.execute("TRUNCATE TABLE bls_oews_metrics, bls_proj_metrics")
            if args.oews:
                load_oews(cur, args.oews)
            if args.projections:
                load_proj(cur, args.projections)
        conn.commit()


if __name__ == "__main__":
    main()
