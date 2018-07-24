import matplotlib
import matplotlib.pyplot as plt
import pandas
from matplotlib.path import Path
import matplotlib.patches as patches

if __name__ == '__main__':
    verts = [
    (0., 0.),  # P0
    (-3.2, 1.), # P1
    (1., 0.8333), # P2
    (0.8, 0.), # P3
    ]

    verts=[(23.6829521, -19.450994), (23.6852583, -19.450893399999998), (23.701406600000002, -19.4528625), (23.7136921, -19.4568523), (23.7351042, -19.4648906)]

    codes = [Path.MOVETO,
             Path.LINETO,
             Path.LINETO,
             Path.LINETO,
             Path.LINETO
             ]

    path = Path(verts, codes)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    patch = patches.PathPatch(path, lw=2)
    ax.add_patch(patch)

    # xs, ys = zip(*verts)
    # ax.plot(xs, ys, 'x--', lw=2, color='black', ms=10)


    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    plt.show()
