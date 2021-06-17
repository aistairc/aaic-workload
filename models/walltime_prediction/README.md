# Walltime Prediction Model

This is an example project that uses AAIC Workload.
This project creates a model for predicting walltime of jobs.

The directory is formatted in MLflow Project format.


## Setup

Install necessary Python packages.

```Console
$ pip install -r requirements.txt
```

Get an AAIC Workload file used for learning a model.

```Console
$ bash ./prepare_data.sh
```

By default, `aaicwl-2018Q1.csv` is downloaded.
To change the file, edit `WORKLOAD_GZ_REMOTE_PATH` variable at l.4.

## Setup Access to MLflow Tracking Server (Optional)

If you have an MLflow traking server, specify environment variables to use the server before training the model.
Depending on your server configuration, you may need to specify following variables.

- MLFLOW_TRACKING_URI
- MLFLOW_S3_ENDPOINT_URL
- AWS_PROFILE

If you do not have any MLflow tracking server, nothing to do.
Experiment tracking records and models are saved in the current directory under `mlflow` directory.
You can access records and models by invoking MLflow tracking UI (type `mlflow ui`).


## Run using MLflow CLI

Typing the following command in the current directory runs `train.py` to train a model with default parameters.

```Console
$ mlflow run . --no-conda
```

To change parameters, run as follows.
Parameters are `workload`, `learning_rate`, `max_depth` and `n_estimators`.

```Console
$ mlflow run . --no-conda -P learning_rate=0.01
```

If you have Anaconda installed and want to create an Anaconda environment to run the program, type as follow.

```Console
$ mlflow run .
```


## Run Training Script Directly

You can directly execute the Python training script as follows.
Parameters are `workload`, `learning_rate`, `max_depth` and `n_estimators` in this order.

```Console
$ python train.py aaicwl-2018Q1.csv 0.3 6 100
```

The following command also records training metrics and models but does not record training parameters in MLflow tracking server.
