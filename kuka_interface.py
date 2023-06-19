from krldriver import *
import serial
out = "i4"
box = 'j2'
zero_point_x = -100
zero_point_y = -100
ptp_velocity = 30
program_override = 30
delay = 1.5


def gripper_close(piece):
    if piece == 'p':
        arduinoData.write('P'.encode())
    elif piece == 'b':
        arduinoData.write('B'.encode())
    elif piece == 'r':
        arduinoData.write('R'.encode())
    elif piece == 'h':
        arduinoData.write('H'.encode())
    elif piece == 'k':
        arduinoData.write('K'.encode())
    elif piece == 'q':
        arduinoData.write('Q'.encode())
    elif piece == 'd':
        arduinoData.write('H'.encode())


def gripper_open():
    arduinoData.write('L'.encode())


arduinoData = serial.Serial('COM3', 9600)


def loc_converter(cell):
    global zero_point_x
    global zero_point_y
    offset_x = 55.3
    offset_y = 55.3
    if cell[0] != 'i' and cell[0] != 'j':
        pos_y = ord(cell[0]) - 96
        pos_x = 9-int(cell[1])
        pos_z = -550

    elif cell[0] == 'i':
        pos_y = -3
        pos_x = 5
        pos_z = -550
    elif cell[0] == 'j':
        pos_y = -3
        pos_x = 2
        pos_z = -550
    pos_x = zero_point_x + offset_x * pos_x
    pos_y = zero_point_y + offset_y * pos_y
    return pos_x, pos_y, pos_z


def pieceLevel(piece):
    if piece == 'p':
        level = -715
    elif piece == 'b':
        level = -700
    elif piece == 'r':
        level = -710
    elif piece == 'h':
        level = -698
    elif piece == 'k':
        level = -700  #-688
    elif piece == 'q':
        level = -688  #-700
    elif piece == 'o':
        level = -550
    elif piece == 'd':
        level = -688
    return level


def take(piece):
    if piece == 'd':
        GRIPPER_CLOSE()
        gripper_close(piece)
        WAIT(1)
        PTP(POS, "", "", pieceLevel(piece))
        PTP(POS, "", "", -550)
        GRIPPER_OPEN()
        gripper_open()
    else:
        PTP(POS, "", "", pieceLevel(piece))
        GRIPPER_CLOSE()
        gripper_close(piece)
        WAIT(delay)
        PTP(POS, "", "", -550)


def drop(piece):
    PTP(POS, "", "", pieceLevel(piece))
    GRIPPER_OPEN()
    gripper_open()
    WAIT(delay)
    PTP(POS, "", "", pieceLevel(piece))


def drops(piece):
    GRIPPER_OPEN()
    gripper_open()
    WAIT(delay)


def castles(n, t):
    if t == "c8":
        p(n)
        take('k')
        p(t)
        drop('k')
        p('a8')
        take('r')
        p('d8')
        drop('r')
    elif t == 'g8':
        p(n)
        take('k')
        p(t)
        drop('k')
        p('h8')
        take('r')
        p('f8')
        drop('r')


def takes(n, t, nPiece, tPiece):
    global out
    p(t)
    take(tPiece)
    p(box)
    drops(tPiece)
    p(n)
    take(nPiece)
    p(t)
    drop(nPiece)


def button(loc):
    moves(loc, "i4", 'd')
    GRIPPER_OPEN()
    moves("i4", box, 'o')


def moves(n, t, nPiece):
    if t == 'i4':
        p(out)
        take(nPiece)

    else:
        p(n)
        take(nPiece)
        p(t)
        drop(nPiece)


def p(n):
    x, y, z = loc_converter(n)
    VEL_CP(3)
    VEL_PTP(ptp_velocity)
    OV_PRO(program_override)
    PAL_MODE(TRUE)
    PTP(POS, "", "", z)
    PTP(POS, x, y, z)

print("start")
VEL_CP(3)
VEL_PTP(ptp_velocity)
OV_PRO(program_override)
APO(0)
BASE(425, 0, 890, 0, 0, 0)
TOOL(0, 0, 0, 0, -90, 0)
PAL_MODE(TRUE)
moves('i4', 'j2', 'o')
# while 1:
#     moves('a1', 'h8', 'p')
#     moves('a8', 'h1', 'p')
#
# #
# while 1:
#     GRIPPER_CLOSE()
#     gripper_close('p')
#     WAIT(delay)
#     GRIPPER_OPEN()
#     gripper_open()
#     WAIT(delay)

