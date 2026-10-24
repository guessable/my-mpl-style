"""Public style helpers exported by :mod:`my_mpl_style`.

Only :func:`plot_rc` and :func:`ax_setting3D` are defined here; their private
machinery lives in :mod:`my_mpl_style._utils`.
"""

from __future__ import annotations

from typing import Literal, Sequence

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

from ._utils import COLOR_ORDER, _AxisTickExtension, _ProjectedGeometry, _finite_scalar

__all__ = ["plot_rc", "ax_setting3D"]


def plot_rc(
    grid: bool = False,
    tick_direction: Literal["in", "out"] = "out",
    tick_right: bool = False,
    tick_top: bool = False,
    save_dpi: int = 300,
    save_bbox: Literal["tight", "standard"] = "tight",
    save_pad_inches: float = 0.05,
    font_family: str = "serif",
    font_serif: Sequence[str] = ("Arial", "Helvetica", "DejaVu Sans"),
) -> None:
    """Apply a publication-oriented style to matplotlib's global rcParams.

    The function updates :data:`matplotlib.rcParams` in place, so it affects
    every figure created afterwards. Besides fonts, colours and ticks it also
    sets the ``savefig`` defaults (300 dpi, tight bounding box, 0.05 in
    padding), so ``fig.savefig("figure.png")`` produces a print-ready file
    without further arguments.

    Parameters
    ----------
    grid : bool, default: False
        If ``True``, draw light major grid lines behind the artists.
    tick_direction : {"in", "out"}, default: "out"
        Direction of the tick marks on both axes.
    tick_right : bool, default: False
        Also show ticks and tick labels on the right-hand y axis.
    tick_top : bool, default: False
        Also show ticks and tick labels on the top x axis.
    save_dpi : int, default: 300
        Resolution used by :meth:`~matplotlib.figure.Figure.savefig`.
    save_bbox : str, default: "tight"
        Bounding-box mode used when saving; matplotlib accepts ``"tight"``
        or ``"standard"`` and normalises ``"standard"`` to ``None``.
    save_pad_inches : float, default: 0.05
        Padding around the tight bounding box, in inches.
    font_family : str, default: "serif"
        Value for ``font.family``; use ``"sans-serif"`` to switch to a
        sans-serif face.
    font_serif : sequence of str, default: ("Arial", "Helvetica", "DejaVu Sans")
        Font candidates used when ``font.family`` is ``"serif"``.

    Raises
    ------
    ValueError
        If ``tick_direction`` is neither ``"in"`` nor ``"out"``.

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> from my_mpl_style import plot_rc
    >>> plot_rc(grid=True, tick_direction="in", save_dpi=600)
    >>> fig, ax = plt.subplots()
    >>> ax.plot([0, 1], [0, 1])
    >>> fig.savefig("figure.png")  # 600 dpi, tight bounding box
    """
    if tick_direction not in ("in", "out"):
        raise ValueError(f"tick_direction must be 'in' or 'out', got {tick_direction!r}")

    rc: dict[str, object] = {
        "font.family": font_family,
        "font.serif": font_serif,
        "mathtext.fontset": "cm",
        "axes.formatter.use_mathtext": True,
        "axes.prop_cycle": plt.cycler(color=list(COLOR_ORDER)),
        "xtick.direction": tick_direction,
        "ytick.direction": tick_direction,
        "axes.grid": bool(grid),
        "savefig.dpi": save_dpi,
        "savefig.bbox": save_bbox,
        "savefig.pad_inches": save_pad_inches,
    }

    if grid:
        rc.update(
            {
                "grid.linewidth": 0.5,
                "grid.alpha": 0.3,
                "axes.grid.which": "major",
                "axes.axisbelow": True,
            }
        )
    if tick_right:
        rc.update({"ytick.right": True, "ytick.labelright": True})
    if tick_top:
        rc.update({"xtick.top": True, "xtick.labeltop": True})

    plt.rcParams.update(rc)


