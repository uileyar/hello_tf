#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

print(pd.__version__, np.__version__)


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



if __name__ == '__main__':
    main()
