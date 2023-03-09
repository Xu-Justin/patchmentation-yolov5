import yaml
import os, shutil
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import List

def _remove_ext(file: str):
    return os.path.splitext(file)[0]

def _zip(folder: str, file: str):
    os.makedirs(os.path.dirname(file), exist_ok=True)
    if os.path.exists(file):
        raise FileExistsError(file)
    print(f'zip {folder} to {file}')
    shutil.make_archive(_remove_ext(file), 'zip', folder)

def _unzip(file: str, folder: str):
    os.makedirs(folder)
    print(f'unzip {file} to {folder}')
    shutil.unpack_archive(file, folder, 'zip')

def _bash_upload(file: str):
    print(f'bash upload {file}')
    os.system(f'curl bashupload.com -T {file}')

def _bash_download(url: str, file: str):
    os.makedirs(os.path.dirname(file), exist_ok=True)
    if os.path.exists(file):
        raise FileExistsError(file)
    print(f'bash download {url} to {file}')
    os.system(f'wget -c {url} -O {file}')
    
def _rm(path: str, check: bool = False):
    if check and not os.path.exists(path):
        return
    print(f'remove {path}')
    os.system(f'rm -rf {path}')

def _link(source: str, target: str):
    print(f'link {source} to {target}')
    os.system(f'ln -s {os.path.abspath(source)} {os.path.abspath(target)}')

def _unlink(path: str, check: bool = False):
    if check and not os.path.exists(path):
        return
    print(f'unlink {path}')
    os.system(f'rm {path}')

def get_folder_output(project: str, name: str):
    return os.path.join(project, name)

def get_folder_output_test(project: str, name: str):
    return os.path.join(get_folder_output(project, name), 'test')

def get_weights(project: str, name: str):
    return os.path.join(get_folder_output(project, name), 'weights', 'best.pt')

def get_file_zip(project: str, name: str):
    return os.path.join(project, f'{name}.zip')

def remove(project: str, name: str, check: bool = False):
    folder_output = get_folder_output(project, name)
    _rm(folder_output, check)

def remove_test(project: str, name: str, check: bool = False):
    folder_output_test = get_folder_output_test(project, name)
    _rm(folder_output_test, check)

def remove_zip(project: str, name: str, check: bool = False):
    file_zip = get_file_zip(project, name)
    _rm(file_zip, check)

def zip(project: str, name: str):
    folder_output = get_folder_output(project, name)
    file_zip = get_file_zip(project, name)
    _zip(folder_output, file_zip)

def unzip(project: str, name: str):
    folder_output = get_folder_output(project, name)
    file_zip = get_file_zip(project, name)
    _unzip(file_zip, folder_output)

def upload(project: str, name: str):
    file_zip = get_file_zip(project, name)
    _bash_upload(file_zip)

def download(project: str, name: str, url: str):
    file_zip = get_file_zip(project, name)
    _bash_download(url, file_zip)

def plot(project: str, name: str):
    plot_results_mix(project, name)

def plot_results_mix(project: str, name: str):
    csv_results = pd.read_csv(get_file_csv_results(project, name))
    plot_mix_train_val(csv_results, get_file_plot_results_mix(project, name))

def plot_mix_train_val_ax(ax, data_train, data_val, title: str = None):
    index_train = np.arange(len(data_train))
    index_val = np.arange(len(data_val))
    ax.set_title(title)
    ax.plot(index_train, data_train, color='green', label='train')
    ax.plot(index_val, data_val, color='red', label='val')
    ax.legend()
    ax.grid()

def get_csv_results_index(csv_results, index: str):
    for key in csv_results.keys():
        if key.strip() == index:
            return key
    raise Exception(index)
    
def plot_mix_train_val(csv_results, path: str):
    fig, axs = plt.subplots(1, 3, figsize=(30, 6), dpi=150)
    
    train_box_loss = csv_results[get_csv_results_index(csv_results, 'train/box_loss')]
    val_box_loss = csv_results[get_csv_results_index(csv_results, 'val/box_loss')]
    plot_mix_train_val_ax(axs[0], train_box_loss, val_box_loss, 'box_loss')
    
    train_obj_loss = csv_results[get_csv_results_index(csv_results, 'train/obj_loss')]
    val_obj_loss = csv_results[get_csv_results_index(csv_results, 'val/obj_loss')]
    plot_mix_train_val_ax(axs[1], train_obj_loss, val_obj_loss, 'obj_loss')
    
    train_cls_loss = csv_results[get_csv_results_index(csv_results, 'train/cls_loss')]
    val_cls_loss = csv_results[get_csv_results_index(csv_results, 'val/cls_loss')]
    plot_mix_train_val_ax(axs[2], train_cls_loss, val_cls_loss, 'cls_loss')
    
    plt.savefig(path)

