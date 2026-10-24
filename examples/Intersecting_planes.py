# ---------------------
#      "
#    '':''
#   ___:____      |\/|
# ,'        `.    \  /
# |  O        \___/  |
# ~^~^~^~^~^~^~^~^~^~^
# ---------------------
# @author: τ

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from my_mpl_style import plot_rc, ax_setting3D

plot_rc(save_dpi=500, save_pad_inches=0.15)

a, b = np.meshgrid(np.linspace(0, 1, 100), np.linspace(0, 1, 100))

# u = exp(-x**2 - y**2 - z**2)


def plot_ax(ax, x, y, z, data, zdir, norm, cmap="viridis"):
    n = 50
    if zdir == "z":
        ax.contourf(x[:n, :n], y[:n, :n], data[:n, :n], norm=norm, levels=100, zdir="z", offset=0.5, cmap=cmap)
        ax.contourf(x[:n, n - 1 :], y[:n, n - 1 :], data[:n, n - 1 :], norm=norm, levels=100, zdir="z", offset=0.5, cmap=cmap)
        ax.contourf(x[n - 1 :, :n], y[n - 1 :, :n], data[n - 1 :, :n], norm=norm, levels=100, zdir="z", offset=0.5, cmap=cmap)
        ax.contourf(
            x[n - 1 :, n - 1 :], y[n - 1 :, n - 1 :], data[n - 1 :, n - 1 :], norm=norm, levels=100, zdir="z", offset=0.5, cmap=cmap
        )
    elif zdir == "y":
        ax.contourf(x[:n, :n], data[:n, :n], z[:n, :n], norm=norm, levels=100, zdir="y", offset=0.5, cmap=cmap)
        ax.contourf(x[:n, n - 1 :], data[:n, n - 1 :], z[:n, n - 1 :], norm=norm, levels=100, zdir="y", offset=0.5, cmap=cmap)
        ax.contourf(x[n - 1 :, :n], data[n - 1 :, :n], z[n - 1 :, :n], norm=norm, levels=100, zdir="y", offset=0.5, cmap=cmap)
        ax.contourf(
            x[n - 1 :, n - 1 :], data[n - 1 :, n - 1 :], z[n - 1 :, n - 1 :], norm=norm, levels=100, zdir="y", offset=0.5, cmap=cmap
        )
    elif zdir == "x":
        ax.contourf(data[:n, :n], y[:n, :n], z[:n, :n], norm=norm, levels=100, zdir="x", offset=0.5, cmap=cmap)
        ax.contourf(data[:n, n - 1 :], y[:n, n - 1 :], z[:n, n - 1 :], norm=norm, levels=100, zdir="x", offset=0.5, cmap=cmap)
        ax.contourf(data[n - 1 :, :n], y[n - 1 :, :n], z[n - 1 :, :n], norm=norm, levels=100, zdir="x", offset=0.5, cmap=cmap)
        ax.contourf(
            data[n - 1 :, n - 1 :], y[n - 1 :, n - 1 :], z[n - 1 :, n - 1 :], norm=norm, levels=100, zdir="x", offset=0.5, cmap=cmap
        )


if __name__ == "__main__":
    fig = plt.figure(figsize=(10, 5))

    fig.subplots_adjust(wspace=0.1)

    # =======================================
    ax = fig.add_subplot(1, 2, 1, projection="3d")

    u1 = np.exp(-(a**2) - b**2 - 0.5**2)  # z = 0.5
    u2 = np.exp(-(a**2) - 0.5**2 - b**2)  # y = 0.5
    u3 = np.exp(-(0.5**2) - a**2 - b**2)  # x = 0.5

    norm = Normalize(vmin=min(u1.min(), u2.min(), u3.min()), vmax=max(u1.max(), u2.max(), u3.max()))
    plot_ax(ax, a, b, 0.5, u1, "z", norm)
    plot_ax(ax, a, 0.5, b, u2, "y", norm)
    plot_ax(ax, 0.5, a, b, u3, "x", norm)

    cm = ScalarMappable(norm=norm)
    cb = fig.colorbar(cm, ax=ax, shrink=0.5, aspect=14)
    cb.set_label(r"$u_{\rm NN}$", fontsize=13, labelpad=2)

    ax_setting3D(ax, (0, 1), (0, 1), (0, 1), [0, 0.5, 1], [0, 0.5, 1], [0, 0.5, 1])
    ax.set_xlabel(r"$x$", labelpad=-5), ax.set_ylabel(r"$y$", labelpad=-5), ax.set_zlabel(r"$z$", labelpad=-4)

    # =======================================
    ax = fig.add_subplot(1, 2, 2, projection="3d")

    u1 = np.exp(-(a**2) - b**2 - 0.5**2)  # z = 0.5
    u2 = np.exp(-(a**2) - 0.5**2 - b**2)  # y = 0.5
    u3 = np.exp(-(0.5**2) - a**2 - b**2)  # x = 0.5

    norm = Normalize(vmin=min(u1.min(), u2.min(), u3.min()), vmax=max(u1.max(), u2.max(), u3.max()))
    plot_ax(ax, a, b, 0.5, u1, "z", norm, cmap="plasma")
    plot_ax(ax, a, 0.5, b, u2, "y", norm, cmap="plasma")
    plot_ax(ax, 0.5, a, b, u3, "x", norm, cmap="plasma")

    cm = ScalarMappable(norm=norm, cmap="plasma")
    cb = fig.colorbar(cm, ax=ax, shrink=0.5, aspect=14)
    cb.set_label(r"$u_{\rm NN}$", fontsize=13, labelpad=2)

    ax_setting3D(ax, (0, 1), (0, 1), (0, 1), [0, 0.5, 1], [0, 0.5, 1], [0, 0.5, 1])
    ax.set_xlabel(r"$x$", labelpad=-5), ax.set_ylabel(r"$y$", labelpad=-5), ax.set_zlabel(r"$z$", labelpad=-4)

    plt.savefig("./docs/images/intersecting_planes.png")
    plt.show()
