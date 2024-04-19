import os

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import pyvista as pv
import torch
from PIL import ImageColor

COLOR_MAP = {
    0: "#000000",
    1: "#6DA3FD",
    2: "#D34949",
}  # 0: background, 1: foreground, 2: noise
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


def plot_2d_camera_labels(data, axs):
    for instance in data["labels_2d"]:
        for box in instance["instances"]:
            if box["type"] == "BOUNDING_BOX":
                points = box["contour"]["points"]
                x_values = [point["x"] for point in points]
                y_values = [point["y"] for point in points]

                # Add bounding box to the plot
                bbox = patches.Polygon(
                    list(zip(x_values, y_values)),
                    edgecolor="r",
                    facecolor="none",
                    linewidth=2,
                )
                axs.add_patch(bbox)
    return axs


def plot_3d_box_label(data, axs, extra_width=(0, 0, 0), color="b"):
    for instance in data["labels_3d"]:
        for box in instance["instances"]:
            if box["type"] == "3D_BOX":
                curr_box = [
                    box["contour"]["center3D"]["x"],
                    box["contour"]["center3D"]["y"],
                    box["contour"]["center3D"]["z"],
                    box["contour"]["size3D"]["x"] + extra_width[0],
                    box["contour"]["size3D"]["y"] + extra_width[1],
                    box["contour"]["size3D"]["z"] + extra_width[2],
                    box["contour"]["rotation3D"]["z"],
                ]
                curr_box = np.array(curr_box)
                corners = boxes_to_corners_3d(curr_box[np.newaxis, ...])[0]

                # ------ box corners -------
                relevant_corners = []
                relevant_corners.append(corners[0])
                relevant_corners.append(corners[1])
                relevant_corners.append(corners[2])
                relevant_corners.append(corners[3])
                relevant_corners.append(corners[4])

                # ------ orientation line  -------
                mid_points_top = (corners[0] + corners[1]) / 2
                mid_points_bottom = (corners[2] + corners[3]) / 2

                mid_points_mid = (mid_points_top + mid_points_bottom) / 2
                mid_points_mid_lower = (mid_points_mid + mid_points_top) / 2

                relevant_corners_no_dir = np.stack(relevant_corners, 0)
                relevant_corners.append(corners[1])
                relevant_corners.append(mid_points_top)
                relevant_corners.append(mid_points_mid_lower)
                # relevant_corners.append(mid_points_mid_lower)
                relevant_corners = np.stack(relevant_corners, 0)

                axs.plot(
                    relevant_corners[:, 0],
                    relevant_corners[:, 1],
                    "-",
                    c=color,
                )
    return axs


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
        % (
            metadata["object_velocity"],
            metadata["ego_velocity"],
            metadata["distance_to_object"],
        ),
        fontsize=12,
    )
    axs[0].imshow(data["camera_image"])

    # plot 2d box labels
    if data["labels_2d"] is not None:
        axs[0] = plot_2d_camera_labels(data=data, axs=axs[0])

    axs[0].axis("off")
    axs[0].axis("equal")

    # ----- plot top mounted LiDAR point cloud and labels -----
    points = data["points"]
    labels = data["labels"]
    colors = map_label_to_color(labels) if labels is not None else points[:, 3]
    for label_id in np.unique(labels):
        mask = labels == label_id
        axs[1].scatter(
            points[mask, 0],
            points[mask, 1],
            c=colors[mask],
            s=point_size,
            label=LABEL_NAME_MAP[label_id],
        )  # Note: flip x and y axis for visualization

    # plot 3d box labels
    if data["labels_3d"] is not None:
        axs[1] = plot_3d_box_label(data=data, axs=axs[1])

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
        ibeo_front[:, 1],
        ibeo_front[:, 0],
        c="red",
        marker="o",
        s=point_size * 2,
        label="low-res front LiDAR",
    )
    axs[2].scatter(
        ibeo_rear[:, 1],
        ibeo_rear[:, 0],
        c="green",
        marker="o",
        s=point_size * 2,
        label="low-res rear LiDAR",
    )
    axs[2].scatter(
        radar_points[:, 1],
        radar_points[:, 0],
        c="blue",
        marker="x",
        s=30,
        label="radar targets",
    )

    axs[2].set_title("Other sensors")
    axs[2].axis("equal")
    axs[2].set_xticks([])
    axs[2].set_yticks([])
    axs[2].set_xlim([x_min, x_max])
    axs[2].set_ylim([y_min, y_max])
    axs[2].legend(fontsize=10, markerscale=1, loc="upper right")
    fig.tight_layout()

    if save_fig:
        plt.savefig(os.path.join(fig_name))
    else:
        plt.show()
    plt.close("all")


