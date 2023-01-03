# Patchmentation YOLOv5 🚀

**This repository is forked from [ultralytics/yolov5](https://github.com/ultralytics/yolov5/) and modified. For more information about the models, please visit the original repository.**

This model YOLOv5 🚀 is used to benchmark patch augmentation performance of [patchmentation](https://github.com/Xu-Justin/patchmentation).

## Experiment Results and Comparison

| Experiment | Dataset                                                                                      | Weights |     P     |     R     |   mAP@.5  | mAP@.5:.95 |
|:----------:|----------------------------------------------------------------------------------------------|:-------:|:---------:|:---------:|:---------:|:----------:|
|   S-base   | Pascal VOC 2007                                                                              | yolov5s |   0.685   |   0.558   |   0.586   |    0.327   |
|     S1     | Pascal VOC 2007<br><sup>with patch augmentation</sup>                                        | yolov5s |   0.715   |   0.621   | **0.671** |  **0.405** |
|     S2     | Pascal VOC 2007<br><sup>with patch augmentation and soft-edge</sup>                          | yolov5s |   0.717   | **0.624** |    0.67   |    0.403   |
|     S3     | Pascal VOC 2007<br><sup>with patch augmentation and negative-patch</sup>                     | yolov5s |   0.726   |   0.607   |   0.665   |    0.393   |
|     S4     | Pascal VOC 2007<br><sup>with patch augmentation, soft-edge, and negative-patch</sup>         | yolov5s | **0.732** |   0.608   |   0.669   |    0.396   |
|            |                                                                                              |         |           |           |           |            |
|   X-base   | Pascal VOC 2007                                                                              | yolov5x |    0.81   |   0.688   |   0.745   |    0.516   |
|     X1     | Pascal VOC 2007<br><sup>with patch augmentation</sup>                                        | yolov5x |   0.817   | **0.719** | **0.776** |  **0.556** |
|     X2     | Pascal VOC 2007<br><sup>with patch augmentation and soft-edge</sup>                          | yolov5x |   0.804   |   0.704   |   0.772   |    0.544   |
|     X3     | Pascal VOC 2007<br><sup>with patch augmentation and negative-patch</sup>                     | yolov5x |   0.796   |   0.718   | **0.776** |    0.549   |
|     X4     | Pascal VOC 2007<br><sup>with patch augmentation, soft-edge, and negative-patch</sup>         | yolov5x | **0.818** |   0.704   |   0.767   |    0.543   |
|            |                                                                                              |         |           |           |           |            |
|   PS-base  | Penn-Fudan-Ped                                                                               | yolov5s |   0.358   |   0.234   |   0.288   |    0.099   |
|     PS1    | Single image from Campus - Garden1<br><sup>with patch augmentation from Penn-Fudan-Ped</sup> | yolov5s | **0.907** | **0.746** | **0.817** |  **0.401** |
|   PX-base  | Penn-Fudan-Ped                                                                               | yolov5x |   0.566   |   0.315   |   0.393   |    0.145   |
|     PX1    | Single image from Campus - Garden1<br><sup>with patch augmentation from Penn-Fudan-Ped</sup> | yolov5x |  **0.9**  |  **0.79** | **0.838** |  **0.431** |

## Dependency

* Using PIP

  ```bash
  pip install -r requirements.txt
  ```

* Using Docker (recommended)
  
  ```bash
  docker pull jstnxu/patchmentation:yolov5
  docker run -it --ipc=host --gpus all \
    -v {data_folder}:/patchmentation-dataset/data \
    -v {project_folder}:/workspace/runs/patchmentation \
    jstnxu/patchmentation:yolov5 /bin/bash
  ```
  
  * change `{data_folder}` to local path to load dataset.

  * change `{project_folder}` to local path to save outputs.

## Arguments

| Priority* |    Arguments   |        Type       | Description                                                                                                    |
|:---------:|:--------------:|:-----------------:|----------------------------------------------------------------------------------------------------------------|
|     -     |   `--version`  | one or more `str` | Training version(s).                                                                                           |
|     -     |  `--overwrite` |    `store_true`   | Overwrite existing output / zip.                                                                               |
|     -     | `--batch-size` |       `int`       | Number of batch size. Required if `train` is true or `test` is true.                                           |
|     -     |   `--epochs`   |       `int`       | Number of epoch. Required if `train` is true.                                                                  |
|     -     |    `--data`    | one or more `str` | Dataset yaml configurations. If not given, will use predefined yaml in accordance with the `version`.          |
|     1     |    `--train`   |    `store_true`   | Train the model. If `overwrite` is true, it will remove the output (if exists) before training.                |
|     2     |    `--test`    |    `store_true`   | Test the model. If `overwrite` is true, it will remove the test output (if exists) before testing.             |
|     3     |     `--zip`    |    `store_true`   | Zip the output. If `overwrite` is true, it will remove the output zip (if exists) before zipping.              |
|     4     |   `--upload`   |    `store_true`   | Upload the output zip.                                                                                         |
|     5     | `--remove-zip` |    `store_true`   | Remove the output zip, if exists.                                                                              |
|     6     |  `--download`  | one or more `url` | Download the output zip. If `overwrite` is true, it will remove the output zip (if exists) before downloading. |
|     7     |    `--unzip`   |    `store_true`   | Unzip the output zip. If `overwrite` is true, it will remove the output (if exists) before unzipping.          |
|     8     |    `--plot`    |    `store_true`   | Generate more plot. If `train` is true, this method will also be called.                                       |
|     9     |   `--remove`   |    `store_true`   | Remove the output, if exists.                                                                                  |

**Smaller priority number will be executed first*

---

This project was developed as part of thesis project, Computer Science, BINUS University.
