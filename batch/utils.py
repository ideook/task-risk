import csv
import re
from typing import Dict, Iterable, Iterator, List, Tuple

INSERT_RE = re.compile(
    r"INSERT\s+INTO\s+(\w+)\s*\((.*?)\)\s*VALUES\s*\((.*)\);",
    re.IGNORECASE | re.DOTALL,
)


def parse_insert(statement: str) -> Tuple[str, List[str], List[str]]:
    match = INSERT_RE.search(statement)
    if not match:
        raise ValueError("not an INSERT statement")
    table = match.group(1)
    columns_raw = match.group(2)
    values_raw = match.group(3)
    columns = [col.strip().strip("`") for col in columns_raw.split(",")]
    reader = csv.reader(
        [values_raw], delimiter=",", quotechar="'", doublequote=True, skipinitialspace=True
    )
    values = next(reader)
    return table, columns, values


def iter_insert_rows(file_path: str, table_name: str) -> Iterator[Dict[str, str]]:
    buffer = ""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            line_stripped = line.lstrip()
            if line_stripped.startswith("INSERT INTO"):
                buffer = line_stripped
                if line_stripped.rstrip().endswith(";"):
                    try:
                        table, columns, values = parse_insert(buffer)
                    except ValueError:
                        buffer = ""
                        continue
                    if table == table_name:
                        row = dict(zip(columns, values))
                        yield _normalize_row(row)
                    buffer = ""
            elif buffer:
                buffer += line
                if line.rstrip().endswith(";"):
                    try:
                        table, columns, values = parse_insert(buffer)
                    except ValueError:
                        buffer = ""
                        continue
                    if table == table_name:
                        row = dict(zip(columns, values))
                        yield _normalize_row(row)
                    buffer = ""


def _normalize_row(row: Dict[str, str]) -> Dict[str, str]:
    normalized = {}
    for key, value in row.items():
        if value is None:
            normalized[key] = None
            continue
        if isinstance(value, str) and value.upper() == "NULL":
            normalized[key] = None
        else:
            normalized[key] = value
    return normalized


def copy_rows(conn, table: str, columns: List[str], rows: Iterable[Tuple]) -> int:
    count = 0
    col_sql = ", ".join(columns)
    with conn.cursor() as cur:
        with cur.copy(f"COPY {table} ({col_sql}) FROM STDIN") as copy:
            for row in rows:
                copy.write_row(row)
                count += 1
    return count
