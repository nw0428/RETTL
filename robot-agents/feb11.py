from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *
import json


hub = PrimeHub()

motor = Motor('A')
color = ColorSensor('D')

def euclidean_distance_sq(loc, other):
    tot = 0
    for i in range(len(loc)):
        tot += (loc[i] - other[i]) ** 2
    return tot

def clear_buttons():
    hub.left_button.was_pressed()
    hub.right_button.was_pressed()

def setup_get_sensor_data(color_sensor):
    return lambda : color_sensor.get_rgb_intensity()[0:2]


def train_menu():
    train = False
    hub.light_matrix.show_image('NO')
    clear_buttons()
    while True:
        if hub.motion_sensor.was_gesture('tapped'):
            return train
        if hub.left_button.was_pressed() or hub.right_button.was_pressed():
            train = not train
            if train:
                hub.light_matrix.show_image('YES')
            else:
                hub.light_matrix.show_image('NO')

def choose(loc, data):
    return min(map(lambda kv : (euclidean_distance_sq(loc, kv[0]), kv[1]), data.items()))[1]

def send(thing):
    print(json.dumps(thing))

def train(get_sensor_data, motor):
    data = {}
    choices = ['CHESSBOARD', 'NO']
    choice = 0
    hub.light_matrix.show_image(choices[choice])
    while True:
        if hub.left_button.was_pressed():
            choice = (choice - 1) % 2
            hub.light_matrix.show_image(choices[choice])
        if hub.right_button.was_pressed():
            choice = (choice + 1 ) % 2
            hub.light_matrix.show_image(choices[choice])
        if hub.motion_sensor.was_gesture('tapped'):
            if choice == 1:
                hub.light_matrix.off()
                return data
            data[get_sensor_data()] = motor.get_position()
            hub.light_matrix.show_image('YES')
            send({"training_data": data})
            wait_for_seconds(.3)
            choice = 0
            hub.light_matrix.show_image(choices[choice])

default = {
    (1023, 1023): 180,
    (1023, 688): 90,
    (0,0): 0,
}



get_sensor_data = setup_get_sensor_data(color)

hub.motion_sensor.was_gesture('tapped')

train_flag = train_menu()
if train_flag:
    default = train(get_sensor_data, motor)

hub.light_matrix.off()

rounds = 0

while True:
    current = get_sensor_data()
    send({"current_value": current})
    target_angle = choose(current, default)
    motor.run_to_position(target_angle)
    rounds = (rounds + 1) % 10
    if rounds == 0:
        send({"training_data": default})
