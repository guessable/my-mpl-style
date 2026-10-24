"""Internal helpers shared by :mod:`my_mpl_style`.

Nothing in this module is part of the public API; the two public functions
live in :mod:`my_mpl_style._style`.

The 3D helpers wrap mplot3d's private tick hooks. Matplotlib 3.11.2 replaced
``_draw_ticks`` with ``_get_updated_ticks``; both signatures are supported so
the style works from matplotlib 3.10 through 3.11.x.
"""

from __future__ import annotations

import numpy as np
from mpl_toolkits.mplot3d import proj3d

#: Default colour cycle (MATLAB-like palette).
COLOR_ORDER: tuple[str, ...] = ("#0072BD", "#D95319", "#7E2F8E", "#77AC30", "#4DBEEE", "#A2142F")


def _finite_scalar(value, name, *, nonnegative=False):
    """Validate a numeric scalar before making any changes to the axes."""
    try:
        array = np.asarray(value, dtype=float)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{name} must be a finite scalar") from error
    if array.ndim != 0 or not np.isfinite(array) or (nonnegative and array < 0):
        qualifier = "finite and non-negative" if nonnegative else "finite"
        raise ValueError(f"{name} must be {qualifier}, got {value!r}")
    return float(array)


def _screen_points(ax, points):
    """Project transformed 3D coordinates to display coordinates."""
    x, y, _ = proj3d.proj_transform(*np.asarray(points).T, ax.M)
    return ax.transData.transform(np.column_stack((x, y)))


class _ProjectedGeometry:
    """Cache the projected box geometry once per axes draw.

    The projection matrix object changes on each mplot3d draw. Sharing this
    cache between the three axis hooks avoids projecting the same box three
    times, while keeping different subplots independent.
    """

    def __init__(self, ax):
        self.ax = ax
        self.matrix = None
        self.bounds = None
        self.longest = 0.0

    def update(self, axis):
        bounds = tuple(self.ax.bbox.bounds)
        if self.matrix is self.ax.M and self.bounds == bounds:
            return
        low, high, _, highs = axis._get_coord_info()
        far = np.where(highs, high, low)
        near = np.where(highs, low, high)
        points = [
            point
            for other in (self.ax.xaxis, self.ax.yaxis, self.ax.zaxis)
            for point in other._get_axis_line_edge_points(far, near)
        ]
        edges = _screen_points(self.ax, points).reshape(3, 2, 2)
        self.longest = float(np.linalg.norm(edges[:, 1] - edges[:, 0], axis=1).max())
        self.matrix, self.bounds = self.ax.M, bounds


class _TickLineDraw:
    """Set the final display-space length without moving the axis anchor."""

    def __init__(self, extension, line):
        self.extension, self.line = extension, line
        self.original = line.draw

    def __call__(self, renderer):
        line, extension = self.line, self.extension
        if line.get_visible() and extension.pixel_length > 0:
            points = line.get_xydata()
            if len(points) == 2:
                transform = line.get_transform()
                projected = transform.transform(points)
                anchor = projected[0]
                endpoint = anchor + extension.label_direction * extension.pixel_length
                adjusted = transform.inverted().transform([anchor, endpoint])
                line.set_data(adjusted[:, 0], adjusted[:, 1])
        return self.original(renderer)


class _ZTickLabel:
    """Position a z-axis tick label beyond its projected tick endpoint.

    The position and alignment are updated immediately before the text is
    drawn, so they follow changes to the view, figure size and tick length.

    Parameters
    ----------
    extension : _AxisTickExtension
        Tick extension that supplies the fallback outward direction.
    tick : matplotlib.axis.Tick
        Tick whose outer endpoint anchors the label.
    text : matplotlib.text.Text
        Tick label to position before calling its original draw method.
    """

    def __init__(self, extension, tick, text):
        self.extension, self.tick, self.text = extension, tick, text
        self.original = text.draw

    def __call__(self, renderer):
        text = self.text
        if text.get_visible():
            line = self.tick.tick1line
            ends = line.get_transform().transform(line.get_xydata())
            outward = ends[-1] - ends[0]
            length = np.linalg.norm(outward)
            direction = outward / length if length > 1e-9 else self.extension.label_direction
            gap = renderer.points_to_pixels(max(0.0, 2.0 + self.tick.get_pad()))
            position = ends[-1] + direction * gap
            text.set_position(text.get_transform().inverted().transform(position))
            if abs(direction[0]) < 0.25:
                text.set_ha("center")
                text.set_va("bottom" if direction[1] >= 0 else "top")
            else:
                text.set_ha("right" if direction[0] < 0 else "left")
                text.set_va("center")
        return self.original(renderer)


