"""Print the canonical comparison of all fourteen fictional baseline cases."""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from opportunity_cookbook.comparison import render_comparison


if __name__ == "__main__":
    print(render_comparison())
