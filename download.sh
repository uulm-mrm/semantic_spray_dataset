#!/bin/bash

# Directory to store downloaded files
download_dir="data/tmp"

# Create directory for data if it doesn't exist
mkdir -p "$download_dir"

# Array of URLs to download
urls=(
    "https://oparu.uni-ulm.de/bitstreams/6a5e73e0-21ce-4d7a-b008-d5cc720fe7e9/download"
    "https://oparu.uni-ulm.de/bitstreams/b17f22e3-f3da-490f-b216-6ba9a3dde91d/download"
    "https://oparu.uni-ulm.de/bitstreams/fe968c7c-b681-4657-b5ed-1facdfe3ff52/download"
    "https://oparu.uni-ulm.de/bitstreams/fe2b309c-0c3c-47a5-a642-e092d5fe030a/download"
    "https://oparu.uni-ulm.de/bitstreams/f3c29610-bc70-4827-ad9b-2e2d1926a580/download"
    "https://oparu.uni-ulm.de/bitstreams/6509fa11-5efd-4c7a-96cb-c320afb7bdb9/download"
    "https://oparu.uni-ulm.de/bitstreams/c8462e8c-1e5a-4078-bacc-490d8b8cc3e7/download"
)

# Download files into specified directory with original filenames
echo "Downloading files into '$download_dir/' directory..."
for url in "${urls[@]}"; do
    wget --content-disposition -P "$download_dir" "$url"
done

# Change working directory to the download directory
cd "$download_dir" || exit

# Check if SemanticSprayDataset.zip exists
if [ ! -f "SemanticSprayDataset.zip" ]; then
    echo "Error: SemanticSprayDataset.zip not found."
    exit 1
fi

# Combine zip files
echo "Combining zip files..."
zip -F SemanticSprayDataset.zip --out SemanticSprayDataset_single_file.zip

# Check if SemanticSprayDataset_single_file.zip was created
if [ ! -f "SemanticSprayDataset_single_file.zip" ]; then
    echo "Error: Combined zip file (SemanticSprayDataset_single_file.zip) not found."
    exit 1
fi

# Extract the combined zip file
echo "Extracting dataset..."
unzip SemanticSprayDataset_single_file.zip

echo "Dataset extracted successfully!"

# Download and extract object and radar labels (SemanticSpray++)
unzip ../../storage/object_and_radar_labels.zip -d .
cp -r radar_labels/* SemanticSprayDataset/
cp -r object_labels/* SemanticSprayDataset/
mv SemanticSprayDataset ..
rm -rf tmp/