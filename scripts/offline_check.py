import argparse
import json
import os
import re
from pathlib import Path

from batch.utils import iter_insert_rows

REQUIRED_FILES = {
    "occupation_data": "03_occupation_data.sql",
    "alternate_titles": "29_alternate_titles.sql",
    "task_statements": "17_task_statements.sql",
    "task_ratings": "18_task_ratings.sql",
}

REQUIRED_COLUMNS = {
    "occupation_data": {"onetsoc_code", "title", "description"},
    "alternate_titles": {"onetsoc_code", "alternate_title", "short_title"},
    "task_statements": {"task_id", "task"},
    "task_ratings": {
        "onetsoc_code",
        "task_id",
        "scale_id",
        "category",
        "data_value",
        "n",
        "standard_error",
        "lower_ci_bound",
        "upper_ci_bound",
        "recommend_suppress",
        "date_updated",
        "domain_source",
    },
}

SOC_PATTERN = re.compile(r"^\d{2}-\d{4}\.\d{2}$")
INSERT_RE = re.compile(r"INSERT\s+INTO\s+`?(\w+)`?", re.IGNORECASE)


def resolve_sql_dir(raw: str) -> Path:
    sql_dir = Path(raw)
    if not sql_dir.is_absolute():
        sql_dir = (Path(__file__).resolve().parents[1] / sql_dir).resolve()
    return sql_dir


def sample_rows(file_path: str, table: str, limit: int) -> list[dict]:
    rows = []
    for row in iter_insert_rows(file_path, table):
        rows.append(row)
        if len(rows) >= limit:
            break
    return rows


def count_insert_rows(file_path: Path, table: str) -> int:
    count = 0
    with file_path.open("r", encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            line_strip = line.lstrip()
            if not line_strip.startswith("INSERT"):
                continue
            match = INSERT_RE.match(line_strip)
            if not match:
                continue
            if match.group(1) == table:
                count += 1
    return count


def null_stats(rows: list[dict], required_cols: set[str]) -> dict[str, int]:
    stats = {col: 0 for col in required_cols}
    for row in rows:
        for col in required_cols:
            value = row.get(col)
            if value is None or value == "":
                stats[col] += 1
    return stats


def key_set(table: str, rows: list[dict]) -> set:
    if table == "occupation_data":
        return {row.get("onetsoc_code") for row in rows if row.get("onetsoc_code")}
    if table == "alternate_titles":
        return {
            (row.get("onetsoc_code"), row.get("alternate_title"))
            for row in rows
            if row.get("onetsoc_code") and row.get("alternate_title")
        }
    if table == "task_statements":
        return {row.get("task_id") for row in rows if row.get("task_id")}
    if table == "task_ratings":
        return {
            (row.get("onetsoc_code"), row.get("task_id"), row.get("scale_id"))
            for row in rows
            if row.get("onetsoc_code") and row.get("task_id") and row.get("scale_id")
        }
    return set()


def analyze_dir(sql_dir: Path, sample: int, count_only: bool, no_count: bool):
    failures = []
    report = {}

    print(f"sql_dir: {sql_dir}")

    for table, filename in REQUIRED_FILES.items():
        file_path = sql_dir / filename
        entry = {"file": str(file_path), "count": None, "rows": []}

        if not file_path.exists():
            failures.append(f"missing file: {file_path}")
            report[table] = entry
            continue

        if not no_count:
            entry["count"] = count_insert_rows(file_path, table)
            print(f"{table}: insert rows (count) = {entry['count']}")

        if count_only:
            report[table] = entry
            continue

        rows = sample_rows(str(file_path), table, sample)
        entry["rows"] = rows
        print(f"{table}: sampled {len(rows)} rows")
        if not rows:
            failures.append(f"no rows found in {filename}")
            report[table] = entry
            continue

        cols = set(rows[0].keys())
        missing_cols = REQUIRED_COLUMNS[table] - cols
        if missing_cols:
            failures.append(f"{table} missing columns: {sorted(missing_cols)}")

        stats = null_stats(rows, REQUIRED_COLUMNS[table])
        entry["nulls"] = stats
        for col, count in sorted(stats.items()):
            if count:
                print(f"  nulls in sample: {col} = {count}")

        if table == "occupation_data":
            bad = [
                r
                for r in rows
                if r.get("onetsoc_code")
                and not SOC_PATTERN.match(r["onetsoc_code"])
            ]
            if bad:
                failures.append("occupation_data has invalid onetsoc_code format in sample")

        report[table] = entry

    return failures, report


def compare_reports(left: dict, right: dict):
    comparison = {}
    print("comparison:")
    for table in REQUIRED_FILES.keys():
        l_entry = left.get(table, {})
        r_entry = right.get(table, {})
        l_count = l_entry.get("count")
        r_count = r_entry.get("count")
        table_comp = {}

        if l_count is not None and r_count is not None:
            diff = r_count - l_count
            table_comp["count"] = {
                "left": l_count,
                "right": r_count,
                "diff": diff,
            }
            print(f"- {table}: count diff = {diff} (left={l_count}, right={r_count})")

        l_rows = l_entry.get("rows") or []
        r_rows = r_entry.get("rows") or []
        if l_rows and r_rows:
            l_keys = key_set(table, l_rows)
            r_keys = key_set(table, r_rows)
            if l_keys and r_keys:
                inter = len(l_keys & r_keys)
                denom = min(len(l_keys), len(r_keys))
                ratio = inter / denom if denom else 0.0
                table_comp["sample_overlap"] = {
                    "intersection": inter,
                    "denominator": denom,
                    "ratio": ratio,
                }
                print(f"- {table}: sample overlap = {inter}/{denom} ({ratio:.2%})")

        comparison[table] = table_comp

    return comparison


def main():
    parser = argparse.ArgumentParser(description="Offline O*NET SQL sanity checks (no DB)")
    parser.add_argument(
        "--sql-dir",
        default=os.getenv("ONET_SQL_DIR", "./Data/db_30_1_mysql"),
        help="Path to O*NET MySQL SQL files",
    )
    parser.add_argument(
        "--compare-to",
        default=None,
        help="Second O*NET SQL dir to compare (optional)",
    )
    parser.add_argument("--sample", type=int, default=50, help="Rows to sample per file")
    parser.add_argument(
        "--count-only",
        action="store_true",
        help="Only count INSERT rows (skip sample parse)",
    )
    parser.add_argument(
        "--no-count",
        action="store_true",
        help="Skip counting rows (sample only)",
    )
    parser.add_argument(
        "--report-json",
        default=None,
        help="Path to write comparison report JSON",
    )
    args = parser.parse_args()

    sql_dir = resolve_sql_dir(args.sql_dir)
    failures, report = analyze_dir(sql_dir, args.sample, args.count_only, args.no_count)

    comparison = None
    if args.compare_to:
        other_dir = resolve_sql_dir(args.compare_to)
        other_failures, other_report = analyze_dir(
            other_dir, args.sample, args.count_only, args.no_count
        )
        failures.extend(other_failures)
        comparison = compare_reports(report, other_report)

    if args.report_json and comparison is not None:
        payload = {
            "left_dir": str(sql_dir),
            "right_dir": str(resolve_sql_dir(args.compare_to)),
            "comparison": comparison,
        }
        Path(args.report_json).write_text(
            json.dumps(payload, ensure_ascii=True, indent=2)
        )

    if failures:
        print("FAILED:")
        for item in failures:
            print(f"- {item}")
        raise SystemExit(1)

    print("OK")


if __name__ == "__main__":
    main()
