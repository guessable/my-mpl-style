# my-mpl-style

[![PyPI](https://img.shields.io/pypi/v/my-mpl-style.svg)](https://pypi.org/project/my-mpl-style/)
[![Python versions](https://img.shields.io/pypi/pyversions/my-mpl-style.svg)](https://pypi.org/project/my-mpl-style/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Two small helpers that give matplotlib figures a publication-ready look:
`plot_rc()` sets a consistent rcParams preset (serif fonts, Computer Modern
math, a MATLAB-like colour cycle, optional grid and inward ticks), and
`ax_setting3D()` turns a 3D axes into a clean orthographic box.

## Installation

```bash
pip install my-mpl-style
```

Requires Python 3.10+ and matplotlib 3.5+.

## Quick start

```python
import matplotlib.pyplot as plt
from my_mpl_style import plot_rc

plot_rc(grid=True)

fig, ax = plt.subplots()
ax.plot([0, 1, 2], [0, 1, 4], label="data")
ax.set(xlabel="$x$", ylabel="$y$")
ax.legend(frameon=False)
plt.show()
```

### 3D axes

```python
import matplotlib.pyplot as plt
import numpy as np
from my_mpl_style import ax_setting3D

a = np.linspace(-1, 1, 200)
x, y = np.meshgrid(a, a)
z = np.sin(np.pi * x) * np.exp(y)

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.plot_surface(x, y, z, linewidth=0, antialiased=True)
ax_setting3D(ax, (-1, 1), (-1, 1), (z.min(), z.max()), box_aspect=(1, 1, 1))
plt.show()
```

## API

### `plot_rc(grid=False, tick_direction="out", tick_right=False, tick_top=False)`

Updates the global `matplotlib.rcParams`, so it affects every figure created
afterwards.

| Parameter        | Type            | Default | Description                                        |
| ---------------- | --------------- | ------- | -------------------------------------------------- |
| `grid`           | `bool`          | `False` | Draw light major grid lines behind the artists.     |
| `tick_direction` | `"in" \| "out"` | `"out"` | Direction of the tick marks.                        |
| `tick_right`     | `bool`          | `False` | Also show ticks and labels on the right y axis.     |
| `tick_top`       | `bool`          | `False` | Also show ticks and labels on the top x axis.       |

### `ax_setting3D(ax, xlim, ylim, zlim, aspect="equal", box_aspect=None, xticks_pad=-5, yticks_pad=-5, zticks_pad=0)`

Makes the panes transparent, thins the grid and tick marks, aligns the tick
labels next to their axes, and draws the grey back edge of the box.

| Parameter    | Type                        | Default   | Description                                 |
| ------------ | --------------------------- | --------- | ------------------------------------------- |
| `ax`         | `Axes` (3D)                 | —         | A 3D axes created with `projection="3d"`.   |
| `xlim`, `ylim`, `zlim` | `Sequence[float]`  | —         | Axis limits.                                |
| `aspect`     | `"auto" \| "equal"`         | `"equal"` | Data aspect.                                |
| `box_aspect` | `Sequence[float] \| None`   | `None`    | Ratio of the axes box along x, y and z.     |
| `*_pad`      | `float`                     | `-5, -5, 0` | Padding between axis and tick labels (pt). |

## Development

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -e ".[dev]"

pytest
python examples/demo.py          # regenerate docs/images/demo.png
python -m build
twine check dist/*
```

## License

MIT © 2026 chengtau
