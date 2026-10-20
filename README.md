# my-mpl-style

[![PyPI](https://img.shields.io/pypi/v/my-mpl-style.svg)](https://pypi.org/project/my-mpl-style/)
[![Python versions](https://img.shields.io/pypi/pyversions/my-mpl-style.svg)](https://pypi.org/project/my-mpl-style/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/guessable/my-mpl-style/blob/main/LICENSE)

Two small helpers that give matplotlib figures a publication-ready look:

- `plot_rc()` applies a consistent rcParams preset — serif fonts, Computer
  Modern math, a MATLAB-like colour cycle, optional grid and tick direction,
  plus 300 dpi / tight-bbox save defaults.
- `ax_setting3D()` turns a 3D axes into a clean orthographic box with explicit
  tick positions and a grey back edge.

## Installation

```bash
pip install my-mpl-style
```

Requires Python 3.10+ and matplotlib 3.5+.

## Example

**2D lines and a 3D surface** — [`examples/demo.py`](https://github.com/guessable/my-mpl-style/blob/main/examples/demo.py)

![2D lines and a 3D surface rendered with the default my-mpl-style preset](https://raw.githubusercontent.com/guessable/my-mpl-style/main/docs/images/demo.png)

The default preset (serif text, Computer Modern math, the six-colour cycle,
light grid) combined with an orthographic `ax_setting3D()` box.

**Intersecting planes** — [`examples/Intersecting_planes.py`](https://github.com/guessable/my-mpl-style/blob/main/examples/Intersecting_planes.py)

![Three orthogonal colour slices drawn inside one 3D box](https://raw.githubusercontent.com/guessable/my-mpl-style/main/docs/images/intersecting_planes.png)

Three orthogonal colour slices inside a single 3D box, each drawn with
`contourf` and a shared colour bar.

**Isosurfaces** — [`examples/isosurface.py`](https://github.com/guessable/my-mpl-style/blob/main/examples/isosurface.py)

![Marching-cubes isosurfaces of phase-field snapshots](https://raw.githubusercontent.com/guessable/my-mpl-style/main/docs/images/isosurface.png)

Marching-cubes isosurfaces of the phase-field snapshots in
[`data/`](https://github.com/guessable/my-mpl-style/tree/main/data), shaded with
a `LightSource`. This example needs `scikit-image` (install with
`pip install "my-mpl-style[examples]"`) and the `data/*.npz` files from the
repository.

## Quick start

```python
import matplotlib.pyplot as plt
from my_mpl_style import plot_rc

plot_rc(grid=True)                 # serif + CM math, 300 dpi, tight bbox

fig, ax = plt.subplots()
ax.plot([0, 1, 2], [0, 1, 4], label="data")
ax.set(xlabel="$x$", ylabel="$y$")
ax.legend(frameon=False)

fig.savefig("figure.png")          # uses savefig.dpi=300, bbox="tight"
```

Every default can be overridden per call:

```python
plot_rc(
    save_dpi=600,
    save_bbox="standard",
    save_pad_inches=0.1,
    font_family="sans-serif",
    font_serif=["DejaVu Sans"],
)
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
ax_setting3D(
    ax,
    (-1, 1), (-1, 1), (z.min(), z.max()),
    xticks=[-1, -0.5, 0, 0.5, 1],
    yticks=[-1, -0.5, 0, 0.5, 1],
    zticks=[-2, 0, 2],
    box_aspect=(1, 1, 1),
)
plt.show()
```

Ticks are passed to `ax_setting3D()` rather than set separately with
`ax.set(xticks=...)`, so the grey back edge is computed after the final limits
and ticks are known.

## API

### `plot_rc(...)`

```python
plot_rc(
    grid=False,
    tick_direction="out",
    tick_right=False,
    tick_top=False,
    save_dpi=300,
    save_bbox="tight",
    save_pad_inches=0.05,
    font_family="serif",
    font_serif=("Arial", "Helvetica", "DejaVu Sans"),
)
```

Updates the global `matplotlib.rcParams`, so it affects every figure created
afterwards.

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `grid` | `bool` | `False` | Draw light major grid lines behind the artists. |
| `tick_direction` | `"in" \| "out"` | `"out"` | Direction of the tick marks on both axes. |
| `tick_right` | `bool` | `False` | Also show ticks and labels on the right y axis. |
| `tick_top` | `bool` | `False` | Also show ticks and labels on the top x axis. |
| `save_dpi` | `int` | `300` | Resolution used by `savefig`. |
| `save_bbox` | `"tight" \| "standard"` | `"tight"` | Bounding-box mode (stored as `None` for `"standard"`). |
| `save_pad_inches` | `float` | `0.05` | Padding around the tight bbox, in inches. |
| `font_family` | `str` | `"serif"` | Value for `font.family`; `"sans-serif"` switches faces. |
| `font_serif` | `Sequence[str]` | `("Arial", "Helvetica", "DejaVu Sans")` | Font candidates for the serif family. |

rcParams written by the preset:

| rcParam | Value |
| --- | --- |
| `font.family` | `font_family` |
| `font.serif` | `font_serif` |
| `mathtext.fontset` | `"cm"` |
| `axes.formatter.use_mathtext` | `True` |
| `axes.prop_cycle` | 6-colour palette: `#0072BD`, `#D95319`, `#7E2F8E`, `#77AC30`, `#4DBEEE`, `#A2142F` |
| `xtick.direction`, `ytick.direction` | `tick_direction` |
| `axes.grid` | `grid` |
| `savefig.dpi`, `savefig.bbox`, `savefig.pad_inches` | `save_dpi`, `save_bbox`, `save_pad_inches` |
| `grid.linewidth`, `grid.alpha`, `axes.grid.which`, `axes.axisbelow` | `0.5`, `0.3`, `"major"`, `True` — only when `grid=True` |
| `ytick.right`, `ytick.labelright` | `True` — only when `tick_right=True` |
| `xtick.top`, `xtick.labeltop` | `True` — only when `tick_top=True` |

### `ax_setting3D(...)`

```python
ax_setting3D(
    ax,
    xlim, ylim, zlim,
    xticks, yticks, zticks,
    aspect="equal",
    box_aspect=None,
    xticks_pad=-5,
    yticks_pad=-5,
    zticks_pad=0,
)
```

Makes the panes transparent, thins the grid and tick marks, aligns the tick
labels next to their axes, sets the tick positions and limits, and draws the
grey back edge of the box.

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `ax` | `Axes3D` | — | Axes created with `projection="3d"`. |
| `xlim`, `ylim`, `zlim` | `Sequence[float]` | — | Axis limits. |
| `xticks`, `yticks`, `zticks` | `Sequence[float]` | — | Tick positions for each axis. |
| `aspect` | `"auto" \| "equal"` | `"equal"` | Data aspect. |
| `box_aspect` | `Sequence[float] \| None` | `None` | Ratio of the axes box along x, y and z. |
| `xticks_pad`, `yticks_pad`, `zticks_pad` | `float` | `-5`, `-5`, `0` | Padding between axis and tick labels, in points. |

## Development

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -e ".[dev,examples]"

pytest
python examples/demo.py          # regenerate docs/images/demo.png
python -m build
twine check dist/*
```

`examples/demo.py` prepends `src/` to `sys.path`, so it always renders with the
checkout's code even when an older release is installed in site-packages.

## Changelog

See [CHANGELOG.md](https://github.com/guessable/my-mpl-style/blob/main/CHANGELOG.md).

## License

MIT © 2026 chengtau
