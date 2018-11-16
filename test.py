#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import random
import datetime


def test1():
    df = pd.DataFrame(((random.randint(2012, 2016), random.choice(['tech', 'art', 'office']),
                        '%dk-%dk' % (random.randint(2, 10), random.randint(10, 20)), 'tt') for _ in range(10000)),
                      columns=['publish_time', 'classf', 'salary', 'title'])
    df.head()
    dd = df.groupby(['publish_time', 'classf', 'salary']).count()['title'].groupby(level=['publish_time', 'classf'], group_keys=False).nlargest(10)
    print(dd)


def test2():
    m_cache_expire_time = 15
    now = datetime.datetime.now()
    interval = (now.minute * 60 + now.second) % m_cache_expire_time
    print(interval, m_cache_expire_time - interval)


def main():
    test1()

if __name__ == '__main__':
    main()