def ax_setting3D(
    ax: Axes3D,
    xlim: Sequence[float],
    ylim: Sequence[float],
    zlim: Sequence[float],
    xticks: Sequence[float],
    yticks: Sequence[float],
    zticks: Sequence[float],
    aspect: Literal["auto", "equal"] = "equal",
    box_aspect: Sequence[float] | None = None,
    xticks_pad: float = -5,
    yticks_pad: float = -5,
    zticks_pad: float = 0,
    box_on: bool = False,
    ztick_length: float = 0.02,
    xtick_length: float = 0.02,
    ytick_length: float = 0.02,
) -> None:
    """Style a 3D axes with a MATLAB-like view, box and tick marks.

    The axes use orthographic projection and the MATLAB default 3D view.
    Pane fills are removed and the grid lines are thinned. Tick lengths on
    all three axes are scaled to the longest projected axis. X and y tick
    directions and label positions are preserved. Z ticks extend along y,
    with their numeric labels placed beyond the outer endpoints.

    Parameters
    ----------
    ax : Axes3D
        A 3D axes created with ``projection="3d"``.
    xlim, ylim, zlim : sequence of float
        Axis limits.
    xticks, yticks, zticks : sequence of float
        Tick positions for each axis.
    aspect : {"auto", "equal"}, default: "equal"
        Data aspect passed to :meth:`~mpl_toolkits.mplot3d.axes3d.Axes3D.set_aspect`.
    box_aspect : sequence of float or None, default: None
        If given, the ratio of the axes box lengths along x, y and z.
    xticks_pad, yticks_pad : float, default: -5
        Padding between the x or y axis and its tick labels, in points.
    zticks_pad : float, default: 0
        Additional padding beyond each z tick's outer endpoint, in points.
        The total gap is ``max(0, 2 + zticks_pad)`` points.
    box_on : bool, default: False
        If ``True``, use the axis line colours for the pane outlines.
        Otherwise, draw the pane outlines in grey.
    ztick_length, xtick_length, ytick_length : float, default: 0.02
        Tick length on each axis as a fraction of the longest projected
        axis. Lengths are recomputed whenever the axes are drawn.

    Raises
    ------
    TypeError
        If ``ax`` is not a 3D axes.
    ValueError
        If limits or ticks contain non-finite values, a tick length is
        negative, or ``box_aspect`` does not contain three positive values.

    Notes
    -----
    Tick directions and labels use private mplot3d draw hooks. The hooks
    are reused when this function is called again on the same axes.
    The y-direction override applies to the default tick position with z
    as the vertical axis; other configurations retain their original direction.
    Each subplot has its own geometry cache. Importing this module does not
    create figures or change global plotting settings.

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> import numpy as np
    >>> from my_mpl_style import ax_setting3D
    >>> a = np.linspace(-1, 1, 50)
    >>> x, y = np.meshgrid(a, a)
    >>> z = np.sin(np.pi * x) * np.cos(np.pi * y)
    >>> fig = plt.figure()
    >>> ax = fig.add_subplot(111, projection="3d")
    >>> ax.plot_surface(x, y, z)
    >>> ax_setting3D(
    ...     ax,
    ...     (-1, 1),
    ...     (-1, 1),
    ...     (-1, 1),
    ...     xticks=[-1, 0, 1],
    ...     yticks=[-1, 0, 1],
    ...     zticks=[-1, 0, 1],
    ...     box_on=True,
    ...     xtick_length=0.02,
    ...     ytick_length=0.02,
    ...     ztick_length=0.02,
    ...     zticks_pad=2,
    ... )
    """
    if not isinstance(ax, Axes3D):
        raise TypeError("ax must be an Axes3D created with projection='3d'")
    if aspect not in ("auto", "equal"):
        raise ValueError("aspect must be 'auto' or 'equal'")
    axes = (ax.xaxis, ax.yaxis, ax.zaxis)
    if not all(hasattr(axis, "_draw_ticks") and hasattr(axis, "_get_tickdir") for axis in axes):
        raise RuntimeError("This style requires the mplot3d drawing hooks in Matplotlib >= 3.10")
    lengths = {
        name: _finite_scalar(value, name + "tick_length", nonnegative=True)
        for name, value in zip("xyz", (xtick_length, ytick_length, ztick_length))
    }
    pads = [_finite_scalar(value, name + "ticks_pad") for name, value in zip("xyz", (xticks_pad, yticks_pad, zticks_pad))]
    limits, ticks = {}, {}
    for name, bounds, values in zip("xyz", (xlim, ylim, zlim), (xticks, yticks, zticks)):
        bounds = np.asarray(bounds, dtype=float)
        values = np.asarray(values, dtype=float)
        if bounds.shape != (2,) or not np.isfinite(bounds).all():
            raise ValueError(f"{name}lim must contain two finite values")
        if values.ndim != 1 or not np.isfinite(values).all():
            raise ValueError(f"{name}ticks must be a one-dimensional finite sequence")
        limits[name], ticks[name] = bounds.copy(), values.copy()
    if box_aspect is not None:
        box_aspect = np.array(box_aspect, dtype=float, copy=True)
        if box_aspect.shape != (3,) or not np.isfinite(box_aspect).all() or np.any(box_aspect <= 0):
            raise ValueError("box_aspect must contain three finite positive values")

    ax.set_proj_type("ortho")
    ax.view_init(elev=30, azim=-127.5)
    for name, pad in zip("xyz", pads):
        ax.tick_params(axis=name, pad=pad)

    for axis in axes:
        axis._axinfo["grid"]["linewidth"] = 0.2
        axis._axinfo["tick"]["inward_factor"] = 0.2
        axis._axinfo["tick"]["outward_factor"] = 0.0
        axis.pane.fill = False
        axis.pane.set_closed(True)
        axis.pane.set_alpha(None)
        axis.pane.set_linewidth(axis.line.get_linewidth())
        axis.pane.set_edgecolor(axis.line.get_color() if box_on else "gray")

    # Set ticks first: Matplotlib otherwise expands explicit limits to fit them.
    for name, axis in zip("xyz", axes):
        axis.set_ticks(ticks[name])
        getattr(ax, "set_" + name + "lim")(limits[name])
    ax.set_aspect(aspect)
    if box_aspect is not None:
        ax.set_box_aspect(box_aspect)

    # Avoid get_ticklabels() here: it assigns raw tick values as temporary 2D
    # positions before the first draw, which can upset constrained_layout.
    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_ha("left")
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_ha("right")
    for tick in ax.zaxis.get_major_ticks():
        tick.label1.set_va("center_baseline")

    geometry = getattr(ax, "_style3d_geometry", None)
    if not isinstance(geometry, _ProjectedGeometry):
        geometry = ax._style3d_geometry = _ProjectedGeometry(ax)
    geometry.matrix = None
    for name, length in lengths.items():
        axis = getattr(ax, name + "axis")
        if isinstance(axis._draw_ticks, _AxisTickExtension):
            axis._draw_ticks.length = length
        else:
            axis._draw_ticks = _AxisTickExtension(axis, length, geometry)
