import numpy as np
import argparse
import os
from tools.dataset.semantic_spray_dataset import SemanticSprayDataset
from tools.visualization import visualization_tools as vis
from torch.utils.data import DataLoader

def visualize_data(dataset, plot):
    for i in range(len(dataset)):
        data = dataset[i]
        vis.visualize_scene(data, plot_type=plot) 
        input("..")


def main():
    parser = argparse.ArgumentParser(description="arg parser")
    parser.add_argument("--data", type=str, required=True, help="path to the SemanticSpray dataset root folder")
    parser.add_argument("--split", type=str, default="train", help="train/test")
    parser.add_argument("--plot", type=str, default="2D", help="2D/3D")
    args = parser.parse_args()
    assert os.path.isdir(args.data)

    dataset = SemanticSprayDataset(root_path=args.data, split=args.split)
    visualize_data(dataset, args.plot)


if __name__ == "__main__":
    main()