def get_file_csv_results(project: str, name: str):
    return os.path.join(project, name, 'results.csv')

def get_file_plot_results_mix(project: str, name: str):
    return os.path.join(project, name, 'results-mix.png')

def get_file_yaml(name: str) -> str:
    return os.path.join('data', f'patchmentation-{name}.yaml')

def get_folder_batch_images(folder: str, batch: int):
    return os.path.join(folder, str(batch).zfill(3), 'images')

def get_folder_images(folder: str):
    return os.path.join(folder, 'images')

def get_folder_batch_annotations(folder: str, batch: int):
    return os.path.join(folder, str(batch).zfill(3), 'labels')

def get_folder_annotations(folder: str):
    return os.path.join(folder, 'labels')

def get_file_cache(folder: str):
    return os.path.join(folder, 'labels.cache')

def create_folder_link(folder: str, batch: int):
    folder_batch_images = get_folder_batch_images(folder, batch)
    folder_batch_annotations = get_folder_batch_annotations(folder, batch)
    folder_link_images = get_folder_images(folder)
    folder_link_annotations = get_folder_annotations(folder)
    _link(folder_batch_images, folder_link_images)
    _link(folder_batch_annotations, folder_link_annotations)

def remove_folder_link(folder: str, check: bool = False):
    folder_link_images = get_folder_images(folder)
    folder_link_annotations = get_folder_annotations(folder)
    _unlink(folder_link_images, check)
    _unlink(folder_link_annotations, check)

def link_dataset(path: str, folders: List[str], batch: int):
    for folder in folders:
        folder_images = os.path.join(path, folder)
        create_folder_link(os.path.dirname(folder_images), batch)

def unlink_dataset(path: str, folders: List[str], check: bool = False):
    for folder in folders:
        folder_images = os.path.join(path, folder)
        remove_folder_link(os.path.dirname(folder_images), check)

def remove_cache(path: str, folders: List[str], check: bool = False):
    for folder in folders:
        folder_images = os.path.join(path, folder)
        file_cache = get_file_cache(os.path.dirname(folder_images))
        _rm(file_cache, check)

SINGLE_BATCH = 'single-batch'
MULTI_BATCH = 'multi-batch'

