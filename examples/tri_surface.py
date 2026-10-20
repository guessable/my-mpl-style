import numpy as np
import matplotlib.pyplot as plt

from matplotlib.colors import Normalize
from my_mpl_style import plot_rc, ax_setting3D

plot_rc(save_dpi=300, save_pad_inches=0.15)


def load_mesh(data):
    v = data["vertices"]
    return v[:, 0], v[:, 1], v[:, 2], data["elements"]


if __name__ == "__main__":
    fig = plt.figure(figsize=(10, 5))

    # ================================
    ax = fig.add_subplot(121, projection="3d")
    x, y, z, tri = load_mesh(np.load("./data/cheese.npz"))

    u = x * np.sin(z) + y * np.sin(x**2)
    u_face = u[tri].mean(axis=1)
    cmap = plt.get_cmap("viridis")
    norm = Normalize(vmin=float(u.min()), vmax=float(u.max()))

    surf = ax.plot_trisurf(x, y, z, triangles=tri, cmap=cmap, norm=norm, linewidth=0, antialiased=False, shade=False)
    surf.set_array(u_face)

    cb = fig.colorbar(surf, ax=ax, shrink=0.62, pad=0.03)
    cb.set_label(r"$x\sin z + y\sin(x^2)$")

    ax_setting3D(ax, (x.min(), x.max()), (y.min(), y.max()), (z.min(), z.max()), [-1, 0, 1], [-1, 0, 1], [-1, 0, 1])
    ax.set_xlabel(r"$x$", fontsize=12, labelpad=-5)
    ax.set_ylabel(r"$y$", fontsize=12, labelpad=-5)
    ax.set_zlabel(r"$z$", fontsize=12, labelpad=-5)

    # ================================
    ax = fig.add_subplot(122, projection="3d")
    x, y, z, tri = load_mesh(np.load("./data/peanut.npz"))

    ax.plot_trisurf(x, y, z, triangles=tri, color="#e8eef5", edgecolor="#2b5f8a", linewidth=0.35, antialiased=True, shade=False)

    ax_setting3D(ax, (x.min(), x.max()), (y.min(), y.max()), (-0.35, 0.35), [-0.8, -0.4, 0, 0.4, -0.8], [-0.3, 0, 0.3], [-0.3, 0, 0.3])
    ax.set_xlabel(r"$x$", fontsize=12, labelpad=-3)
    ax.set_ylabel(r"$y$", fontsize=12, labelpad=-4)
    ax.set_zlabel(r"$z$", fontsize=12, labelpad=-2)

    plt.savefig("./docs/images/tri_surface.png")
    plt.show()
