#!/usr/bin/env bash
set -euo pipefail

src_dir="${1:-.}"
out_file="${2:-all_docs.md}"

if [[ ! -d "$src_dir" ]]; then
  echo "source directory not found: $src_dir" >&2
  exit 1
fi

mkdir -p "$(dirname "$out_file")"

out_abs="$(cd "$(dirname "$out_file")" && pwd)/$(basename "$out_file")"
tmp_file="$(mktemp)"

while IFS= read -r file; do
  file_abs="$(cd "$(dirname "$file")" && pwd)/$(basename "$file")"
  if [[ "$file_abs" == "$out_abs" ]]; then
    continue
  fi
  rel_path="${file#$src_dir/}"
  {
    echo ""
    echo "---"
    echo ""
    echo "# ${rel_path}"
    echo ""
    cat "$file"
    echo ""
  } >> "$tmp_file"
done < <(find "$src_dir" -type f | LC_ALL=C sort)

mv "$tmp_file" "$out_file"
echo "wrote: $out_file"
