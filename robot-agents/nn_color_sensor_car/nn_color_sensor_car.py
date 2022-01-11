from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *
import random
from hub import button

hub = PrimeHub()

force_button = ForceSensor('C')
motor_pair = MotorPair('B', 'A')
color = ColorSensor('D')

def euclidean_distance_sq(loc, other):
    tot = 0
    for i in range(len(loc) - 1):
        tot += (loc[i] - other[i]) ** 2
    return tot

def clear_buttons():
    hub.left_button.was_pressed()
    hub.right_button.was_pressed()
    force_button.wait_until_released()

def train_menu():
    train = False
    hub.light_matrix.show_image('NO')
    clear_buttons()
    while True:
        if force_button.is_pressed():
            return train
        if hub.left_button.was_pressed() or hub.right_button.was_pressed():
            train = not train
            if train:
                hub.light_matrix.show_image('YES')
            else:
                hub.light_matrix.show_image('NO')

def choose(loc, data):
    return min(map(lambda kv : (euclidean_distance_sq(loc, kv[0]), kv[1]), data.items()))[1]

straight = lambda pair : pair.move(1, 'cm')
left = lambda pair : pair.move(1, 'cm', -100)
right = lambda pair : pair.move(1, 'cm', 100)
backward = lambda pair : pair.move(-1, 'cm')
actions = [straight, right, backward, left]
stay = lambda pair : None

def train():
    data = {}
    action = stay
# I built the robot "backwards" so the left arrow points right
    dirs = ['GO_DOWN', 'GO_LEFT', 'GO_UP', 'GO_RIGHT', 'NO']
    clear_buttons()
    choice = 0
    hub.light_matrix.show_image(dirs[choice])
    while True:
        if hub.left_button.was_pressed():
            choice = (choice - 1) % 5
            hub.light_matrix.show_image(dirs[choice])
        if hub.right_button.was_pressed():
            choice = (choice + 1 ) % 5
            hub.light_matrix.show_image(dirs[choice])
        if force_button.is_pressed():
            if choice == 4:
                return data
            hub.light_matrix.show_image('TARGET')
            force_button.wait_until_released()
            data[color.get_rgb_intensity()] = actions[choice]
            hub.light_matrix.show_image('YES')
            wait_for_seconds(.3)
            choice = 0
            hub.light_matrix.show_image(dirs[choice])
    return data

default = {
    (1023, 1023, 1023, 1023): straight,
    (1023, 688, 692, 1023): right,
    (0,0,0,0): left,
}

train_flag = train_menu()
if train_flag:
    default = train()

hub.light_matrix.off()


while True:
    current = color.get_rgb_intensity()
    print(current)
    act = choose(current, default)
    act(motor_pair)

