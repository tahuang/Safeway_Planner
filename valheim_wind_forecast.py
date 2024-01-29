import math

def create_rng(seed):
    a = seed & 0xFFFFFFFF
    b = ((a * 1812433253) + 1) & 0xFFFFFFFF
    c = ((b * 1812433253) + 1) & 0xFFFFFFFF
    d = ((c * 1812433253) + 1) & 0xFFFFFFFF

    def next():
        nonlocal a, b, c, d
        t1 = a ^ (a << 11) & 0xFFFFFFFF
        t2 = t1 ^ (t1 >> 8)
        a, b, c = b, c, d
        d = (d ^ (d >> 19) ^ t2) & 0xFFFFFFFF
        return d

    def random():
        value = (next() << 9) & 0xFFFFFFFF
        return value / 4294967295

    def random_range():
        return 1.0 - random()

    return random, random_range

WIND_PERIOD = 1000 / 8
WEATHER_PERIOD = 666
DAY_LENGTH = 1800
INTRO_TIME = 2040

def add_octave(time, octave, wind):
    period = math.floor(time / (WIND_PERIOD * 8 / octave))
    random, _ = create_rng(period)
    wind['angle'] += random() * 2 * math.pi / octave
    wind['intensity'] += (random() - 0.5) / octave

def get_global_wind(time):
    wind = {
        'angle': 0,
        'intensity': 0.5,
        'from': 0,
    }
    add_octave(time, 1, wind)
    add_octave(time, 2, wind)
    add_octave(time, 4, wind)
    add_octave(time, 8, wind)
    wind['intensity'] = min(1, max(0, wind['intensity']))
    wind['angle'] = wind['angle'] * 180 / math.pi
    while wind['angle'] > 180:
        wind['angle'] -= 360
    wind['from'] = wind['angle'] + 180
    while wind['from'] > 180:
        wind['from'] -= 360
    return wind

def forecast_wind(day):
    start_time = max(INTRO_TIME - WIND_PERIOD, day * DAY_LENGTH)
    end_time = (day + 1) * DAY_LENGTH
    index = 1
    time = start_time
    
    times = [0.0]
    winds = []
    
    while time < end_time:
        wind_period = math.floor(time / WIND_PERIOD)
        weather_period = math.floor(time / WEATHER_PERIOD)
        wind = get_global_wind(time)
        time = min((wind_period + 1) * WIND_PERIOD, (weather_period + 1) * WEATHER_PERIOD)
        index += 1
        winds.append(wind['from'])
        times.append((time - start_time)/60)
        
    return times[:-1], winds
        
        
if __name__ == '__main__':
    forecast_wind(500)