for ARGUMENT in "$@"
do
   KEY=$(echo $ARGUMENT | cut -f1 -d=)

   KEY_LENGTH=${#KEY}
   VALUE="${ARGUMENT:$KEY_LENGTH+1}"

   export "$KEY"="$VALUE"
done

if [ -z ${version+x} ]; then
    echo [ERROR] no version specified.
    exit;
fi

default_name=exp
if [ -z ${name+x} ]; then
    echo [WARN] using default name: $default_name
    name=$default_name
fi
runs_name=$name

default_batch_size=32
if [ -z ${batch_size+x} ]; then
    echo [WARN] using default batch_size: $default_batch_size
    batch_size=$default_batch_size
fi

default_epochs=1
if [ -z ${epochs+x} ]; then
    echo [WARN] using default epochs: $default_epochs
    epochs=$default_epochs
fi

default_weights=runs/train/"${version/train/"patchmentation"}"/$runs_name/weights/best.pt
if [ -z ${weights+x} ]; then
    echo [WARN] using default weights: $default_weights
    weights=$default_weights
fi

default_task=test
if [ -z ${task+x} ]; then
    echo [WARN] using default task: $default_task
    task=$default_task
fi

data_yaml=data/"${version/train/"patchmentation"}".yaml
runs_project=runs/train/"${version/valid/"patchmentation"}"

echo ============================================================
echo version: $version
echo data_yaml: $data_yaml
echo runs_project: $runs_project
echo runs_name: $runs_name
echo weights: $weights
echo epochs: $epochs
echo batch_size: $batch_size
echo task: $task
echo ============================================================

python3 val.py \
    --data $data_yaml \
    --weights $weights --batch-size $batch_size --verbose --task $task \
    --project $runs_project --name $runs_name
