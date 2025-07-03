F = 1.5


def get_burn(uvi, med):


    try:
        burn_time = (med / (uvi * 0.025)) // 60
        return burn_time
    except ZeroDivisionError:
        return 0


def get_spf(uvi, med):
    try:
        spf = 120 / get_burn(uvi, med)
        print(spf)

        if 4 < spf <= 15:
            return 15

        elif 15 < spf <= 30:
            return 30

        elif 30 < spf <= 50:
                return 50

        elif spf > 50:
            return "50+"

        else:
            return 'Not Required'

    except ZeroDivisionError:
        return 'Not Required'


def get_real_uv(clouds, uv):
        cloud_percent = clouds / 100

        func = 0.3 + 0.7 * (1 - cloud_percent)

        real_uv = uv * func

        return real_uv
