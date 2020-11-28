#!/usr/bin/env python3

import logging, sys
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel, conint
from enum import Enum
from time import sleep


logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

app = FastAPI(
    title = "4x4 Rover API",
    description = " This is an API used to controll 4x4 Rover Platform",
    version = "beta",
    docs_url="/documentation",
    redoc_url=None
)

real_left_speed, real_right_speed = -50, 70
step = 10

class DirectionEnum(str, Enum):
    forward = 'forward'
    backward = 'backward'
    spinleft = 'spinleft'
    spinright = 'spinright'
    turnleft = 'turnleft'
    turnright = 'turnright'
    stop = 'stop'

class Drive(BaseModel):
    direction: DirectionEnum
    speed: conint(ge=0, le=100) = None

@app.get("/drive", tags=["Drive"])
async def get_drive():
    return {"rover": {"drive": {"left_speed": real_left_speed, "right_speed": real_right_speed }}}

@app.put("/drive", tags=["Drive"])
async def update_drive( 
    drive: Drive
    ):
    print(drive.direction.value)
    return drive

def stop():
    values(0,0,step)

def forward():
    values(100,100,step)

def backward():
    values(100,100,step)

def spinleft():
    values(-100,100,step)

def spinright():
    values(100,-100,step)

def turnleft():
    values(0,100,step)

def turnright():
    values(100,0,step)

def values(expected_left_speed,expected_right_speed,step):

    global real_left_speed, real_right_speed

    current_left_speed = real_left_speed
    current_right_speed = real_right_speed

    if expected_left_speed > 100 or expected_left_speed < -100 or expected_right_speed > 100 or expected_right_speed < -100:
        logging.debug("expected values outside range")
        exit(1)

    left_step=round(abs(current_left_speed - expected_left_speed)/step,2)
    right_step=round(abs(current_right_speed - expected_right_speed)/step,2)

    logging.info("current L: " + str(current_left_speed)+" R: "+str(current_right_speed))
    logging.info("expected L: " + str(expected_left_speed)+" R: "+str(expected_right_speed))

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

        logging.debug("set\t\tL: " + str(new_left_speed) + "\tR: " + str(new_right_speed))
        real_left_speed = new_left_speed
        real_right_speed = new_right_speed
        if new_left_speed == 0:
            logging.debug(" L - sleep longer!")
        if new_right_speed == 0:
            logging.debug(" R - sleep longer!")

    logging.info("achieved L: " + str(new_left_speed)+" R: "+str(new_right_speed))
    return {"rover": {"drive": {"left_speed": new_left_speed, "right_speed": new_right_speed }}}
