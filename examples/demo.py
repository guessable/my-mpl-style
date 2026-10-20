"""Render the demo figure used in the README.

Run from the repository root::

    python examples/demo.py

The script puts the checkout's ``src`` directory first on ``sys.path``, so it
always exercises the local sources even when an older release is installed.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if SRC.is_dir() and str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from my_mpl_style import ax_setting3D, plot_rc  # noqa: E402


def main(outfile: Path = ROOT / "docs" / "images" / "demo.png") -> None:
    plot_rc(grid=True, tick_direction="in")

    fig = plt.figure(figsize=(10, 4.2), dpi=150)

    # --- 2D panel: colour cycle, serif fonts and mathtext -------------------
    ax = fig.add_subplot(121)
    x = np.linspace(0.0, 2.0 * np.pi, 400)
    for k in range(4):
        ax.plot(x, np.sin(x + k * 0.5) * np.exp(-0.1 * x), label=rf"$\phi={k * 0.5:.1f}$")
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$\sin(x+\phi)\,e^{-0.1x}$")
    ax.set_title("2D defaults")
    ax.legend()

    # --- 3D panel: orthographic box with a grey back edge -------------------
    ax = fig.add_subplot(122, projection="3d")
    a = np.linspace(-1, 1, 200)
    xx, yy = np.meshgrid(a, a)
    zz = np.sin(np.pi * xx) * np.exp(yy)
    ax.plot_surface(xx, yy, zz, linewidth=0, antialiased=True, cmap="viridis")
    ax.set_title("3D defaults")
    ax_setting3D(
        ax,
        (-1, 1),
        (-1, 1),
        (float(zz.min()), float(zz.max())),
        xticks=[-1, -0.5, 0, 0.5, 1],
        yticks=[-1, -0.5, 0, 0.5, 1],
        zticks=[-2, 0, 2],
        box_aspect=(1, 1, 1),
    )

    outfile.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(outfile)  # savefig.dpi / bbox / pad_inches come from plot_rc
    plt.close(fig)
    print(f"wrote {outfile}")


if __name__ == "__main__":
    main()
