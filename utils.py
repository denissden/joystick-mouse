def interpolate(val, low, high):
    if val <= low:
        return 0
    if val >= high:
        return 1
    return (val - low) / (high - low)


def interpolate_power(val, power):
    sign = 1 if val > 0 else -1
    after = abs(val ** power)
    return sign * after
