#!/usr/bin/env python
# -*- coding: utf-8 -*-


import datetime

if __name__ == '__main__':
    m_cache_expire_time = 15
    now = datetime.datetime.now()

    interval = (now.minute * 60 + now.second) % m_cache_expire_time
    print(interval, m_cache_expire_time - interval)

