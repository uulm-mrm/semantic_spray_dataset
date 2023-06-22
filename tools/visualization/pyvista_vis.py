import pyvista as pv
import numpy as np
from pathlib import Path
import os


def plot_points(points, labels=None, point_size=5):
    # Generate random points
    np.random.seed(0)

    pl = pv.Plotter(window_size=[1200, 1000])
    pl.set_background("white")
    pl.add_points(points, point_size=5, scalars=labels, render_points_as_spheres=True, show_scalar_bar=False)

    pl.camera_position = [
        (-60.810111402636636, -1.1432336493635211, 31.115739100900377),
        (-12.68539445370988, -0.2602375438310467, 4.786760766965742),
        (0.4794470854598159, 0.025508583993243458, 0.8771999797006083),
    ]
    pl.show()

    print("pl.camera_position ", pl.camera_position)
    print("pl.camera.azimuth ", pl.camera.azimuth)
    print("pl.camera.elevation ", pl.camera.elevation)


def plot_semantic_plots(points, labels, save_path=None, scan_id=0, save=False):
    # Generate random points
    np.random.seed(0)
    off_screen = True if save else False

    pl = pv.Plotter(window_size=[5000, 5000], lighting="three lights", off_screen=off_screen, polygon_smoothing=True)
    pl.set_background("#dee5ef")

    unique_labels = np.unique(labels)
    label_colors = {0: [0, 0, 0], 1: [0.427, 0.639, 0.992], 2: [0.827, 0.286, 0.286]}
    label_point_size = {0: 15, 1: 25, 2: 25}
    for l in unique_labels:
        mask = labels == l
        pl.add_points(
            points[mask],
            point_size=label_point_size[l],
            color=label_colors[l],
            render_points_as_spheres=True,
            show_scalar_bar=False,
        )

    pl.camera_position = [
        (-70.36770915411218, -0.49252270630862727, 37.64747975323724),
        (-12.697324824904422, 0.20195395399359106, 4.775594754302546),
        (0.4946115275402882, 0.03374817566270463, 0.8684586907065311),
    ]

    if save:
        save_path = Path(save_path)
        save_path.mkdir(parents=True, exist_ok=True)
        pl.show(screenshot=os.path.join(save_path, "img_%s.png" % (str(scan_id).zfill(6))))
    else:
        pl.show()