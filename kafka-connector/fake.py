# -*- coding: utf-8 -*-
import faker
import json
import random

LOCALE = ['en_US', 'ja_JP', 'vi_VN']


def _get_random_locale():
    """
    Get random locale
    :return:
    """
    return LOCALE[random.randint(0, len(LOCALE) - 1)]


def generate_data():
    """
    Generate fake data
    :return:
    """
    fake = faker.Faker(_get_random_locale())
    data = {
        'name': fake.name(),
        'address': fake.address(),
        'created_at': fake.date_time_this_century().isoformat(),
        'updated_at': fake.date_time_this_century().isoformat(),
    }
    return data


if __name__ == '__main__':
    print(generate_data())
