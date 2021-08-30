from typing import List

from tensorflow.keras import models
import numpy as np
import pandas as pd
import datetime
import time

input_data = 1
network = models.load_model('billyboard.v3.h5')
data = pd.read_csv('/home/toliman/Desktop/holidays_new_mean_sum_dist_month.csv')

K: int = 3  # is hyper parameter how much samples generate to make predict

network.predict(input_data)

def unix_to_month(int_unix):
    return datetime.datetime.fromtimestamp(int_unix).month - 1


def unix_to_day(int_unix):
    return datetime.datetime.fromtimestamp(int_unix).day - 1


def unix_to_half_hour_index(int_unix):
    obj = datetime.datetime.fromtimestamp(int_unix)
    return 1 + obj.hour * 2 + obj.minute // 30 - 1


def get_parameters():
    return {'month': -1,
            'week_day': -1,
            'half_hour': -1,
            'efficiency': .75,
            'views': .5,
            'distances': .99,
            'mean_half_hour': .35,
            'mean_weekday': .35,
            'holidays': .1, }


def transform_predict_to_real_value(val):
    pass


def prepare_stats_dataset(dates: List):
    stats_data = np.zeros(shape=(len(dates), 48, K))
    for i, date in enumerate(dates):
        week_day = date[0].weekday()
        int_unix_start = int(date[0].timestamp())
        int_unix_finish = int(date[1].timestamp())
        h_half_start = unix_to_half_hour_index(int_unix_start)
        h_half_finish = unix_to_half_hour_index(int_unix_finish)

        for h_half_param in range(h_half_start, h_half_finish + 1):
            for j in range(K):  # get k last samples
                params = get_parameters()
                params['month'] = (date[0] - datetime.timedelta(days=i + 1)).month / 11
                params['week_day'] = (date[0] - datetime.timedelta(days=i + 1)).weekday() / 6
                params['half_hour'] = h_half_param / 47
                sample = np.array([x for x in params.values()])
                predicted_val = network.predict(sample.reshape((1, 9)))[0]
                print(predicted_val)

            for j in range(K):  # get k last the same week day
                pass

            kwargs = get_parameters()
            kwargs['month'] = date
        # k_last_samples = np.zeros(shape=)
    pass


def make_predict(sample, stats_data):
    pass


date_arr = [(datetime.datetime(2021, 3, 21, 11, 30), datetime.datetime(2021, 3, 21, 16, 30)),
            (datetime.datetime(2021, 4, 21, 11, 30), datetime.datetime(2021, 4, 21, 16, 30)),
            (datetime.datetime(2021, 5, 21, 11, 30), datetime.datetime(2021, 5, 21, 16, 30))]

prepare_stats_dataset(date_arr)
