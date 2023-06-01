import numpy as np
import argparse
import os
from tools.dataset.semantic_spray_dataset import SemanticSprayDataset
from tools.visualization import visualization_tools as vis


def visualize_data(dataset):
    for i in range(len(dataset)):
        data = dataset[i]
        vis.visualize_scene(data)
        input("..")


def main():
    parser = argparse.ArgumentParser(description="arg parser")
    parser.add_argument("--data", type=str, required=True, help="path to the SemanticSpray dataset root folder")
    parser.add_argument("--shuffle", action="store_true", help="shuffle dataloader")
    args = parser.parse_args()
    assert os.path.isdir(args.data)

    dataset = SemanticSprayDataset(root_path=args.data, train=False)
    visualize_data(dataset)


if __name__ == "__main__":
    main()
