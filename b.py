#!/usr/bin/env python3

from time import sleep

def values(current_left_speed,expected_left_speed,current_right_speed,expected_right_speed,step):

    if expected_left_speed > 1 or expected_left_speed < -1 or expected_right_speed > 1 or expected_right_speed < -1:
        print("expected values outside range")
        exit(1)

    left_step=round(abs(current_left_speed - expected_left_speed)/step,2)
    right_step=round(abs(current_right_speed - expected_right_speed)/step,2)

    print("current\t\tL: " + str(current_left_speed)+"\t R: "+str(current_right_speed))
    print("expected\tL: " + str(expected_left_speed)+"\t R: "+str(expected_right_speed))

    previous_left_speed=current_left_speed
    new_left_speed=current_left_speed
    next_left_speed=current_left_speed

    previous_right_speed=current_right_speed
    new_right_speed=current_right_speed
    next_right_speed=current_right_speed

    for i in range(0,step,1):

        new_left_speed = round(new_left_speed,2) 
        new_right_speed = round(new_right_speed,2) 

        if current_left_speed > expected_left_speed:
            new_left_speed -= left_step
            next_left_speed = new_left_speed 
            next_left_speed -= left_step
            if new_left_speed > 0 and next_left_speed < 0:
                new_left_speed = 0
        elif current_left_speed < expected_left_speed:
            previous_left_speed = new_left_speed
            new_left_speed += left_step
            if new_left_speed > 0 and previous_left_speed < 0:
                new_left_speed = 0
        else:
            new_left_speed = current_left_speed

        if current_right_speed > expected_right_speed:
            new_right_speed -= right_step
            next_right_speed = new_right_speed 
            next_right_speed -= right_step
            if new_right_speed > 0 and next_right_speed < 0:
                new_right_speed = 0
        elif current_right_speed < expected_right_speed:
            previous_right_speed = new_right_speed
            new_right_speed += right_step
            if new_right_speed > 0 and previous_right_speed < 0:
                new_right_speed = 0
        else:
            new_right_speed = current_right_speed

        new_left_speed = round(new_left_speed,2) 
        new_right_speed = round(new_right_speed,2) 

        if i == (step - 1):
            if new_left_speed != expected_left_speed:
                new_left_speed = expected_left_speed
            if new_right_speed != expected_right_speed:
                new_right_speed = expected_right_speed

        print("set\t\tL: " + str(new_left_speed) + "\tR: " + str(new_right_speed), end="")
        if new_left_speed == 0:
            print(" L - sleep longer!",end="")
        if new_right_speed == 0:
            print(" R - sleep longer!",end="")
        print("")

    print("achieved\tL: " + str(new_left_speed)+"\tR: "+str(new_right_speed))
values(1,-1,1,-1,10)