def draw_scene_3D(data):
    points = data["points"][:, :3]
    labels = data["labels"]
    boxes_3d = data["boxes_3d"]
    windows_size = [1000, 1000]
    pl = pv.Plotter(
        window_size=windows_size,
        lighting="three lights",
        off_screen=False,
        polygon_smoothing=True,
    )
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

    plot_boxes(boxes_3d, pl)
    pl.show()


def visualize_scene(data, plot_type="2D"):
    if plot_type == "2D":
        draw_scene_2D(data)
    elif plot_type == "3D":
        draw_scene_3D(data)
    else:
        return NotImplementedError


# ------------- 3D Box Plotting -----------------
def plot_boxes(boxes, pl, line_width=2, color=[0, 0.9, 0]):
    if isinstance(boxes, torch.Tensor):
        boxes = boxes.cpu().numpy()

    for box in boxes:
        corners = boxes_to_corners_3d(box[np.newaxis, ...])[0]
        line_indices = [
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0),  # Bottom face
            (4, 5),
            (5, 6),
            (6, 7),
            (7, 4),  # Top face
            (0, 4),
            (1, 5),
            (2, 6),
            (3, 7),  # Connecting lines
        ]
        for curr_idx in line_indices:
            pts = pv.lines_from_points([corners[curr_idx[0]], corners[curr_idx[1]]])
            pl.add_mesh(pts, line_width=line_width, color=color)

    return pl


def boxes_to_corners_3d(boxes3d):
    """
        7 -------- 4
       /|         /|
      6 -------- 5 .
      | |        | |
      . 3 -------- 0
      |/         |/
      2 -------- 1
    Args:
        boxes3d:  (N, 7) [x, y, z, dx, dy, dz, heading], (x, y, z) is the box center

    Returns:
    """

    boxes3d, is_numpy = check_numpy_to_torch(boxes3d)

    template = (
        boxes3d.new_tensor(
            (
                [1, 1, -1],
                [1, -1, -1],
                [-1, -1, -1],
                [-1, 1, -1],
                [1, 1, 1],
                [1, -1, 1],
                [-1, -1, 1],
                [-1, 1, 1],
            )
        )
        / 2
    )

    corners3d = boxes3d[:, None, 3:6].repeat(1, 8, 1) * template[None, :, :]
    corners3d = rotate_points_along_z(corners3d.view(-1, 8, 3), boxes3d[:, 6]).view(-1, 8, 3)
    corners3d += boxes3d[:, None, 0:3]

    return corners3d.numpy() if is_numpy else corners3d


def rotate_points_along_z(points, angle):
    """
    Args:
        points: (B, N, 3 + C)
        angle: (B), angle along z-axis, angle increases x ==> y
    Returns:

    """
    points, is_numpy = check_numpy_to_torch(points)
    angle, _ = check_numpy_to_torch(angle)

    cosa = torch.cos(angle)
    sina = torch.sin(angle)
    zeros = angle.new_zeros(points.shape[0])
    ones = angle.new_ones(points.shape[0])
    rot_matrix = torch.stack((cosa, sina, zeros, -sina, cosa, zeros, zeros, zeros, ones), dim=1).view(-1, 3, 3).float()
    points_rot = torch.matmul(points[:, :, 0:3], rot_matrix)
    points_rot = torch.cat((points_rot, points[:, :, 3:]), dim=-1)
    return points_rot.numpy() if is_numpy else points_rot


def check_numpy_to_torch(x):
    if isinstance(x, np.ndarray):
        return torch.from_numpy(x).float(), True
    return x, False
