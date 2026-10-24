"""Tests for :mod:`my_mpl_style`."""

import matplotlib

matplotlib.use("Agg")

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import pytest

import my_mpl_style
from my_mpl_style import ax_setting3D, plot_rc
from my_mpl_style._style import __all__ as STYLE_ALL
from my_mpl_style._utils import _AxisTickExtension


@pytest.fixture(autouse=True)
def _restore_rcparams():
    """Keep the global rcParams untouched between tests."""
    saved = plt.rcParams.copy()
    yield
    plt.rcParams.update(saved)


def _axes3d():
    fig = plt.figure()
    return fig, fig.add_subplot(111, projection="3d")


def test_plot_rc_defaults():
    plt.rcParams["axes.grid"] = True
    plt.rcParams["savefig.dpi"] = 100

    plot_rc()

    assert plt.rcParams["axes.grid"] is False
    assert plt.rcParams["xtick.direction"] == "out"
    assert plt.rcParams["ytick.direction"] == "out"
    assert list(plt.rcParams["font.serif"])[0] == "Arial"
    assert list(plt.rcParams["font.family"]) == ["serif"]
    assert plt.rcParams["mathtext.fontset"] == "cm"
    assert plt.rcParams["savefig.dpi"] == 300
    assert plt.rcParams["savefig.bbox"] == "tight"
    assert plt.rcParams["savefig.pad_inches"] == pytest.approx(0.05)


def test_plot_rc_options():
    plot_rc(grid=True, tick_direction="in", tick_right=True, tick_top=True)

    assert plt.rcParams["axes.grid"] is True
    assert plt.rcParams["axes.grid.which"] == "major"
    assert plt.rcParams["xtick.direction"] == "in"
    assert plt.rcParams["ytick.direction"] == "in"
    assert plt.rcParams["ytick.right"] is True
    assert plt.rcParams["ytick.labelright"] is True
    assert plt.rcParams["xtick.top"] is True
    assert plt.rcParams["xtick.labeltop"] is True


def test_plot_rc_overrides_savefig_and_fonts():
    plot_rc(
        save_dpi=600,
        save_bbox="standard",
        save_pad_inches=0.1,
        font_family="sans-serif",
        font_serif=["DejaVu Sans"],
    )

    assert plt.rcParams["savefig.dpi"] == 600
    # matplotlib normalises the "standard" bbox mode to None.
    assert plt.rcParams["savefig.bbox"] is None
    assert plt.rcParams["savefig.pad_inches"] == pytest.approx(0.1)
    assert list(plt.rcParams["font.family"]) == ["sans-serif"]
    assert list(plt.rcParams["font.serif"]) == ["DejaVu Sans"]


def test_plot_rc_colour_cycle():
    plot_rc()

    colours = [entry["color"] for entry in plt.rcParams["axes.prop_cycle"]]

    assert colours[0] == "#0072BD"
    assert len(colours) == 6


def test_plot_rc_rejects_unknown_tick_direction():
    with pytest.raises(ValueError, match="tick_direction"):
        plot_rc(tick_direction="sideways")


def test_only_two_public_functions_are_exposed():
    assert my_mpl_style.__all__ == ["plot_rc", "ax_setting3D"]
    assert STYLE_ALL == ["plot_rc", "ax_setting3D"]


def test_ax_setting3d_styles_axes():
    fig, ax = _axes3d()
    ax.plot([0.0, 1.0], [0.0, 1.0], [0.0, 1.0])

    ax_setting3D(
        ax,
        (0, 1),
        (0, 1),
        (-1, 1),
        xticks=[0, 0.5, 1],
        yticks=[0, 1],
        zticks=[-1, 0, 1],
        box_aspect=(2, 1, 1),
    )

    assert ax.get_xlim() == (0.0, 1.0)
    assert ax.get_zlim() == (-1.0, 1.0)
    assert [float(v) for v in ax.get_xticks()] == [0.0, 0.5, 1.0]
    assert [float(v) for v in ax.get_zticks()] == [-1.0, 0.0, 1.0]
    assert ax.get_box_aspect() is not None

    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        assert axis.pane.fill is False
        assert axis._axinfo["grid"]["linewidth"] == 0.2
        assert axis._axinfo["tick"]["outward_factor"] == 0.0

    assert ax.xaxis.get_major_ticks()[0].label1.get_ha() == "left"
    assert ax.yaxis.get_major_ticks()[0].label1.get_ha() == "right"
    assert ax.zaxis.get_major_ticks()[0].label1.get_va() == "center_baseline"

    fig.canvas.draw()
    plt.close(fig)


def test_ax_setting3d_installs_hooks_once():
    fig, ax = _axes3d()
    args = ((0, 1), (0, 1), (0, 1))
    ticks = dict(xticks=[0, 1], yticks=[0, 1], zticks=[0, 1])

    ax_setting3D(ax, *args, **ticks)

    hooks = (ax.xaxis._draw_ticks, ax.yaxis._draw_ticks, ax.zaxis._draw_ticks)
    assert all(isinstance(hook, _AxisTickExtension) for hook in hooks)

    ax_setting3D(ax, *args, **ticks, xtick_length=0.05)

    assert (ax.xaxis._draw_ticks, ax.yaxis._draw_ticks, ax.zaxis._draw_ticks) == hooks
    assert ax.xaxis._draw_ticks.length == pytest.approx(0.05)

    fig.canvas.draw()
    plt.close(fig)


def test_ax_setting3d_box_on_uses_axis_colour():
    fig, ax = _axes3d()
    args = ((0, 1), (0, 1), (0, 1))
    ticks = dict(xticks=[0, 1], yticks=[0, 1], zticks=[0, 1])

    ax_setting3D(ax, *args, **ticks)
    assert tuple(ax.xaxis.pane.get_edgecolor()) == pytest.approx(mcolors.to_rgba("gray"))

    ax_setting3D(ax, *args, **ticks, box_on=True)
    assert tuple(ax.xaxis.pane.get_edgecolor()) == pytest.approx(
        mcolors.to_rgba(ax.xaxis.line.get_color())
    )

    plt.close(fig)


def test_ax_setting3d_rejects_non_3d_axes():
    fig, ax = plt.subplots()
    with pytest.raises(TypeError, match="Axes3D"):
        ax_setting3D(ax, (0, 1), (0, 1), (0, 1), xticks=[0, 1], yticks=[0, 1], zticks=[0, 1])
    plt.close(fig)


@pytest.mark.parametrize(
    "overrides",
    [
        {"xlim": (0, 1, 2)},
        {"ylim": (0, float("nan"))},
        {"xticks": [0, float("inf")]},
        {"xticks": 0},
        {"ztick_length": -0.1},
        {"zticks_pad": float("nan")},
        {"box_aspect": (1, 0, 1)},
        {"aspect": "square"},
    ],
)
def test_ax_setting3d_validates_arguments(overrides):
    fig, ax = _axes3d()
    kwargs = dict(xlim=(0, 1), ylim=(0, 1), zlim=(0, 1), xticks=[0, 1], yticks=[0, 1], zticks=[0, 1])
    kwargs.update(overrides)

    with pytest.raises((TypeError, ValueError)):
        ax_setting3D(ax, **kwargs)

    plt.close(fig)