def train(data: str, hyp: str, weights: str, epochs: int, batch_size: int, project: str, name: str):
    
    print(f'=================== TRAIN =====================')

    print(f'data: {data}')
    print(f'hyp: {hyp}')
    print(f'weights: {weights}')
    print(f'epochs : {epochs}')
    print(f'batch_size: {batch_size}')
    print(f'project: {project}')
    print(f'name: {name}')
    print(f'===============================================')
    
    if os.path.exists(get_folder_output(project, name)):
        raise FileExistsError(get_folder_output(project, name))
    
    with open(data, 'r') as f:
        yaml_dict = yaml.safe_load(f)

    train_format = yaml_dict.get('train-format', None)
    val_format = yaml_dict.get('val-format', None)
    test_format = yaml_dict.get('test-format', None)

    print(f'train_format: {train_format}')
    print(f'val_format: {val_format}')
    print(f'test_format: {test_format}')
    print(f'===============================================')
    

    if train_format is not None and train_format in (SINGLE_BATCH, MULTI_BATCH):
        remove_cache(yaml_dict['path'], yaml_dict['train'], check=True)
        unlink_dataset(yaml_dict['path'], yaml_dict['train'], check=True)
        link_dataset(yaml_dict['path'], yaml_dict['train'], 0)
    if val_format is not None and val_format in (SINGLE_BATCH, MULTI_BATCH):
        remove_cache(yaml_dict['path'], yaml_dict['val'], check=True)
        unlink_dataset(yaml_dict['path'], yaml_dict['val'], check=True)
        link_dataset(yaml_dict['path'], yaml_dict['val'], 0)
    if test_format is not None and test_format in (SINGLE_BATCH, MULTI_BATCH):
        remove_cache(yaml_dict['path'], yaml_dict['test'], check=True)
        unlink_dataset(yaml_dict['path'], yaml_dict['test'], check=True)
        link_dataset(yaml_dict['path'], yaml_dict['test'], 0)

    command_initial = f'python3 train.py --data {data} --hyp {hyp} --weights {weights} --epochs {epochs} --batch-size {batch_size} --project {project} --name {name}'
    os.system(command_initial)

    resume_weight = os.path.join(project, name, 'weights', 'last.pt')
    command_resume = f'python3 train.py --resume {resume_weight}'
    for epoch in range(1, epochs):
        if train_format is not None and train_format in (MULTI_BATCH):
            remove_cache(yaml_dict['path'], yaml_dict['train'])
            unlink_dataset(yaml_dict['path'], yaml_dict['train'])
            link_dataset(yaml_dict['path'], yaml_dict['train'], epoch)
        if val_format is not None and val_format in (MULTI_BATCH):
            remove_cache(yaml_dict['path'], yaml_dict['val'])
            unlink_dataset(yaml_dict['path'], yaml_dict['val'])
            link_dataset(yaml_dict['path'], yaml_dict['val'], epoch)
        if test_format is not None and test_format in (MULTI_BATCH):
            remove_cache(yaml_dict['path'], yaml_dict['test'])
            unlink_dataset(yaml_dict['path'], yaml_dict['test'])
            link_dataset(yaml_dict['path'], yaml_dict['test'], epoch)
        os.system(command_resume)

    if train_format is not None and train_format in (SINGLE_BATCH, MULTI_BATCH):
        remove_cache(yaml_dict['path'], yaml_dict['train'])
        unlink_dataset(yaml_dict['path'], yaml_dict['train'])
    if val_format is not None and val_format in (SINGLE_BATCH, MULTI_BATCH):
        remove_cache(yaml_dict['path'], yaml_dict['val'])
        unlink_dataset(yaml_dict['path'], yaml_dict['val'])
    if test_format is not None and test_format in (SINGLE_BATCH, MULTI_BATCH):
        remove_cache(yaml_dict['path'], yaml_dict['test'])
        unlink_dataset(yaml_dict['path'], yaml_dict['test'])

def test(data: str, weights:str, batch_size: int, project: str, name: str):

    print(f'=================== TEST ======================')

    print(f'data: {data}')
    print(f'weights: {weights}')
    print(f'batch_size: {batch_size}')
    print(f'project: {project}')
    print(f'name: {name}')
    print(f'===============================================')

    if os.path.exists(get_folder_output_test(project, name)):
        raise FileExistsError(get_folder_output_test(project, name))
    
    with open(data, 'r') as f:
        yaml_dict = yaml.safe_load(f)

    val_format = yaml_dict.get('val-format', None)
    test_format = yaml_dict.get('test-format', None)

    print(f'val_format: {val_format}')
    print(f'test_format: {test_format}')
    print(f'===============================================')
    

    if val_format is not None and val_format in (SINGLE_BATCH, MULTI_BATCH):
        remove_cache(yaml_dict['path'], yaml_dict['val'], check=True)
        unlink_dataset(yaml_dict['path'], yaml_dict['val'], check=True)
        link_dataset(yaml_dict['path'], yaml_dict['val'], 0)
    if test_format is not None and test_format in (SINGLE_BATCH, MULTI_BATCH):
        remove_cache(yaml_dict['path'], yaml_dict['test'], check=True)
        unlink_dataset(yaml_dict['path'], yaml_dict['test'], check=True)
        link_dataset(yaml_dict['path'], yaml_dict['test'], 0)

    command = f'python3 val.py --data {data} --weights {weights} --batch-size {batch_size} --verbose --task test --project {project} --name {name + "/test"} --iou-thres 0.2'
    os.system(command)

    if val_format is not None and val_format in (SINGLE_BATCH, MULTI_BATCH):
        remove_cache(yaml_dict['path'], yaml_dict['val'])
        unlink_dataset(yaml_dict['path'], yaml_dict['val'])
    if test_format is not None and test_format in (SINGLE_BATCH, MULTI_BATCH):
        remove_cache(yaml_dict['path'], yaml_dict['test'])
        unlink_dataset(yaml_dict['path'], yaml_dict['test'])
