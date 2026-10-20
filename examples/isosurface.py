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

from skimage.measure import marching_cubes
from matplotlib.colors import LightSource
from my_mpl_style import plot_rc, ax_setting3D

plot_rc(save_dpi=300, save_pad_inches=0.15)


def plot_isosurface(ax, x, y, z, phi, level=0):
    """phi(x,y,z) = level"""
    vertices, faces, _, _ = marching_cubes(phi, level=level, spacing=(x[1] - x[0], y[1] - y[0], z[1] - z[0]), allow_degenerate=False)

    light = LightSource(azdeg=300.0, altdeg=38.0)
    ax.plot_trisurf(
        vertices[:, 0],
        vertices[:, 1],
        vertices[:, 2],
        triangles=faces,
        color="#18b83e",
        linewidth=0.0,
        antialiased=False,
        shade=True,
        lightsource=light,
    )
    ax.set_xlabel(r"$x$", labelpad=-5, fontsize=11)
    ax.set_ylabel(r"$y$", labelpad=-5, fontsize=11)
    ax.set_zlabel(r"$z$", labelpad=-2, fontsize=11)


if __name__ == "__main__":
    fig = plt.figure(figsize=(12.0, 4.2))
    axes = [fig.add_subplot(1, 3, index + 1, projection="3d") for index in range(3)]
    fig.subplots_adjust(wspace=0.05)

    phi_mean = [-0.20, -0.35, -0.43]

    for i in range(3):
        ax = axes[i]
        data = np.load(f"./data/pfc_3d_{i+1}_T3000.npz")
        x, y, z = data["x"], data["y"], data["z"]
        phi = data["u_t3000"]

        plot_isosurface(ax, x, y, z, phi, level=0)
        ax.set_title(rf"$\bar{{\phi}}={phi_mean[i]}$")
        ax_setting3D(ax, (0, 50), (0, 50), (0, 50), [0, 25, 50], [0, 25, 50], [0, 25, 50])

    plt.savefig("./docs/images/isosurface.png")
    plt.show()
