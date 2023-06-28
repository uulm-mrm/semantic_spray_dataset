<div align="center">   

# SemanticSpray Dataset
<h3 align="center">
  <a href="https://semantic-spray-dataset.github.io/">Project Page</a> |
  <a href="https://arxiv.org/abs/2305.16129">arXiv</a> |
  <a href="https://www.youtube.com/watch?v=P_dM0mG9wX8&list=PLajmQbgGUOt2T-JjM6sUUDDeaxqmMZro3">Video</a> |
  <a href="https://oparu.uni-ulm.de/xmlui/handle/123456789/48891">Download</a>
</h3>
</div>
<br>

<div align="center">
<figure class="half" style="display:flex">
    <img style="width:300px" src="img/teaser_0.gif">  
    <img style="width:300px" src="img/teaser_1.gif">  
    <img style="width:300px" src="img/teaser_2.gif">
</figure>
</div>

## Abstract
<p style="text-align:justify;">
LiDARs are one of the main sensors used for autonomous driving applications, providing accurate depth estimation regardless of lighting conditions. However, they are severely affected by adverse weather conditions such as rain, snow, and fog.
<br>
<br>
This dataset provides semantic labels for a subset of the [Road Spray dataset](https://www.fzd-datasets.de/spray/), which contains scenes of vehicles traveling at different speeds on wet surfaces, creating a trailing spray effect. We provide semantic labels for over 200 dynamic scenes, labeling each point in the LiDAR point clouds as background (road, vegetation, buildings, ...), foreground (moving vehicles), and noise (spray, LiDAR artifacts).
</p>



___
## Getting Started
- Download the dataset from here. Afterwards, you should have the following files: 
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
- The extracted dataset should have a structure like this: 
  ```text
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
  |   |   |--- velodyne
  |   |   |   |--- 000000.bin
  |   |   |   |--- ....
  |   |   |--- poses.txt
  |   |   |--- metadata.txt
  |--- Golf_dynamic
  ...
  ```
- In order to use the default train/test splits, the `ImageSet` folder should be located in `data/SemanticSprayDataset/ImageSets`. The final dataset structure shold be the following:
  ```text
  |--- Crafter_dynamic
  |--- Golf_dynamic
  |--- ImageSets
  |   |--- train.txt
  |   |--- test.txt
  ```

## Exploring The Data
 The sensor setup used for the recordings is the [following](https://www.fzd-datasets.de/spray/):

  - 1 Front Camera
  - 1 Velodyne VLP32C LiDAR (top-mounted high-resolution LiDAR)
  - 2 Ibeo LUX 2010 LiDAR (front and rear mounted, l.- w-resolution LiDAR)
  - 1 Aptiv ESR 2.5 Radar

For each scene, each sensor data can be found in their respective folders:

  - [Camera Image] in the folder "image_2"
  - [VLP32C LiDAR] in the folder "velodyne"
  - [VLIbeo LUX 2010 LiDAR front] in the folder "ibeo_front"
  - [VLIbeo LUX 2010 LiDAR rear] in the folder "ibeo_rear"
  - [Aptiv ESR 2.5 Radar] in the folder "delphi_radar"
  - [Semantic Labels for VLP32C LiDAR] in the folder "labels"
  - The ego vehicle poses are located in the file "poses.txt". The convention used by the [SemanticKITTI dataset](http://www.semantic-kitti.org/dataset.html) is followed.
  - Additional information on the scene setup (e.g., ego_velocity) are given in the "metadata.txt" file.

We provide semantic labels for the VLP32C LiDAR scans. The labeled classes and associated class ID are the following:

  - `Background: 0`
  - `Leading Vehicle: 1`
  - `Spray and other noise artifacts : 2`

___
## Visualizing The Data
- First create a [conda](https://docs.conda.io/en/latest/miniconda.html) envirement and install the requirements:
  ```bash
  conda create -n vis python=3.8
  conda activate vis
  pip3 install -r requirements.txt
  ```
- To visualize the data in a 2D plot, use:
  ```bash
  python3 demo.py --data data/SemanticSprayDataset/ --plot 2D
  ```
  <details>
  <summary>Image result:</summary>
    <div align="center">
    <img style="width:350px" src="img/2d_plot.png">  
    </div>
  </details>

- To visualize the data in a 3D plot, use:
  ```bash
  python3 demo.py --data data/SemanticSprayDataset/ --plot 3D
  ```
  <details>
  <summary>Image result:</summary>
    <div align="center">
    <img style="width:350px" src="img/3d_plot.png">  
    </div>
  </details>

___

## Citation 
If you find this dataset useful in your research, consider citing our work:


```
@ARTICLE{10143263,
author={Piroli, Aldi and Dallabetta, Vinzenz and Kopp, Johannes and Walessa, Marc and Meissner, Daniel and Dietmayer, Klaus},
journal={IEEE Robotics and Automation Letters},
title={Energy-Based Detection of Adverse Weather Effects in LiDAR Data}, 
year={2023},
volume={8},
number={7},
pages={4322-4329},
doi={10.1109/LRA.2023.3282382}}
```

Additionally, consider citing the original Road Spray dataset: 

```
@misc{https://tudatalib.ulb.tu-darmstadt.de/handle/tudatalib/3537,
url = { https://tudatalib.ulb.tu-darmstadt.de/handle/tudatalib/3537 },
author = { Linnhoff, Clemens and Elster, Lukas and Rosenberger, Philipp and Winner, Hermann },
doi = { 10.48328/tudatalib-930 },
keywords = { Automated Driving, Lidar, Radar, Spray, Weather, Perception, Simulation, 407-04 Verkehrs- und Transportsysteme, Intelligenter und automatisierter Verkehr, 380 },
publisher = { Technical University of Darmstadt },
year = { 2022-04 },
copyright = { Creative Commons Attribution 4.0 },
title = { Road Spray in Lidar and Radar Data for Individual Moving Objects }}
```
