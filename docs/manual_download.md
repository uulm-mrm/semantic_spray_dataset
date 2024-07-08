### Manually Download the Dataset
- Download the dataset from [here](https://oparu.uni-ulm.de/xmlui/handle/123456789/48891). Afterwards, you should have the following files: 
  - `SemanticSprayDataset.zip`
  - `SemanticSprayDataset.z01`
  - `SemanticSprayDataset.z02`
  - `SemanticSprayDataset.z03`
  - `SemanticSprayDataset.z04`
  - `SemanticSprayDataset.z05`
- Combine all of the zip files in one single file:
    ```bash 
    $ zip -F SemanticSprayDataset.zip --out SemanticSprayDataset_single_file.zip
    ```

- Extract the files:

    ```bash 
    $ unzip SemanticSprayDataset_single_file.zip
    ```
- The radar semantic labels and object labels (camera and LiDAR) are [stored](../storage/object_and_radar_labels.zip) in `storage/object_and_radar_labels.zip`. Extract the folders and place them inside the previously downloaded folder. 
- The extracted dataset should have a structure like this: 
  ```text
    ├── data
        |--- Crafter_dynamic
        |   |--- 0000_2021-09-08-14-36-56_0
        |   |   |--- image_2
        |   |   |   |--- 000000.jpg
        |   |   |   |--- ....
        |   |   |--- delphi_radar
        |   |   |   |--- 000000.bin
        |   |   |   |--- ....
        |   |   |--- ibeo_front
        |   |   |   |--- 000000.bin
        |   |   |   |--- ....
        |   |   |--- ibeo_rear
        |   |   |   |--- 000000.bin
        |   |   |   |--- ....
        |   |   |--- labels
        |   |   |   |--- 000000.label
        |   |   |   |--- ....
        |   |   |--- radar_labels
        |   |   |   |--- 000000.npy
        |   |   |   |--- ....
        |   |   |--- object_labels
        |   |   |   |--- camera
        |   |   |   |    |--- 000000.json
        |   |   |   |    |--- ....
        |   |   |   |--- lidar
        |   |   |   |    |--- 000000.json
        |   |   |   |    |--- ....
        |   |   |--- velodyne
        |   |   |   |--- 000000.bin
        |   |   |   |--- ....
        |   |   |--- poses.txt
        |   |   |--- metadata.txt
        |--- Golf_dynamic
        ...
        ├── ImageSets
        │   ├── test.txt
        │   └── train.txt
        ├── ImageSets++
        │   └── test.txt
        └── README.txt
  ```
