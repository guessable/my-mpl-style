# ---------------------
#      "
#    '':''
#   ___:____      |\/|
# ,'        `.    \  /
# |  O        \___/  |
# ~^~^~^~^~^~^~^~^~^~^
# ---------------------
# @author: τ

import matplotlib.pyplot as plt

from my_mpl_style import plot_rc, ax_setting3D

if __name__ == "__main__":
    import numpy as np

    plot_rc()

    a = np.linspace(-1, 1, 500)
    x, y = np.meshgrid(a, a)
    u = np.sin(np.pi * x) * np.exp(y)

    fig = plt.figure()
    ax = fig.add_subplot(121, projection="3d")

    ax.plot_surface(x, y, u)
    ax.set(xticks=[-1, -0.5, 0, 0.5, 1], yticks=[-1, -0.5, 0, 0.5, 1])
    ax_setting3D(ax, (-1, 1), (-1, 1), (u.min(), u.max()), box_aspect=(1, 1, 1))

    ax = fig.add_subplot(122, projection="3d")
    ax.plot_surface(x, y, u)
    ax.set(xticks=[-1, -0.5, 0, 0.5, 1], yticks=[-1, -0.5, 0, 0.5, 1])
    ax_setting3D(ax, (-1, 1), (-1, 1), (u.min(), u.max()), box_aspect=(1, 1, 1))

    plt.show()
