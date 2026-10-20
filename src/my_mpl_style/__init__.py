"""Publication-oriented matplotlib style helpers.

``my-mpl-style`` bundles two small helpers that make the default matplotlib
output look closer to a journal figure: :func:`plot_rc` applies a consistent
rcParams preset (serif fonts, CM math, MATLAB-like colours, optional grid and
inward ticks, 300 dpi tight-bbox saving), and :func:`ax_setting3D` turns a 3D
axes into a clean, orthographic box with explicit tick positions.

Basic usage::

    import matplotlib.pyplot as plt
    from my_mpl_style import plot_rc

    plot_rc(grid=True)
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2], [0, 1, 4])
    fig.savefig("figure.png")  # 300 dpi, tight bounding box
"""

from ._style import ax_setting3D, plot_rc

__all__ = ["plot_rc", "ax_setting3D"]
__version__ = "0.2.2"
