#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from pandas import Series

print(pd.__version__, np.__version__)


def select_and_transform_features(source_df):
    LATITUDE_RANGES = zip(range(32, 44), range(33, 45))
    selected_examples = pd.DataFrame()
    selected_examples['median_income'] = source_df['median_income']
    for k in LATITUDE_RANGES:
        selected_examples['latitude_{}_{}'.format(k[0], k[1])] = source_df['latitude'].apply(lambda la: 1.0 if k[0]<= la<=k[1]  else 0)

    return selected_examples

def main():
    city_names = pd.Series(['San Francisco', 'San Jose', 'Sacramento'])
    population = pd.Series([852469, 1015785, 485199])
    cities = pd.DataFrame({'City name': city_names, 'Population': population})
    cities['Area square miles'] = pd.Series([46.87, 176.53, 97.92])
    cities['Population density'] = cities['Population'] / cities['Area square miles']
    print('{}\n{}\n'.format(type(cities['City name']), cities['City name']))
    print('{}\n{}\n'.format(type(cities['City name'][1]), cities['City name'][1]))
    print('{}\n{}\n'.format(type(cities[0:2]), cities[0:2]))
    print('{}\n'.format(population / 1000))
    print('{}\n'.format(np.log(population)))
    print('{}\n'.format(population.apply(lambda val: val > 1000000)))
    cities['dkk'] = (cities['Area square miles'] > 50) & cities['City name'].apply(lambda name: name.startswith('San'))
    print(cities)
    cities.reindex(np.random.permutation(cities.index))

    california_housing_dataframe = pd.read_csv("./california_housing_train.csv", sep=",")
    print(california_housing_dataframe.describe())
    print(california_housing_dataframe.head())
    california_housing_dataframe.hist('housing_median_age')
    select_and_transform_features(california_housing_dataframe)


def test_1():
    music_data = [("the rolling stones", "Satisfaction"), ("Beatles", "Let It Be"), ("Guns N'Roses", "Don't Cry"),
                  ("Metallica", "Nothing Else Matters")]
    mu_df = pd.DataFrame(data=music_data, index=range(1, 5), columns=['singer', 'song_name'])
    mu_df['time'] = "2018.12.5"
    print(mu_df.append(dict(zip(['singer', 'song_name', 'time'], ("ccc", "ccc", 'cccc'))), ignore_index=True))
    mu_df.loc[8] = ("AAA", "AAAA", 'AAAAA')
    mu_df.iloc[0] = ("BBB", "BBBB", 'BBBBB')
    print(mu_df)
    print(mu_df.drop('time', axis=1))
    print(sorted(set('You need Python.'))[2])
    sa = Series(['a', 'b', 'c'], index = [0, 1, 2])
    sb = Series(['a', 'b', 'c'])
    sc = Series(['a', 'c', 'b'])
    print(sa*3 + sc*2)
    print(sa.equals(sc))
    print(sb.equals(sa))
    data = {'language': ['Java', 'PHP', 'Python', 'R', 'C#'],
            'year': [1995,  1995, 1991,1993, 2000]}
    frame = pd.DataFrame(data)
    frame['IDE'] = Series(['Intellij', 'Notepad', 'IPython', 'R studio', 'VS'])
    for v in frame['IDE']:
        print(type(v), v)
    print('VS' in frame['IDE'],frame['year'][2])
    dict_mark = {'Wang': 'C', 'Li': 'B', 'Ma': 'A'}
    s = ''
    for c in dict_mark.values():
        s += c
    print(s)

    a = {1, 2, 3, 4}
    b = {2, 3, 5, 6}
    print(a.difference(b) == a - b)
    print(a.issubset(b))
    print(a.union(b) == a | b)
    print(a.intersection(b) == a & b)


if __name__ == '__main__':
    #main()
    test_1()