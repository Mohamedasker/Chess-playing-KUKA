#!/usr/bin/env pypy
# -*- coding: utf-8 -*-
from __future__ import print_function
import re
import time
import engine_lib
import cv2
import detection_lib
import kuka_interface

turn = True
taking = False
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
# frame =cv2.imread('trya900.png')
cv2.imshow('img',frame)
cv2.waitKey()  ## turn on filter keys
ret, frame = cap.read()
# detection_lib.img = frame ## comment in case of saved image
# cv2.imwrite('backgroundd.png', frame) ##comment in case of saved image
detection_lib.img =cv2.imread('backgroundd.png') ##uncomment in case of saved background image
detection_lib.locList =  detection_lib.boardDetect(detection_lib.img)
cv2.waitKey()
ret, frame = cap.read()
# frame = cv2.imread("trya1000.png")
a = detection_lib.init(frame)
if a == 0:
    cap.release()
    cv2.destroyAllWindows()
p_frame_count = 1000


def main():
    global turn
    global p_frame_count
    castling = False
    pos = engine_lib.Position(engine_lib.initial, 0, (True, True), (True, True), 0, 0)
    searcher = engine_lib.Searcher()
    frame_count = 1000
    while True:
        # ret, frame = cap.read()
        cv2.waitKey()
        time.sleep(1)
        frame_count += 1

        if frame_count > 0:
            if frame_count != p_frame_count:
                engine_lib.print_pos(pos)
                if pos.score <= -engine_lib.MATE_LOWER:
                    print("You lost")
                    break

                # We query the user until she enters a (pseudo) legal move.
                move = None
                trials = 0
                while move not in pos.gen_moves():
                    if trials == 0:
                        # frame = cv2.imread("trya"+str(frame_count)+".png")
                        ret, frame = cap.read()
                        pt = detection_lib.detect(frame, detection_lib.pPieceCount, detection_lib.pColor)
                        # cv2.imshow('img', frame)
                        # for i in range(8):
                        #     for j in range(8):
                        #         detection_lib.pColor[i][j] = pt[i][j]
                        # # frame_count += 1
                    else:
                        print('invalid move')
                        frame_count +=1
                        cv2.waitKey()
                        # frame = cv2.imread("trya" + str(frame_count) + ".png")
                        ret, frame = cap.read()
                        pt = detection_lib.detect(frame, detection_lib.pPieceCount, detection_lib.pColor)
                        # cv2.imshow('img', frame)
                    match = re.match('([a-h][1-8])' * 2, detection_lib.tMove)
                    if match:
                        move = engine_lib.parse(match.group(1)), engine_lib.parse(match.group(2))
                        trials += 1

                    else:
                        # Inform the user when invalid input (e.g. "help") is entered
                        print("Please enter a move like g8f6")
                        cv2.imshow('img',frame)
                        frame_count += 1
                        # print(frame_count)
                        # ret, frame = cap.read()
                        cv2.waitKey()
                if detection_lib.state == 'normal':
                    detection_lib.d1[detection_lib.temp1] = detection_lib.temp2
                    print(detection_lib.temp1,detection_lib.temp2)
                elif detection_lib.state == 'taking':
                    detection_lib.d1[detection_lib.temp1] = detection_lib.temp2
                    detection_lib.d1[detection_lib.temp3] = 'null'
                    print(detection_lib.temp1,detection_lib.temp2,detection_lib.temp3)

                elif detection_lib.state == 'casltling1':
                    detection_lib.d1["wk"] = "c1"
                    detection_lib.d1["wr1"] = "d1"
                    print(detection_lib.d1['wk'])
                    print(detection_lib.d1['wr'])
                elif detection_lib.state == 'castling2':
                    detection_lib.d1["wk"] = "g1"
                    detection_lib.d1["wr2"] = "f1"
                    print(detection_lib.d1['wk'])
                    print(detection_lib.d1['wr2'])

                # print(frame_count)
                # print('right')
                for i in range(8):
                    for j in range(8):
                        detection_lib.pColor[i][j] = pt[i][j]
                for i in range(8):
                    for j in range(8):
                        detection_lib.pOccupation[i][j] = detection_lib.occupation[i][j]
                detection_lib.pPieceCount = detection_lib.pieceCount
                detection_lib.pieceCount = 0
                pos = pos.move(move)
                p_frame_count = frame_count
                # cv2.waitKey()

            # After our move we rotate the board and print it again.
            # This allows us to see the effect of our move.
            engine_lib.print_pos(pos.rotate())
            if pos.score <= -engine_lib.MATE_LOWER:
                print("You won")
                break
            # Fire up the engine to look for a move.
            move, score = searcher.search(pos, secs=1)
            if score == engine_lib.MATE_UPPER:
                print("Checkmate!")
            # The black player moves from a rotated position, so we have to
            # 'back rotate' the move before printing it.
            new = engine_lib.render(119-move[0])
            taken = engine_lib.render(119-move[1])
            print("My move:", engine_lib.render(119-move[0]) + engine_lib.render(119-move[1]))

            if taken in detection_lib.d1.values():
                global taking
                taking = True
                for piece, loc in detection_lib.d1.items():
                    if loc == new:
                        nPiece = piece[1]
                        tempn = piece
                    elif loc == taken:
                        tPiece = piece[1]
                        tempt = piece

                print(new,taken,nPiece,tPiece)
                kuka_interface.takes(new, taken, nPiece, tPiece)
                kuka_interface.button(taken)
                detection_lib.d1[tempn] = taken
                detection_lib.d1[tempt] = 'null'
                detection_lib.pOccupation[ord(taken[0]) - 97][int(taken[1]) - 1] = True
                detection_lib.pOccupation[ord(new[0]) - 97][int(new[1]) - 1] = False
                detection_lib.pColor[ord(taken[0]) - 97][int(taken[1]) - 1] = 2
                detection_lib.pColor[ord(new[0]) - 97][int(new[1]) - 1] = 0
                detection_lib.pPieceCount -= 1

            else:
                taking = False
                if new =="e8":
                    if castling == False:
                        if taken == "c8" or taken == "g8":
                            print("castling",new,taken)
                            if taken == "c8":
                                home = "d8"
                                rook = 'br1'

                            else:
                                home = "f8"
                                rook = 'br2'

                            kuka_interface.castles(new, taken)
                            kuka_interface.button(home)
                            detection_lib.d1['bk'] = taken
                            if rook[2] == '1':
                                detection_lib.d1[rook] = home
                                detection_lib.pOccupation[ord('a') - 97][7] = False
                                detection_lib.pOccupation[ord('d') - 97][7] = True
                                detection_lib.pColor[ord('a') - 97][7] = 0
                                detection_lib.pColor[ord('d') - 97][7] = 2
                            else:
                                detection_lib.d1[rook] = home
                                detection_lib.pOccupation[ord('h') - 97][7] = False
                                detection_lib.pOccupation[ord('f') - 97][7] = True
                                detection_lib.pColor[ord('h') - 97][7] = 0
                                detection_lib.pColor[ord('f') - 97][7] = 2
                        castling = True
                        detection_lib.pOccupation[ord(taken[0]) - 97][int(taken[1]) - 1] = True
                        detection_lib.pOccupation[ord(new[0]) - 97][int(new[1]) - 1] = False
                        detection_lib.pColor[ord(taken[0]) - 97][int(taken[1]) - 1] = 2
                        detection_lib.pColor[ord(new[0]) - 97][int(new[1]) - 1] = 0
                else:
                    for piece, loc in detection_lib.d1.items():
                        if loc == new:
                            nPiece = piece[1]
                            tempn = piece
                        tPiece = "NULL"
                    print(new, taken, nPiece, tPiece)
                    if not detection_lib.pOccupation[ord(taken[0]) - 97][int(taken[1]) - 1]:
                        print(new, taken, nPiece, tPiece)
                        kuka_interface.moves(new, taken, nPiece)
                        kuka_interface.button(taken)
                    else:
                        print("remove what is in square "+taken+"then press the button")
                        cv2.waitKey()
                    detection_lib.d1[tempn] = taken
                    detection_lib.pOccupation[ord(taken[0]) - 97][int(taken[1]) - 1] = True
                    detection_lib.pOccupation[ord(new[0]) - 97][int(new[1]) - 1] = False
                    detection_lib.pColor[ord(taken[0]) - 97][int(taken[1]) - 1] = 2
                    detection_lib.pColor[ord(new[0]) - 97][int(new[1]) - 1] = 0

        # print("My move:", engine_lib.render(119-move[0]) + engine_lib.render(119-move[1]))
        cv2.waitKey()
        frame_count +=1
        pos = pos.move(move)
        if pos.score <= -engine_lib.MATE_LOWER:
            print("You lost")
            time.sleep(3)
            break
        # frame = cv2.imread("trya"+str(frame_count)+".png")
        ret, frame = cap.read()
        cv2.imshow('img', frame)

        # pt = detection_lib.detect(frame, detection_lib.pPieceCount, detection_lib.pColor)
        # for i in range(8):
        #     for j in range(8):
        #         detection_lib.pColor[i][j] = pt[i][j]
        p_frame_count = frame_count
if __name__ == '__main__':
    main()