class _AxisTickExtension:
    """Set projected tick lengths, with custom endpoint labels on z only.

    Tick lengths are recomputed from the projected axes at each draw, and
    z-axis labels follow the outer endpoints. X and y labels retain their
    original positions and alignment. The hook is installed on the supplied
    axis instance and reused when the style is applied again.

    Matplotlib 3.11.2 replaced ``_draw_ticks`` with ``_get_updated_ticks``;
    the extension wraps whichever hook the running version provides.

    Parameters
    ----------
    axis : mpl_toolkits.mplot3d.axis3d.Axis
        Axis whose tick drawing is wrapped.
    length : float
        Tick length as a fraction of the longest projected axis.
    geometry : _ProjectedGeometry
        Per-subplot cache shared by the x, y and z tick hooks.
    """

    def __init__(self, axis, length, geometry):
        self.axis = axis
        self.length = length
        self.geometry = geometry
        self.pixel_length = 0.0
        self.label_direction = np.array([-1.0, 0.0])
        self.original_tickdir = axis._get_tickdir
        if axis.axis_name == "z":
            axis._get_tickdir = self._tickdir

        if hasattr(axis, "_get_updated_ticks"):
            self.original = axis._get_updated_ticks
            axis._get_updated_ticks = self._updated_ticks
        elif hasattr(axis, "_draw_ticks"):
            self.original = axis._draw_ticks
            axis._draw_ticks = self._draw_ticks
        else:  # pragma: no cover - guarded by the caller as well
            raise RuntimeError("This style requires Matplotlib >= 3.10")

    def _tickdir(self, position):
        # Preserve native x/y directions; extend z ticks along y.
        if self.axis.axis_name == "z" and position == "default" and self.axis.axes._vertical_axis == 2:
            return 1
        return self.original_tickdir(position)

    def _updated_ticks(self, edgep1, centers, deltas, highs, deltas_per_point, pos):
        self._apply(edgep1, centers, deltas, highs, pos)
        return self.original(edgep1, centers, deltas, highs, deltas_per_point, pos)

    def _draw_ticks(self, renderer, edgep1, centers, deltas, highs, deltas_per_point, pos):
        self._apply(edgep1, centers, deltas, highs, pos)
        return self.original(renderer, edgep1, centers, deltas, highs, deltas_per_point, pos)

    def _apply(self, edgep1, centers, deltas, highs, pos):
        axis = self.axis
        ax = axis.axes
        self.geometry.update(axis)
        dimension = axis._get_tickdir(pos)
        anchor = np.array(edgep1, dtype=float)
        anchor[axis._axinfo["i"]] = centers[axis._axinfo["i"]]
        tick_delta = deltas[dimension] * (1 if highs[dimension] else -1)

        # Derive the direction from the matrix rather than subtracting two
        # large data coordinates, e.g. an axis spanning 1e12 to 1e12 + 1.
        outward_sign = 1.0 if anchor[dimension] > centers[dimension] else -1.0
        if np.all(ax.M[3, :3] == 0):
            vector = ax.M[:2, dimension] * abs(deltas[dimension]) * outward_sign / ax.M[3, 3]
            scale = np.max(np.abs(vector))
            vector = vector / scale if scale > 0 else vector
            projected_direction = np.diff(ax.transData.transform([[0, 0], vector]), axis=0)[0]
            reference = np.max(np.abs(ax.M[:2, :3] * np.abs(deltas)[None, :] / ax.M[3, 3]))
            visible = scale > 1e-12 * reference
        else:
            # Preserve the local direction if the caller later uses perspective.
            tip = anchor.copy()
            tip[dimension] += outward_sign * abs(deltas[dimension])
            projected_direction = np.diff(_screen_points(ax, [anchor, tip]), axis=0)[0]
            visible = np.linalg.norm(projected_direction) > 1e-9
        unit_length = np.linalg.norm(projected_direction)
        if visible and unit_length > 1e-9:
            self.label_direction = projected_direction / unit_length
            self.pixel_length = self.length * self.geometry.longest
        else:
            self.pixel_length = 0.0

        # Native drawing still supplies tick anchors and original x/y labels;
        # the line wrapper normalises only the final visible short segments.
        factor = 0.2
        if (anchor[dimension] - centers[dimension]) * tick_delta > 0:
            factor = -factor
        axis._axinfo["tick"].update(inward_factor=factor, outward_factor=0.0)
        for tick in axis._update_ticks():
            if not isinstance(tick.tick1line.draw, _TickLineDraw):
                tick.tick1line.draw = _TickLineDraw(self, tick.tick1line)
            if axis.axis_name == "z":
                for text in (tick.label1, tick.label2):
                    if not isinstance(text.draw, _ZTickLabel):
                        text.draw = _ZTickLabel(self, tick, text)
