from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from PIL import ImageColor
import pyvista as pv

COLOR_MAP = {0: "#000000", 1: "#6DA3FD", 2: "#D34949"}  # 0: background, 1: foreground, 2: noise
LABEL_NAME_MAP = {0: "background", 1: "foreground", 2: "noise"}


def hex2rgb(hexcode, normalize=True):
    rgb = ImageColor.getcolor(hexcode, "RGB")
    if normalize:
        rgb = rgb_to_norm(rgb)
    return rgb


def rgb_to_norm(color, max_val=255, bgr=False):
    if bgr:
        color = color[::-1]
    if type(color) is str:
        color = ImageColor.getcolor(color, "RGB")

    norm_color = (color[0] / max_val, color[1] / max_val, color[2] / max_val)
    return norm_color


def map_label_to_color(labels, plot_type="2D"):
    label_colors = []
    for curr_label in labels:
        label_colors.append(hex2rgb(COLOR_MAP[curr_label]))
    label_colors = np.array(label_colors)
    return label_colors


def draw_scene_2D(data, save_fig=True, save_path="../output", fig_name="semantic_scene_2d"):
    # ----- params ------
    x_min, x_max = -10, 10
    y_min, y_max = -30, 30
    point_size = 3

    # ----- plot camera image -----
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))
    metadata = data["infos"]["metadata"]
    fig.suptitle(
        "object velocity: %s km/h, ego velocity: %s km/h, distance to object: %s m"
        % (metadata["object_velocity"], metadata["ego_velocity"], metadata["distance_to_object"]),
        fontsize=12,
    )
    axs[0].imshow(data["camera_image"])
    axs[0].axis("off")
    axs[0].axis("equal")

    # ----- plot top mounted LiDAR point cloud and labels -----
    points = data["points"]
    labels = data["labels"]
    colors = map_label_to_color(labels) if labels is not None else points[:, 3]
    for label_id in np.unique(labels):
        mask = labels == label_id
        axs[1].scatter(
            points[mask, 1], points[mask, 0], c=colors[mask], s=point_size, label=LABEL_NAME_MAP[label_id]
        )  # Note: flip x and y axis for visualization
    axs[1].set_title("Semantic Labels (top-mounted LiDAR)")
    axs[1].axis("equal")
    axs[1].set_xticks([])
    axs[1].set_yticks([])
    axs[1].set_xlim([x_min, x_max])
    axs[1].set_ylim([y_min, y_max])
    axs[1].legend(fontsize=10, markerscale=4, loc="upper right")

    # ----- other sensors -----
    points = data["points"]
    ibeo_front = data["ibeo_front"]
    ibeo_rear = data["ibeo_rear"]
    radar_points = data["radar_points"]
    axs[2].scatter(points[:, 1], points[:, 0], c="#DCDCDC", s=point_size, label="top-mounted LiDAR")
    axs[2].scatter(
        ibeo_front[:, 1], ibeo_front[:, 0], c="red", marker="o", s=point_size * 2, label="low-res front LiDAR"
    )
    axs[2].scatter(
        ibeo_rear[:, 1], ibeo_rear[:, 0], c="green", marker="o", s=point_size * 2, label="low-res rear LiDAR"
    )
    axs[2].scatter(radar_points[:, 1], radar_points[:, 0], c="blue", marker="x", s=30, label="radar targets")

    axs[2].set_title("Other sensors")
    axs[2].axis("equal")
    axs[2].set_xticks([])
    axs[2].set_yticks([])
    axs[2].set_xlim([x_min, x_max])
    axs[2].set_ylim([y_min, y_max])
    axs[2].legend(fontsize=10, markerscale=1, loc="upper right")
    fig.tight_layout()
    plt.show()
    plt.close("all")


def draw_scene_3D(data):
    points = data["points"][:, :3]
    labels = data["labels"]
    windows_size = [1000, 1000]
    pl = pv.Plotter(window_size=windows_size, lighting="three lights", off_screen=False, polygon_smoothing=True)
    pl.set_background("#dee5ef")

    unique_labels = np.unique(labels)
    for l in unique_labels:
        mask = labels == l
        pl.add_points(
            points[mask],
            point_size=3,
            color=COLOR_MAP[l],
            render_points_as_spheres=True,
            show_scalar_bar=False,
        )
    pl.show()


def visualize_scene(data, plot_type="2D"):
    if plot_type == "2D":
        draw_scene_2D(data)
    elif plot_type == "3D":
        draw_scene_3D(data)
    else:
        return NotImplementedError
