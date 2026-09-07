#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

VERSION="$(python3 -c "import json; print(json.load(open('MANIFEST.json', encoding='utf-8'))['tool']['version'])")"
ZEIT="$(date +'%Y%m%d_%H%M%S')"
ZIEL="$ROOT/backups"
NAME="TOOL_2026_Multi_${VERSION}_SICHERUNG_${ZEIT}.zip"
mkdir -p "$ZIEL"

python3 - "$ROOT" "$ZIEL/$NAME" <<'PY_BACKUP'
from pathlib import Path
import sys, zipfile
root=Path(sys.argv[1]).resolve()
out=Path(sys.argv[2]).resolve()
ausschluss={'.git','.venv','backups','logs','berichte','tmp','release','__pycache__'}
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(root.rglob('*')):
        rel=p.relative_to(root)
        if any(part in ausschluss for part in rel.parts):
            continue
        if p.is_file() and p.resolve()!=out:
            z.write(p, rel)
PY_BACKUP

sha256sum "$ZIEL/$NAME" > "$ZIEL/$NAME.sha256"
printf '🟢 Sicherung erstellt: %s\n' "$ZIEL/$NAME"
printf '🟢 Prüfsumme: %s\n' "$ZIEL/$NAME.sha256"
