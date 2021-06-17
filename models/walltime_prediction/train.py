import math
import os
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mlflow
import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

JOB_ATTRIBUTES = ['user',
                  'group',
                  'queue',
                  'nodes',
                  'gpus',
                  'walltime_req',
                  'walltime']

RANDOM_SEED = 1


def train(infile, learning_rate, max_depth, n_estimators):
    with mlflow.start_run():
        # load data
        category_columns = ['user', 'group', 'queue']

        data_raw = pd.read_csv(infile, index_col=0, dtype={col: object for col in category_columns})
        data = data_raw[data_raw['termcode'] == 0]
        data = data[JOB_ATTRIBUTES]
        data = data[data['walltime'] >= 60]

        X = data.iloc[:, :-1]
        X = pd.get_dummies(X, prefix=['u', 'g', 'q'], columns=category_columns)
        y = data.iloc[:, -1]
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=RANDOM_SEED)

        # train
        xgb_model = xgb.XGBRegressor(booster='gbtree',
                                     learning_rate=learning_rate,  # default: 0.3
                                     max_depth=max_depth,          # default: 6
                                     n_estimators=n_estimators,    # default: 100
                                     n_jobs=-1,
                                     random_state=RANDOM_SEED,
                                     verbosity=1)
        xgb_model.fit(X_train, y_train)

        # evaluate
        y_pred = xgb_model.predict(X_test)
        rmse = math.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        mlflow.log_metric('rmse', rmse)
        mlflow.log_metric('r2', r2)

        # log model
        mlflow.xgboost.log_model(xgb_model, 'model')
        # log artifact
        graph_filename = '0000.png'
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot([0, max(y_test)], [0, max(y_test)], color='C1')
        ax.scatter(y_test, y_pred, color='C0')
        ax.set_xlabel('test data')
        ax.set_ylabel('predicted data')
        fig.savefig(graph_filename, bbox_inches='tight')
        mlflow.log_artifact(graph_filename)
        os.remove(graph_filename)


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print('./train.py infile learning_rate max_depth n_estimators', file=sys.stderr)
        sys.exit(1)
    _, infile, learning_rate, max_depth, n_estimators = sys.argv
    train(infile, float(learning_rate), int(max_depth), int(n_estimators))
