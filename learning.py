import machine
import neopixel
import time


n = 16
p = 5

np = neopixel.NeoPixel(machine.Pin(p), n)

# lights up four lights
# np[0] = (255, 0, 0) #red
# np[3] = (125, 204, 223) #blueish
# np[7] = (120, 153, 23) #greenish
# np[10] = (255, 0, 153) #pinkish
# np.write()

# clear all the lights
def clear():
    for i in range(n):
        np[i] = (0, 0, 0)
        np.write()


# set all the lights to one color
def set_color(r, g, b):
    for i in range(n):
        np[i] = (r, g, b)
    np.write()


# make a light turn off as it cycles through the lights abd bounces back and forth
def bounce(r, g, b, wait):
    for i in range(4 * n):
        for j in range(n):
            np[j] = (r, g, b)
        if (i // n) % 2 == 0:
            np[i % n] = (0, 0, 0)
        else:
            np[n - 1 - (i % n)] = (0, 0, 0)
        np.write()
        time.sleep_ms(wait)


# make one light cycle through the lights
def cycle(r, g, b, wait):
    for i in range(4 * n):
        for j in range(n):
            np[j] = (0, 0, 0)
        np[i % n] = (r, g, b)
        np.write()
        time.sleep_ms(wait)


def wheel(pos):
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)


# def rainbow_cycleOne(wait):
#   for j in range(255):
#     for i in range(n):
#       rc_index = (i * 256 // n) + j
#       np[i] = wheel(rc_index & 255)
#     np.write()
#     time.sleep_ms(wait)


def rainbow_cycle(wait, wheel_func):
    for ci in range(255 / 5):
        color_index = ci * 5
        for pixel_number in range(n):
            rc_index = (pixel_number * 256 // n) + color_index
            np[pixel_number] = wheel_func(rc_index & 255)
        np.write()
        time.sleep_ms(wait)


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


def warm_wheel(pos):
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 127:
        return (255 - pos * 2, 0, pos * 2)
    pos -= 127
    return (pos * 2, 0, 255 - pos * 2)


def cool_wheel(pos):
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 127:
        return (0, 255 - pos * 2, pos * 2)
    pos -= 127
    return (0, pos * 2, 255 - pos * 2)


# set_color(255,0,153)
# time.sleep_ms(500)
# clear()
# time.sleep_ms(500)
# set_color(125,204,223)
# time.sleep_ms(500)
# clear()
# time.sleep_ms(500)
# bounce(120,153,23,500)
# time.sleep_ms(500)
# clear()
# cycle(255,0,0,250)
# clear()

while True:
    rainbow_cycle(50, cool_wheel)
    rainbow_cycle(50, warm_wheel)
    rainbow_cycle(50, rainbow_wheel)
