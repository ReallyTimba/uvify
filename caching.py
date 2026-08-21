import os
import json
import time

CACHE_CURRENT = 'assets/requests/current_cache.json'
CACHE_FORECAST = 'assets/requests/forecast_cache.json'

CACHE_MAP = 'assets/requests/map_cache.json'
CACHE_MAX_TIME = 60 * 60 * 24 * 3


def save_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


def load_json(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)



    return


# def get_cached_places():
#     if os.path.exists(CACHE_MAP):
#         cache_age = time.time() - os.path.getmtime(CACHE_MAP)
#         if cache_age < CACHE_MAX_TIME:
#             with open(CACHE_MAP, 'r') as file:
#                 return json.load(file)
#
#     return
#
# def save_cached_places(data):
#     with open(CACHE_MAP, 'w') as file:
#         json.dump(data, file)