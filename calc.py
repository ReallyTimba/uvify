from translations import t
from ui_builder import lang


def get_burn(uvi_lst, med, indx=0):

    try:

        burn_time = (med / (uvi_lst[indx] * 0.025)) // 60

        if burn_time < 60:
            return int(burn_time)
        elif burn_time <= 240:
            return int(burn_time + get_burn(uvi_lst, med, indx+1))
        else:
            return 0

    except (ZeroDivisionError, IndexError):
        return 0



def get_vitamin_d(uvi, med):
    try:
        formula = 0.167 * (med/uvi)
    except ZeroDivisionError:
        formula = 0
    t_vitamin_d = round(formula)

    if med >= 600:
        return 'no_d'
    return t_vitamin_d if t_vitamin_d < 60 else 60

def get_spf(uvi, med):
    try:
        spf = (uvi * 15 * 120) / med

        if 5 < spf <= 15:
            return 15

        elif 15 < spf <= 30:
            return 30

        elif 30 < spf <= 50:
                return 50

        elif spf > 50:
            return "50+"

        else:
            return t('spf_not_req', lang)

    except ZeroDivisionError:
        return t('spf_not_req', lang)


# def get_real_uv(clouds, uv):
#         cloud_percent = clouds / 100
#
#         func = 0.3 + 0.7 * (1 - cloud_percent)
#
#         real_uv = uv * func
#
#         return real_uv


def uv_ahead(h, offset):
    day = 0
    hour_ahead = h + offset

    if hour_ahead >= 24:
        day += hour_ahead // 24
        hour_ahead %= 24


    return day, hour_ahead


def auto_font_size(text, base_size, container_width, min_size=10):
    size = base_size

    while size > min_size:
        estimated_width = len(text) * size * 0.55
        if estimated_width <= container_width:
            break
        size -= 1

    return size