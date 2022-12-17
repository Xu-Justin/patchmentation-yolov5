# Patchmentation YOLOv5 🚀

**This repository is forked from [ultralytics/yolov5](https://github.com/ultralytics/yolov5/) and modified. Please refer to the original repository for more informations about the models.**

This model YOLOv5 🚀 is used to benchmark patch augmentation performance of [patchmentation](https://github.com/Xu-Justin/patchmentation).

## Training

Run the following commands to start training.

```bash
--python3 patchmentation_yolov5.py --version [version] \
    --train --batch-size [batch_size] --epochs [epochs]
```

## Validation

Run the following commands to start validating.

```bash
./val.sh version=[version] task=test
```

## Docker

Run the following commands to get into docker container env.

```bash
docker run -it --rm --gpus all jstnxu/patchmentation:yolov5 /bin/bash
```

---

This project was developed as part of thesis project, Computer Science, BINUS University.
