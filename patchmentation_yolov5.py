import patchmentation_utils as utils
from typing import List

def get_args_parser():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', type=str, default=[], nargs='+', help='dataset version')
    parser.add_argument('--train', action='store_true', help='train yolov5')
    parser.add_argument('--test', action='store_true', help='train yolov5')
    parser.add_argument('--epochs', type=int, default=None, help='number of training epoch')
    parser.add_argument('--batch-size', type=int, default=None, help='number of batch size')
    parser.add_argument('--data', type=str, default=[], nargs='+', help='dataset.yaml')
    parser.add_argument('--hyp', type=str, default='data/hyps/hyp.patchmentation.yaml', help='hyperparameters')
    parser.add_argument('--weights', type=str, default='yolov5s.pt', help='initial weights')
    parser.add_argument('--project', type=str, default=None, help='folder to save project')
    parser.add_argument('--remove', action='store_true', help='remove output')
    parser.add_argument('--zip', action='store_true', help='zip output')
    parser.add_argument('--unzip', action='store_true', help='unzip output')
    parser.add_argument('--remove-zip', action='store_true', help='remove zip output')
    parser.add_argument('--upload', action='store_true', help='upload output zip')
    parser.add_argument('--download', type=str, default=[], nargs='+', help='download output zip')
    parser.add_argument('--plot', action='store_true', help='extra output plots')
    parser.add_argument('--overwrite', action='store_true', help='overwrite existing output / zip')
    args = parser.parse_args()
    return args

def project(args):
    return 'runs/patchmentation/' + utils._remove_ext(args.weights)

def main(args):

    versions = args.version

    if args.project is None:
        args.project = project(args)

    for index, version in enumerate(versions):
        print(version)

        if args.train:
            if args.overwrite:
                utils.remove(args.project, version)
            if len(args.data) > index:
                data = args.data[index]
            else:
                data = utils.get_file_yaml(version)
            assert args.batch_size is not None
            assert args.epochs is not None
            utils.train(data, args.hyp, args.weights, args.epochs, args.batch_size, args.project, version)
            utils.plot(args.project, version)

        if args.test:
            if args.overwrite:
                utils.remove_test(args.project, version)
            if len(args.data) > index:
                data = args.data[index]
            else:
                data = utils.get_file_yaml(version)
            assert args.batch_size is not None
            utils.test(data, utils.get_weights(args.project, version), args.batch_size, args.project, version)

        if args.zip:
            if args.overwrite:
                utils.remove_zip(args.project, version)
            utils.zip(args.project, version)

        if args.upload:
            utils.upload(args.project, version)
        
        if args.remove_zip:
            utils.remove_zip(args.project, version)

        if len(args.download) > index:
            if args.overwrite:
                utils.remove_zip(args.project, version)
            utils.download(args.project, version, args.download[index])
        
        if args.unzip:
            if args.overwrite:
                utils.remove_folder_output(args.project, version)
            utils.unzip(args.project, version)

        if args.plot:
            utils.plot(args.project, version)

        if args.remove:
            utils.remove(args.project, version)

if __name__ == '__main__':
    args = get_args_parser()
    print(args)
    main(args)
