import socket
import cv2
import numpy
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM

DEAD_ZONE = 10
FORWARD_SPEED = 75.0
TURN_SPEED = 50.0
FORWARD = 1
BACKWARD = -1
LEFT = 0
RIGHT = 1

"""
Output pins for the motor driver board:
"""
motor_pwms = ["P9_14", "P9_21"]
motor_ins = [["P9_11", "P9_12"], ["P9_25", "P9_26"]]
STBY = "P9_27"

# format of input in bytes: start_byte(255) + up + down + left + right
CHUNK_SIZE = 5
HOST = ''
PORT = 50007

def init_motors():
    """
    Initialize the pins needed for the motor driver.
    """
    global motor_ins
    global motor_pwms
    # initialize GPIO pins
    GPIO.setup(STBY, GPIO.OUT)
    GPIO.output(STBY, GPIO.HIGH)
    for motor in motor_ins:
        for pin in motor:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
                                                                             # initialize PWM pins
    # first need bogus start due to unknown bug in library
    PWM.start("P9_14", 0.0)
    PWM.stop("P9_14")
    # now start the desired PWMs
    for pwm_pin in motor_pwms:
        PWM.start(pwm_pin, 0.0)
        # PWM.set_run(pwm_pin, 1)

def set_motor(motor, direction, value):
    """
    Set an individual motor's direction and speed
    """
    if direction == BACKWARD: # For now, assume CW is forwards
        # forwards: in1 LOW, in2 HIGH
        GPIO.output(motor_ins[motor][0], GPIO.LOW)
        GPIO.output(motor_ins[motor][1], GPIO.HIGH)
    elif direction == FORWARD:
        GPIO.output(motor_ins[motor][0], GPIO.HIGH)
        GPIO.output(motor_ins[motor][1], GPIO.LOW)
    else:
        # there has been an error, stop motors
        GPIO.output(STBY, GPIO.LOW)
    PWM.set_duty_cycle(motor_pwms[motor], value)


def parse_command_string(s):
    left_speed = 0.0
    left_dir = FORWARD
    right_speed = 0.0
    right_dir = FORWARD
    if s[1] == chr(1):
        print('UP')
        left_speed = FORWARD_SPEED
        right_speed = FORWARD_SPEED
    if s[2] == chr(1):
        print('DOWN')
        left_speed = FORWARD_SPEED
        right_speed = FORWARD_SPEED
        left_dir = BACKWARD
        right_dir = BACKWARD
    if s[3] == chr(1):
        print('LEFT')
        left_speed = FORWARD_SPEED
        right_speed = FORWARD_SPEED
        left_dir = BACKWARD
        right_dir = FORWARD
    if s[4] == chr(1):
        print('RIGHT')
        left_dir = FORWARD
        left_speed = FORWARD_SPEED
        right_speed = FORWARD_SPEED
        right_dir = BACKWARD

    set_motor(LEFT, left_dir, left_speed)
    set_motor(RIGHT, right_dir, right_speed)

init_motors()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind((HOST, PORT))
sock.listen(1) # blocks program execution until a connection request occurs from client (sender)

conn, addr = sock.accept()

print('Connection to: ', addr)

while 1:
    data = conn.recv(CHUNK_SIZE)
    if not data: break
    print('------------------------------')
    parse_command_string(data)
    print('------------------------------')

conn.close()

