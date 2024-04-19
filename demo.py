import argparse
import os
from tools.dataset.semantic_spray_dataset import SemanticSprayDataset
from tools.visualization import visualization_tools as vis


def visualize_data(dataset, args):
    for i in range(len(dataset)):
        print("Processing: %d/%d" % (i, len(dataset)))
        data = dataset[i]
        vis.visualize_scene(data, plot_type=args.plot)
        input("...")


def main():
    parser = argparse.ArgumentParser(description="arg parser")
    parser.add_argument("--data", type=str, required=True, help="path to the SemanticSpray dataset root folder")
    parser.add_argument("--split", type=str, default="test", help="train/test")
    parser.add_argument("--plot", type=str, default="2D", help="2D/3D")
    parser.add_argument("--save", action="store_true", help="save scenes")

    args = parser.parse_args()
    assert os.path.isdir(args.data)

    dataset = SemanticSprayDataset(root_path=args.data, split=args.split)
    visualize_data(dataset, args)


if __name__ == "__main__":
    main()
