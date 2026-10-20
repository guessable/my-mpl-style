"""Core style helpers: global rcParams presets and 3D axes adjustments."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal, Sequence

import matplotlib.pyplot as plt

if TYPE_CHECKING:
    from mpl_toolkits.mplot3d import Axes3D

__all__ = ["plot_rc", "ax_setting3D"]

#: Default colour cycle (MATLAB-like palette).
COLOR_ORDER: tuple[str, ...] = ("#0072BD", "#D95319", "#7E2F8E", "#77AC30", "#4DBEEE", "#A2142F")


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
) -> None:
    """Style a 3D axes to look like a clean, orthogonal box.

    The panes are made transparent, the grid and tick marks are thinned, the
    out-of-plane back edge is drawn in grey, and the tick labels are aligned
    so that they sit next to their axes.

    Tick positions are passed in here rather than set with
    ``ax.set(xticks=...)``, so that the limits, the ticks and the grey back
    edge are all computed from the same final state of the axes.

    Parameters
    ----------
    ax : Axes3D
        A 3D axes created with ``projection="3d"``.
    xlim, ylim, zlim : sequence of float
        Axis limits.
    xticks, yticks, zticks : sequence of float
        Tick positions for each axis.
    aspect : {"auto", "equal"}, default: "equal"
        Data aspect passed to :meth:`~matplotlib.axes.Axes.set_aspect`.
    box_aspect : sequence of float or None, default: None
        If given, the ratio of the axes box lengths along x, y and z.
    xticks_pad, yticks_pad, zticks_pad : float, default: -5, -5, 0
        Padding between each axis and its tick labels, in points.

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> import numpy as np
    >>> from my_mpl_style import ax_setting3D
    >>> a = np.linspace(-1, 1, 50)
    >>> x, y = np.meshgrid(a, a)
    >>> z = np.sin(np.pi * x) * np.exp(y)
    >>> fig = plt.figure()
    >>> ax = fig.add_subplot(111, projection="3d")
    >>> ax.plot_surface(x, y, z)
    >>> ax_setting3D(
    ...     ax,
    ...     (-1, 1),
    ...     (-1, 1),
    ...     (z.min(), z.max()),
    ...     xticks=[-1, 0, 1],
    ...     yticks=[-1, 0, 1],
    ...     zticks=[-2, 0, 2],
    ... )
    """
    ax.set_proj_type("ortho")
    ax.view_init(elev=30, azim=-127.5)
    ax.tick_params(axis="x", pad=xticks_pad)
    ax.tick_params(axis="y", pad=yticks_pad)
    ax.tick_params(axis="z", pad=zticks_pad)

    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis._axinfo["grid"]["linewidth"] = 0.2
        axis._axinfo["tick"]["inward_factor"] = 0.2
        axis._axinfo["tick"]["outward_factor"] = 0.0
        axis.pane.set_edgecolor("gray")
        axis.pane.fill = False

    for tick in ax.xaxis.get_ticklabels():
        tick.set_horizontalalignment("left")
    for tick in ax.yaxis.get_ticklabels():
        tick.set_horizontalalignment("right")
    for tick in ax.zaxis.get_ticklabels():
        tick.set_verticalalignment("center_baseline")

    ax.set(xlim=xlim, ylim=ylim, zlim=zlim, aspect=aspect, xticks=xticks, yticks=yticks, zticks=zticks)
    if box_aspect is not None:
        ax.set(box_aspect=box_aspect)

    from matplotlib.lines import Line2D
    from mpl_toolkits.mplot3d import proj3d

    fig = ax.figure
    fig.canvas.draw()
    ax.M = ax.get_proj()

    x1, y0 = ax.get_xlim()[1], ax.get_ylim()[0]
    z0, z1 = ax.get_zlim()
    ends = [fig.transFigure.inverted().transform(ax.transData.transform(proj3d.proj_transform(x1, y0, z, ax.M)[:2])) for z in (z0, z1)]

    if hasattr(ax, "_box_edge"):
        ax._box_edge.remove()
    ax._box_edge = Line2D(
        [ends[0][0], ends[1][0]],
        [ends[0][1], ends[1][1]],
        transform=fig.transFigure,
        color="gray",
        lw=0.9,
        zorder=1000,
        alpha=0.6,
    )
    fig.add_artist(ax._box_edge)
