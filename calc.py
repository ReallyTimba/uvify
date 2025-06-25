F = 1.5


def get_burn(uvi, med):


    try:
        burn_time = (med / 9) / uvi

        return burn_time
    except ZeroDivisionError:
        return 0


def get_spf(time_to_burn, uvi, med):
    try:
        spf = (120 / get_burn(uvi, med)) * F

        if spf <= 15:
            return 15

        elif 15 < spf <= 30:
            return 30

        elif 30 < spf <= 50:
                return 50

        elif spf > 50:
            return "50+"

    except ZeroDivisionError:
        return 'Not Required'

