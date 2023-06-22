import torch
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path
from PIL import ImageColor
import open3d

COLOR_MAP_2D = {0: "#CFCFCF", 1: "#1B3FAB", 2: "#DC143C"}  # 0: background, 1: foreground, 2: noise
COLOR_MAP_3D = {0: "#939393", 1: "#1B3FAB", 2: "#DC143C"}  # 0: background, 1: foreground, 2: noise
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
    COLOR_MAP = COLOR_MAP_2D if plot_type == "2D" else COLOR_MAP_3D
    label_colors = []
    for curr_label in labels:
        label_colors.append(hex2rgb(COLOR_MAP[curr_label]))
    label_colors = np.array(label_colors)
    return label_colors


def draw_scene_3D(data):
    points = data["points"]
    labels = data["labels"]
    colors = map_label_to_color(labels, plot_type="3D")

    vis = open3d.visualization.Visualizer()
    vis.create_window(width=1250, height=1000)
    vis.get_render_option().point_size = 3.0
    vis.get_render_option().background_color = hex2rgb("#f6faff")

    pts = open3d.geometry.PointCloud()
    pts.points = open3d.utility.Vector3dVector(points[:, :3])
    vis.add_geometry(pts)
    pts.colors = open3d.utility.Vector3dVector(colors)

    vis.run()
    vis.destroy_window()


def save_scene_3D(data, save_path, camera_settings, scan_id, save=True):
    points = data["points"]
    labels = data["labels"]
    colors = map_label_to_color(labels, plot_type="3D")

    vis = open3d.visualization.Visualizer()
    vis.create_window(width=1250, height=1000)

    pts = open3d.geometry.PointCloud()
    pts.points = open3d.utility.Vector3dVector(points[:, :3])
    vis.add_geometry(pts)
    pts.colors = open3d.utility.Vector3dVector(colors)

    assert os.path.isfile(camera_settings)
    param = open3d.io.read_pinhole_camera_parameters(camera_settings)
    ctr = vis.get_view_control()
    ctr.convert_from_pinhole_camera_parameters(param)
    vis.poll_events()
    vis.update_renderer()

    vis.run()
    if save:
        image = vis.capture_screen_float_buffer(True)
        image = np.asarray(image)
        plt.figure(figsize=(100, 100))
        plt.imshow(image)
        plt.axis("off")
        # plt.colorbar()
        filename = os.path.join(save_path, scan_id + ".jpg")
        plt.savefig(filename, bbox_inches="tight")
        plt.clf()
    vis.destroy_window()


def draw_scene_2D(data, save_fig=True, save_path="../output", fig_name="semantic_scene_2d"):
    # ----- params ------
    val = 35
    x_min, x_max = -val, val
    y_min, y_max = -val, val
    point_size = 80

    # ----- plot camera image -----
    fig, axs = plt.subplots(2, 1, figsize=(30, 30))
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
    axs[1].axis("equal")
    axs[1].set_yticklabels([])
    axs[1].set_xticklabels([])
    axs[1].set_xlim([x_min, x_max])
    axs[1].set_ylim([y_min, y_max])
    axs[1].legend(fontsize=40, markerscale=4, loc="upper right")

    fig.tight_layout()
    if not save_fig:
        plt.show()
    else:
        save_path_fig = Path(save_path)
        save_path_fig.mkdir(parents=True, exist_ok=True)
        save_path_fig = save_path_fig / (fig_name + ".png")
        plt.savefig(save_path_fig)
        print("Figure saved in: ", save_path_fig)
    plt.close("all")


def visualize_scene(data, plot_type="2D"):
    if plot_type == "2D":
        draw_scene_2D(data)
    elif plot_type == "3D":
        # draw_scene_3D(data)
        save_scene_3D(data)
    else:
        return NotImplementedError
