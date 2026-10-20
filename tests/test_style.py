"""Tests for :mod:`my_mpl_style`."""

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pytest

from my_mpl_style import ax_setting3D, plot_rc


@pytest.fixture(autouse=True)
def _restore_rcparams():
    """Keep the global rcParams untouched between tests."""
    saved = plt.rcParams.copy()
    yield
    plt.rcParams.update(saved)


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


def test_ax_setting3d_returns_clean_box():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.plot([0.0, 1.0], [0.0, 1.0], [0.0, 1.0])

    ax_setting3D(
        ax,
        (0, 1),
        (0, 1),
        (0, 1),
        xticks=[0, 1],
        yticks=[0, 1],
        zticks=[0, 1],
        box_aspect=(1, 1, 1),
    )

    assert ax.get_xlim() == (0.0, 1.0)
    assert [float(v) for v in ax.get_xticks()] == [0.0, 1.0]
    assert [float(v) for v in ax.get_yticks()] == [0.0, 1.0]
    assert [float(v) for v in ax.get_zticks()] == [0.0, 1.0]
    assert ax.get_box_aspect() is not None
    assert hasattr(ax, "_box_edge")
    assert ax._box_edge in fig.artists

    # A second call must replace, not duplicate, the edge artist.
    ax_setting3D(ax, (0, 1), (0, 1), (0, 1), xticks=[0, 1], yticks=[0, 1], zticks=[0, 1])
    assert sum(artist is ax._box_edge for artist in fig.artists) == 1

    fig.canvas.draw()
    plt.close(fig)
