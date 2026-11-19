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

N = 100


def plot_ax(ax, x, y, z, data, zdir, norm, cmap="viridis", offset=0.5):
    n = N // 2
    if zdir == "z":
        ax.contourf(x[:n, :n], y[:n, :n], data[:n, :n], norm=norm, levels=100, zdir="z", offset=offset, cmap=cmap)
        ax.contourf(x[:n, n - 1 :], y[:n, n - 1 :], data[:n, n - 1 :], norm=norm, levels=100, zdir="z", offset=offset, cmap=cmap)
        ax.contourf(x[n - 1 :, :n], y[n - 1 :, :n], data[n - 1 :, :n], norm=norm, levels=100, zdir="z", offset=offset, cmap=cmap)
        ax.contourf(
            x[n - 1 :, n - 1 :], y[n - 1 :, n - 1 :], data[n - 1 :, n - 1 :], norm=norm, levels=100, zdir="z", offset=offset, cmap=cmap
        )
    elif zdir == "y":
        ax.contourf(x[:n, :n], data[:n, :n], z[:n, :n], norm=norm, levels=100, zdir="y", offset=offset, cmap=cmap)
        ax.contourf(x[:n, n - 1 :], data[:n, n - 1 :], z[:n, n - 1 :], norm=norm, levels=100, zdir="y", offset=offset, cmap=cmap)
        ax.contourf(x[n - 1 :, :n], data[n - 1 :, :n], z[n - 1 :, :n], norm=norm, levels=100, zdir="y", offset=offset, cmap=cmap)
        ax.contourf(
            x[n - 1 :, n - 1 :], data[n - 1 :, n - 1 :], z[n - 1 :, n - 1 :], norm=norm, levels=100, zdir="y", offset=offset, cmap=cmap
        )
    elif zdir == "x":
        ax.contourf(data[:n, :n], y[:n, :n], z[:n, :n], norm=norm, levels=100, zdir="x", offset=offset, cmap=cmap)
        ax.contourf(data[:n, n - 1 :], y[:n, n - 1 :], z[:n, n - 1 :], norm=norm, levels=100, zdir="x", offset=offset, cmap=cmap)
        ax.contourf(data[n - 1 :, :n], y[n - 1 :, :n], z[n - 1 :, :n], norm=norm, levels=100, zdir="x", offset=offset, cmap=cmap)
        ax.contourf(
            data[n - 1 :, n - 1 :], y[n - 1 :, n - 1 :], z[n - 1 :, n - 1 :], norm=norm, levels=100, zdir="x", offset=offset, cmap=cmap
        )


if __name__ == "__main__":
    fig = plt.figure(figsize=(10, 5))

    fig.subplots_adjust(wspace=0.1)

    # =======================================
    a, b = np.meshgrid(np.linspace(0, 1, N), np.linspace(0, 1, N))
    snap = 0.5 * np.ones_like(a)

    # [...,0] x = 0.5, [...,1] y = 0.5, [...,2] z = 0.5
    x = np.stack([snap, a, a], axis=-1)
    y = np.stack([a, snap, b], axis=-1)
    z = np.stack([b, b, snap], axis=-1)

    u = np.sin(10 * np.pi * (x + y + z))

    ax = fig.add_subplot(1, 2, 1, projection="3d")

    norm = Normalize(vmin=u.min(), vmax=u.max())
    plot_ax(ax, x[..., 0], y[..., 0], z[..., 0], u[..., 0], "x", norm)  # x = 0.5
    plot_ax(ax, x[..., 1], y[..., 1], z[..., 1], u[..., 1], "y", norm)  # y = 0.5
    plot_ax(ax, x[..., 2], y[..., 2], z[..., 2], u[..., 2], "z", norm)  # z = 0.5

    cm = ScalarMappable(norm=norm)
    cb = fig.colorbar(cm, ax=ax, shrink=0.5, aspect=14)
    cb.set_label(r"$u_{\rm NN}$", fontsize=13, labelpad=2)

    ax_setting3D(ax, (0, 1), (0, 1), (0, 1), [0, 0.5, 1], [0, 0.5, 1], [0, 0.5, 1])
    ax.set_xlabel(r"$x$", labelpad=-5), ax.set_ylabel(r"$y$", labelpad=-5), ax.set_zlabel(r"$z$", labelpad=-4)

    # =======================================
    x, y, z = 2 * x - 1, 2 * y - 1, 2 * z - 1
    u = np.sin(10 * np.pi * (x + y + z))

    ax = fig.add_subplot(1, 2, 2, projection="3d")

    norm = Normalize(vmin=u.min(), vmax=u.max())
    plot_ax(ax, x[..., 0], y[..., 0], z[..., 0], u[..., 0], "x", norm, offset=0, cmap="plasma")  # x = 0
    plot_ax(ax, x[..., 1], y[..., 1], z[..., 1], u[..., 1], "y", norm, offset=0, cmap="plasma")  # y = 0
    plot_ax(ax, x[..., 2], y[..., 2], z[..., 2], u[..., 2], "z", norm, offset=0, cmap="plasma")  # z = 0

    cm = ScalarMappable(norm=norm, cmap="plasma")
    cb = fig.colorbar(cm, ax=ax, shrink=0.5, aspect=14)
    cb.set_label(r"$u_{\rm NN}$", fontsize=13, labelpad=2)

    ax_setting3D(ax, (-1, 1), (-1, 1), (-1, 1), [-1, -0.5, 0, 0.5, 1], [-1, -0.5, 0, 0.5, 1], [-1, -0.5, 0, 0.5, 1])
    ax.set_xlabel(r"$x$", labelpad=-5), ax.set_ylabel(r"$y$", labelpad=-5), ax.set_zlabel(r"$z$", labelpad=-4)

    plt.savefig("./docs/images/intersecting_planes.png")
    plt.show()
