"""Make ``run.py`` importable from test modules.

``run.py`` is a single PEP 723 script at the repo root, not an installable
package, so it is not on ``sys.path`` by default. Pytest auto-discovers
``conftest.py`` before collecting any test modules, so this insertion runs
once and lets every test module use a plain top-level ``from run import ...``.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
