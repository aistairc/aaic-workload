import random
import sys

import pandas as pd
import xgboost as xgb

JOB_ATTRIBUTES = ['user',
                  'group',
                  'queue',
                  'nodes',
                  'gpus',
                  'walltime_req',
                  'walltime']


def predict(model_file, infile):
    # load data
    category_columns = ['user', 'group', 'queue']

    data_raw = pd.read_csv(infile, index_col=0, dtype={col: object for col in category_columns})
    data = data_raw[data_raw['termcode'] == 0]
    data = data[JOB_ATTRIBUTES]
    data = data[data['walltime'] >= 60]

    X = data.iloc[:, :-1]
    X = pd.get_dummies(X, prefix=['u', 'g', 'q'], columns=category_columns)
    y = data.iloc[:, -1]

    # select a job
    index = random.randrange(len(X))
    X = X.iloc[index:index+1, :]
    y = y.iloc[index:index+1]

    # use model
    xgb_model = xgb.XGBRegressor()
    xgb_model.load_model(model_file)
    y_pred = xgb_model.predict(X)
    print(f'Preficted walltime: {y_pred[0]:.2f}, Actual walltime: {y.iloc[0]}')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('./use_model.py model_file infile', file=sys.stderr)
        sys.exit(1)
    _, model_file, infile = sys.argv
    predict(model_file, infile)
