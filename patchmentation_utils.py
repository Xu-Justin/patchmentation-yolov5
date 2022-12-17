import yaml
import os, shutil
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
    
def _rm(path: str):
    print(f'remove {path}')
    os.system(f'rm -rf {path}')

def _link(source: str, target: str):
    print(f'link {source} to {target}')
    os.system(f'ln -s {os.path.abspath(source)} {os.path.abspath(target)}')

def _unlink(path: str):
    print(f'unlink {path}')
    os.system(f'rm {path}')

def get_folder_output(project: str, name: str):
    return os.path.join(project, name)

def get_file_zip(project: str, name: str):
    return os.path.join(project, f'{name}.zip')

def remove(project: str, name: str):
    folder_output = get_folder_output(project, name)
    _rm(folder_output)

def remove_zip(project: str, name: str):
    file_zip = get_file_zip(project, name)
    _rm(file_zip)

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

def remove_folder_link(folder: str):
    folder_link_images = get_folder_images(folder)
    folder_link_annotations = get_folder_annotations(folder)
    _unlink(folder_link_images)
    _unlink(folder_link_annotations)

def link_dataset(path: str, folders: List[str], batch: int):
    for folder in folders:
        folder_images = os.path.join(path, folder)
        create_folder_link(os.path.dirname(folder_images), batch)

def unlink_dataset(path: str, folders: List[str]):
    for folder in folders:
        folder_images = os.path.join(path, folder)
        remove_folder_link(os.path.dirname(folder_images))

def remove_cache(path: str, folders: List[str]):
    for folder in folders:
        folder_images = os.path.join(path, folder)
        file_cache = get_file_cache(os.path.dirname(folder_images))
        _rm(file_cache)

SINGLE_BATCH = 'single-batch'
MULTI_BATCH = 'multi-batch'

def train(data: str, hyp: str, weights: str, epochs: int, batch_size: int, project: str, name: str):
    
    print(f'=================== TRAIN ======================')

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
        remove_cache(yaml_dict['path'], yaml_dict['train'])
        unlink_dataset(yaml_dict['path'], yaml_dict['train'])
        link_dataset(yaml_dict['path'], yaml_dict['train'], 0)
    if val_format is not None and val_format in (SINGLE_BATCH, MULTI_BATCH):
        remove_cache(yaml_dict['path'], yaml_dict['val'])
        unlink_dataset(yaml_dict['path'], yaml_dict['val'])
        link_dataset(yaml_dict['path'], yaml_dict['val'], 0)
    if test_format is not None and test_format in (SINGLE_BATCH, MULTI_BATCH):
        remove_cache(yaml_dict['path'], yaml_dict['test'])
        unlink_dataset(yaml_dict['path'], yaml_dict['test'])
        link_dataset(yaml_dict['path'], yaml_dict['test'], 0)

    command_initial = f'python3 train.py --data {data} --hyp {hyp} --weights {weights} --epochs {epochs} --batch-size {batch_size} --project {project} --name {name} --save-period 1'
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
