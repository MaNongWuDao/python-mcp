from __future__ import annotations

import sys


print("intentional failure", file=sys.stderr)
raise SystemExit(3)
