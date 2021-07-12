import machine
import neopixel
import time
import network
import urandom
import ujson
import urequests

network_ssid = "$CURRENT_WIFI_SSID"
network_passphrase = "$CURRENT_WIFI_PSK"

WEATHER_ENDPOINT = "http://192.168.10.40:8000/current.json"  # Used for testing

n = 84
p = 5

np = neopixel.NeoPixel(machine.Pin(p), n)


def do_connect(connection_pending_delegate):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("connecting to network...")
        wlan.connect(network_ssid, network_passphrase)
    print("network config:", wlan.ifconfig())


def randint(min, max):
    span = max - min + 1
    div = 0x3FFFFFFF // span
    offset = urandom.getrandbits(30) // div
    val = min + offset
    return val


def rainbow_wheel(pos):
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)


def cool_wheel(pos):
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 127:
        return (0, 255 - pos * 2, pos * 2)
    pos -= 127
    return (0, pos * 2, 255 - pos * 2)


def warm_wheel(pos):
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 127:
        return (255 - pos * 2, 0, pos * 2)
    pos -= 127
    return (pos * 2, 0, 255 - pos * 2)


def rainbow_cycle(wait, wheel_func):
    for ci in range(255 / 5):
        color_index = ci * 5
        for pixel_number in range(n):
            rc_index = (pixel_number * 256 // n) + color_index
            np[pixel_number] = wheel_func(rc_index & 255)
        np.write()
        time.sleep_ms(wait)


# def rainbow_cycle(wait, wheel_func):
#   for ci in range(255/5):
#     color_index = ci * 5
#     for pixel_number in range(n):
#       rc_index = (pixel_number * 256 // n) + color_index
#       np[pixel_number] = wheel_func(rc_index & 255)
#     np.write()
#     time.sleep_ms(wait)


def cycle(r, g, b, wait):
    for i in range(4 * n):
        for j in range(n):
            np[j] = (0, 0, 0)
        np[i % n] = (r, g, b)
        np.write()
        time.sleep_ms(wait)


def quad_cycle(colors, wait):
    for offset in range(n):  # For each offset in a full rotation
        for pix in range(n):  # For each pixel in this position
            group = pix // 4  # Groups 0-3
            np[(offset + pix) % n] = colors[group]
            # np[j] = (0, 0, 0)

        # np[(i+0) % n] = colors[0]
        # np[(i+4) % n] = colors[1]
        # np[(i+8) % n] = colors[2]
        # np[(i+12) % n] = colors[3]
        np.write()
        time.sleep_ms(wait)


def set_color(r, g, b):
    for i in range(n):
        np[i] = (r, g, b)
    np.write()


def flash():
    for _ in range(3):
        for p in range(n):
            np[p] = (25, 25, 25)

        np.write()
        time.sleep_ms(5)

        for p in range(n):
            np[p] = (0, 0, 0)

        np.write()
        time.sleep_ms(5)

    for p in range(n):
        np[p] = (255, 255, 255)

    np.write()
    time.sleep_ms(200)

    for p in range(n):
        np[p] = (0, 0, 0)

    np.write()


def snow(num_flakes):
    for _ in range(num_flakes):
        set_color(0, 0, 0)
        np[randint(0, 83)] = (255, 255, 255)
        np[randint(0, 83)] = (255, 255, 255)
        np[randint(0, 83)] = (255, 255, 255)
        np.write()
        time.sleep_ms(500)


def party_snow(num_party):
    for _ in range(num_party):
        set_color(0, 0, 0)
        np[randint(0, 83)] = (randint(0, 255), randint(0, 255), randint(0, 255))
        np[randint(0, 83)] = (randint(0, 255), randint(0, 255), randint(0, 255))
        np[randint(0, 83)] = (randint(0, 255), randint(0, 255), randint(0, 255))
        np.write()
        time.sleep_ms(500)


def rain(num_drops):
    for _ in range(num_drops):
        set_color(0, 0, 0)
        np[randint(0, 83)] = (125, 249, 255)

    for _ in range(255 // 5):
        set_color(125, 249, 255)


colors = [
    (230, 59, 25),
    (255, 156, 25),
    (255, 236, 25),
    (18, 224, 11),
    (11, 168, 224),
    (11, 50, 224),
    (114, 29, 163),
    (242, 56, 165),
]

# while True:
#   flash()
#   flash()
#   snow(6)
#   party_snow(6)
#   rainbow_cycle(10, cool_wheel)
#   rainbow_cycle(10, warm_wheel)
#   rainbow_cycle(10, rainbow_wheel)


class ConnectionIndicator:
    def __init__(self):
        self.current_pos = 0
        for i in range(n):
            np[i] = (0, 0, 0)
        np.write()

    def step(self):
        self.current_pos += 1
        if self.current_pos >= 16:
            self.current_pos = 0

        for j in range(n):
            np[j] = (0, 0, 0)
        np[self.current_pos] = (255, 255, 255)

        np.write()
        time.sleep_ms(50)


conn_indicator = ConnectionIndicator()

do_connect(conn_indicator.step)

set_color(0, 0, 0)

WEATHER_TUNDERSTORM = "Thunderstorm"
WEATHER_DRIZZLE = "Drizzle"
WEATHER_RAIN = "Rain"
WEATHER_SNOW = "Snow"
WEATHER_ATMOSPHERE = "Atmosphere"
WEATHER_CLEAR = "Clear"
WEATHER_CLOUDS = "Clouds"


while True:
    weather_main = ""
    try:
        resp_data = urequests.get(
            WEATHER_ENDPOINT, headers={"Accept": "application/json"}
        ).text
        weather = ujson.loads(resp_data)
        weather_main = weather["wather"][0]["main"]
    except Exception as e:
        pass

    if weather_main == WEATHER_CLOUDS:
        party_snow(6)
    elif weather_main == WEATHER_TUNDERSTORM:
        for _ in range(5):
            flash()
            time.sleep_ms(randint(1, 5) * 750)
    elif weather_main == WEATHER_CLEAR:
        set_color(255, 255, 255)
        time.sleep_ms(5000)
    elif weather_main == WEATHER_DRIZZLE:
        pass
    elif weather_main == WEATHER_RAIN:
        pass
    elif weather_main == WEATHER_SNOW:
        pass
    elif weather_main == WEATHER_ATMOSPHERE:
        pass
    else:
        rainbow_cycle(10, rainbow_wheel)

# while True:
# for _ in range(2):
#   for p in range(n):
#     np[p] = (255, 255, 255)

#   np.write()
#   time.sleep_ms(50)

#   for p in range(n):
#     np[p] = (0,0,0)

#   np.write()
#   time.sleep_ms(500)


# for c in range(10):
# quad_cycle(colors,10)
# for c in range(10):
#     rainbow_cycle(10, warm_wheel)

# for c in range(10):
#   rainbow_cycle(10, warm_wheel)

#     for c in range(10):
#         rainbow_cycle(10, cool_wheel)
#     for c in range(10):
#         rainbow_cycle(10, rainbow_wheel)
