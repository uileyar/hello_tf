#!/usr/bin/env python
# coding: utf-8


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# we don't like warnings
# you can comment the following 2 lines if you'd like to
import warnings
warnings.filterwarnings('ignore')

sns.set()

# Graphics in SVG format are more sharp and legible
#%config InlineBackend.figure_format = 'svg'


def get_fraud_note(df):
    return df.groupby(['fraud_note'])['payout','is_fraud','is_valid_pb', 'fraud_payout'].aggregate(np.sum)


def get_top_datas(df, key, tops):
    return df[df[key].isin(tops)]


def init_data(file_path):
    max_citi = 3600 * 24 * 3
    max_fraud_ctit = 30
    df = pd.read_csv(file_path)
    print('列参数 = {}'.format(df.columns.values))

    df['fraud_payout'] = (df['payout'] * df['is_fraud']).round(decimals=1)
    df['ctit'] = ((pd.to_datetime(df['postback_datetime']) - pd.to_datetime(df['click_datetime'])) / np.timedelta64(1, 's')).astype(int)
    df['ctit'] = df['ctit'].where(df['ctit'] <= max_citi, other=max_citi)
    df['is_ctit'] = (df['ctit'] <= max_fraud_ctit).astype(np.bool).astype(np.int0)
    df = df.drop('clickid', axis=1)
    print(df.head())
    return df


def _summary_data(dd, need_cumsum=True):
    dd['payout'] = dd['payout'].round(decimals=1)
    dd['fraud_payout_p'] = (dd['fraud_payout'] / dd['payout']).round(decimals=2)
    dd['is_fraud_p'] = (dd['is_fraud'] / dd['is_valid_pb']).round(decimals=2)
    dd['is_ctit_p'] = (dd['is_ctit'] / dd['is_valid_pb']).round(decimals=2)

    if need_cumsum:
        cumsum_payout = dd['payout'].cumsum()
        cumsum_is_fraud = dd['is_fraud'].cumsum()
        cumsum_is_valid_pb = dd['is_valid_pb'].cumsum()
        cumsum_fraud_payout = dd['fraud_payout'].cumsum()
        cumsum_is_ctit = dd['is_ctit'].cumsum()
        dd['cumsum_fraud_payout_p'] = (cumsum_fraud_payout / cumsum_payout).round(decimals=2)
        dd['cumsum_is_fraud_p'] = (cumsum_is_fraud / cumsum_is_valid_pb).round(decimals=2)
        dd['cumsum_is_ctit_p'] = (cumsum_is_ctit / cumsum_is_valid_pb).round(decimals=2)
    return dd


def get_summary_by_date(df):
    dd = df.groupby(['date'])['payout', 'is_valid_pb', 'fraud_payout', 'is_fraud', 'is_ctit'].aggregate(np.sum)
    return _summary_data(dd)


def get_tops(df, df_summary, group_by=['pubid']):
    dd = df.groupby(group_by)['payout', 'is_valid_pb', 'fraud_payout', 'is_fraud', 'is_ctit'].aggregate(np.sum)
    dd = _summary_data(dd, False)
    query_list = []
    for (date, series) in df_summary.iterrows():
        query_list.append('(date == "{}" and (fraud_payout_p > {} or is_fraud_p > {} or is_ctit_p > {}))'.format(date, series.fraud_payout_p, series.is_fraud_p, series.is_ctit_p))
    # print(str_query)
    dd = dd.query(' or '.join(query_list))
    return dd


def main():
    file_path = './data/analy_2018-10-28_28_246.csv.gz'
    # file_path = './data/analy_2018-10-28_28_.csv.gz'
    #file_path = './data/analy_2018-09-30_19_246.csv.gz'
    org_df = init_data(file_path)
    df_summary = get_summary_by_date(org_df)
    groups = [
        ['date', 'pubid'], ['date', 'source'], ['date', 'geo'], ['date', 'campid'],
        ['date', 'pubid', 'subid'],

        ['date', 'source', 'pubid'], ['date', 'source', 'pubid', 'subid'], ['date', 'source', 'campid', 'pubid'], ['date', 'source', 'campid', 'pubid', 'subid'],

        ['date', 'campid', 'pubid'], ['date', 'campid', 'pubid', 'subid'],
        ['date', 'geo', 'pubid'], ['date', 'geo', 'pubid', 'subid'],
        ['date', 'geo', 'campid', 'pubid'], ['date', 'geo', 'campid', 'pubid', 'subid'],
    ]
    for groupby in groups:
        dd = get_tops(org_df, df_summary, group_by=groupby)
    pass


def test():
    num_list = [1, 2, 3, 4]
    df = pd.DataFrame(data=num_list)
    print(df.cumsum())


if __name__ == '__main__':
    #test()
    main()

