# Patchmentation YOLOv5 🚀

**This repository is forked from [ultralytics/yolov5](https://github.com/ultralytics/yolov5/) and modified. For more information about the models, please visit the original repository.**

This model YOLOv5 🚀 is used to benchmark patch augmentation performance of [patchmentation](https://github.com/Xu-Justin/patchmentation).

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
