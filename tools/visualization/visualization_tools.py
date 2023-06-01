import torch
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path
from PIL import ImageColor

COLOR_MAP = {0: "#fcba03", 1: "#0388fc", 2: "#fc033d"}  # 0: background, 1: foreground, 2: noise


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


def map_label_to_color(labels):
    label_colors = []
    for curr_label in labels:
        label_colors.append(hex2rgb(COLOR_MAP[curr_label]))
    label_colors = np.array(label_colors)
    return label_colors


def draw_scene_3D(points, labels=None, save_fig=True, save_path="../output", fig_name="semantic_scene_2d"):
    fig, ax = plt.subplots(figsize=(20, 20))
    colors = map_label_to_color(labels) if labels is not None else points[:, 3]
    ax.scatter(points[:, 0], points[:, 1], c=colors, s=1)

    ax.axis("equal")
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


def draw_scene_2D(data, save_fig=True, save_path="../output", fig_name="semantic_scene_2d"):
    # ----- params ------
    x_min, x_max = -25, 25
    y_min, y_max = -25, 25

    # ----- plot camera image -----
    fig, axs = plt.subplots(2, 1, figsize=(35, 35))
    axs[0].imshow(data["camera_image"])
    axs[0].axis("off")

    # ----- plot top mounted LiDAR point cloud and labels -----
    points = data["points"]
    labels = data["labels"]
    colors = map_label_to_color(labels) if labels is not None else points[:, 3]
    axs[1].scatter(points[:, 1], points[:, 0], c=colors, s=2)  # Note: flip x and y for visualization
    axs[1].axis("equal")

    axs[1] = plt.gca()
    axs[1].set_xlim([x_min, x_max])
    axs[1].set_ylim([y_min, y_max])

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
        draw_scene_3D(data)
    else:
        return NotImplementedError
