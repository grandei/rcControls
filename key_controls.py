#!/usr/bin/env python

from djitellopy import tello
import keypress_module as kp
from time import sleep
import cv2

kp.init()

drone = tello.Tello()
drone.connect()

fps = drone.FPS_30
res = drone.RESOLUTION_720P
drone.set_video_fps(fps)
drone.set_video_resolution(res)
drone.streamon()

image_folder = r"C:\Users\GrandeI\Documents\droneTestImages\\" #replace filepath with where you will be storing your drone images
image_count = 1

frame_read = drone.get_frame_read()

print(drone.get_battery())


def get_keyboard_input():
    # (L/R, bk/fwd, up/down, clock/counterclock-wise yaw) each in -/+100%
    left_right = 0
    bk_fwd = 0
    down_up = 0
    c_cc_yaw = 0
    speed = 50
    image_count = 1

    if kp.is_key_pressed(''):
        drone.land()
    elif kp.is_key_pressed(''):
        drone.takeoff()

    if kp.is_key_pressed('LEFT'): #this is an arrow key
        left_right = -speed
    elif kp.is_key_pressed('RIGHT'):
        left_right = speed

    if kp.is_key_pressed('DOWN'):
        bk_fwd = -speed
    elif kp.is_key_pressed('UP'):
        bk_fwd = speed

    if kp.is_key_pressed(''): #moves down
        down_up = -speed
    elif kp.is_key_pressed('w'):#moves up
        down_up = speed

    if kp.is_key_pressed('d'):
        c_cc_yaw = -speed
    elif kp.is_key_pressed('a'):
        c_cc_yaw = speed
    
    if kp.is_key_pressed('p'):
        image_path = f"{image_folder}image_{image_count}.png"
        cv2.imwrite(image_path, img)
        print(f"Image saved: {image_path}")
        image_count += 1

    return [left_right, bk_fwd, down_up, c_cc_yaw]


# wait for RETURN to take off

while True:
    if kp.is_key_pressed('RETURN') is True:
        break
drone.takeoff()

while True:
    img = frame_read.frame
    img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imshow("drone", img)

    commands = get_keyboard_input()
    drone.send_rc_control(
        commands[0],
        commands[1],
        commands[2],
        commands[3])
    sleep(0.05)
