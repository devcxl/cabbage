#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BIN_DIR="${CABBAGE_BIN_DIR:-$HOME/.local/bin}"

if ! python3 -c 'import yaml' >/dev/null 2>&1; then
  python3 -m pip install --user 'PyYAML>=6.0'
fi

mkdir -p "$BIN_DIR"
cat > "$BIN_DIR/cabbage" <<EOF
#!/usr/bin/env bash
export PYTHONPATH="$ROOT\${PYTHONPATH:+:\$PYTHONPATH}"
exec python3 -m cabbage_cli "\$@"
EOF
chmod +x "$BIN_DIR/cabbage"
printf 'installed: %s/cabbage\n' "$BIN_DIR"
