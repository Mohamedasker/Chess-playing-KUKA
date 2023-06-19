import numpy as np
import cv2

# vision variables
corner_spacing = 27
edges_threshold = 245
avg_threshold = 150 ##
color_threshold = 50 ##40
# data variables
d1 = {}
pieceCount = 0
pPieceCount = 0
occupation = [0] * 8
pOccupation = [0] * 8
color = [0] * 8
pColor = [0] * 8
turn = True
tMove = ""
state = 0
temp1 = 0
temp2 = 0
temp3 = 0
locList = 0
img =0
for i in range(8):
    occupation[i] = [0] * 8
for j in range(8):
    pOccupation[j] = [0] * 8
for k in range(8):
    color[k] = [0] * 8
for l in range(8):
    pColor[l] = [0] * 8


def boardDetect(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    corners = cv2.goodFeaturesToTrack(gray, 81, 0.001, corner_spacing)
    corners = np.int0(corners)
    xLoc = []
    yLoc = []
    for corner in corners:
        x, y = corner.ravel()
        xLoc.append(x)
        yLoc.append(y)
        cv2.circle(frame, (x, y), 3, 255, -1)

    locListT = list(zip(xLoc,yLoc))
    print(len(locListT))
    cv2.imshow('img', frame)
    # cv2.imshow('img', img)
    locListT.sort()
    sortA = []
    for i in range(9):
        for j in range(9):
            w=j + i*9
            sortA.append(locListT[w])
        sortA = sorted(sortA, key=lambda x: x[1])
        for j in range(9):
            w = j + i * 9
            locListT[w] = sortA[j]
        # sortA.clear()
        del sortA[:]

    return locListT


def detect(frame, pieces, col):
    global tMove
    global turn
    global pieceCount
    global pPieceCount
    global state
    global temp1
    global temp2
    global temp3
    pieceCount = 0
    pPieceCount = pieces
    castling = False
    avg = 0
    count = 0
    nCount = 0 # does absolutely nothing
    temp1 = ""
    temp2 = ""
    temp3 = ""
    for j in range(8):
        for i in range(8):
            w = j + i * 9
            roi = frame[locList[w][1]:locList[w + 1][1], locList[w][0]:locList[w + 9][0]]
            origin = img[locList[w][1]:locList[w + 1][1], locList[w][0]:locList[w + 9][0]]
            diff = roi
            for k in range(2, ((locList[w + 1][1]) - (locList[w][1])) - 2):
                for l in range(2, ((locList[w + 9][0]) - (locList[w][0])) - 2):
                    thres1 = abs(int(roi[k, l][0]) - int(origin[k, l][0]))
                    thres2 = abs(int(roi[k, l][1]) - int(origin[k, l][1]))
                    thres3 = abs(int(roi[k, l][2]) - int(origin[k, l][2]))
                    if thres1 < color_threshold \
                            and thres2 < color_threshold and thres3 < color_threshold:
                        diff[k, l] = (0, 0, 0)
                        # frame[locList[w][1]:locList[w + 1][1], locList[w][0]:locList[w + 9][0]][k, l] = (0, 0, 0)
                        nCount += 1
                    else:
                        avg += diff[k, l][0]
                        count += 1
            if count > 100 and count <900: ##200
                avg = avg / count
                # cv2.imshow('diff', diff)
                if avg > avg_threshold:
                    color[j][i] = 1
                    occupation[j][i] = True
                    pieceCount += 1

                elif avg < avg_threshold and avg > 0:
                    color[j][i] = 2
                    occupation[j][i] = True
                    pieceCount += 1
            else:
                color[j][i] = 0
                occupation[j][i] = False
            avg = 0
            count = 0
            nCount = 0
    cv2.imshow('img', frame)
    change_count = 0
    color_change = 0
    for i in range(8):
        for j in range(8):
            if occupation[j][i] != pOccupation[j][i]:
                change_count += 1
            if color[j][i] != col[j][i]:
                color_change += 1
    print(change_count)
    print(color_change)
    if change_count == 4:
        castling = True
        if pOccupation[4][7] == True and occupation[4][7] == False:
            print('black king castling')
            if pOccupation[0][7] == True and occupation[0][7] == False:
                print("e8c8")
                d1["bk"] = "c8"
                d1["br1"] = "d8"
            elif pOccupation[7][7] == True and occupation[7][7] == False:
                print("e8g8")
                d1["bk"] = "g8"
                d1["br2"] = "f8"
            for i in range(8):
                for j in range(8):
                    pOccupation[i][j] = occupation[i][j]
            pPieceCount = pieceCount
        elif pOccupation[4][0] == True and occupation[4][0] == False:
            print('white king castling')
            if pOccupation[0][0] == True and occupation[0][0] == False:
                state = 'castling1'
                tMove = "e1c1"
                print("e1c1")
                # d1["wk"] = "c1"
                # d1["wr1"] = "d1"
            elif pOccupation[7][0] == True and occupation[7][0] == False:
                state = 'castling2'
                tMove = "e1g1"
                print("e1g1")
                # d1["wk"] = "g1"
                # d1["wr1"] = "f1"
            # for i in range(8):
            #     for j in range(8):
            #         pOccupation[i][j] = occupation[i][j]
            # pPieceCount = pieceCount


        else:
            print('invalid4')
            tMove = "NULL"

    elif change_count != 2 and change_count != 1:
        print('invalid3')
        tMove = "NULL"
    elif change_count == 1 and pPieceCount <= pieceCount:
        print('invalid4')
        tMove = "NULL"
    elif change_count == 1 and color_change == 1:
        print('invalid take')
        tMove = "NULL"
    else:
        for i in range(8):
            for j in range(8):
                if occupation[j][i] != pOccupation[j][i]:
                    if not occupation[j][i]:
                        for key, value in d1.items():
                            if value == str(chr(97 + j)) + str(i + 1):
                                temp1 = key
                    else:
                        temp2 = str(chr(97 + j)) + str(i + 1)
        # for i in range(8):
        #     for j in range(8):
        #         pOccupation[i][j] = occupation[i][j]
        if pPieceCount == pieceCount:
            state = 'normal'
            if turn:
                # print(temp1)
                # print(temp2)
                tMove = str(d1[temp1] + temp2)
                print(d1[temp1] + temp2)
            else:
                print(d1[temp1] + temp2)
            # d1[temp1] = temp2
        else:
            state = 'taking'
            for i in range(8):
                for j in range(8):
                    if color[j][i] != col[j][i]:
                        if color[j][i] == 0:
                            for key, value in d1.items():
                                if value == str(chr(97 + j)) + str(i + 1):
                                    temp1 = key
                        if color[j][i] != 0:
                            for key, value in d1.items():
                                if value == str(chr(97 + j)) + str(i + 1):
                                    temp3 = key
                        if col[j][i] == 1 and color[j][i] == 2:
                            temp2 = str(chr(97 + j)) + str(i + 1)
                            # print("b took w")
                        elif col[j][i] == 2 and color[j][i] == 1:
                            temp2 = str(chr(97 + j)) + str(i + 1)
                            # print("w took b")
            if turn:
                # print(temp1)
                # print(temp2)
                tMove = str(d1[temp1]) + str(temp2)
                print(tMove)
            else:
                print(d1[temp1] + temp2)
            # d1[temp1] = temp2
            # d1[temp3] = 'null'
    # if change_count == 1 or change_count == 2:
        # pPieceCount = pieceCount
        # pieceCount = 0

    return color


def init(sf):
    global pieceCount
    global pPieceCount
    global occupation
    global pOccupation
    global pColor
    avg = 0
    count = 0
    nCount = 0
    # diff = 0
    for j in range(8):
        for i in range(8):
            w = j + i * 9
            roi = sf[locList[w][1]:locList[w + 1][1], locList[w][0]:locList[w + 9][0]]
            origin = img[locList[w][1]:locList[w + 1][1], locList[w][0]:locList[w + 9][0]]
            diff = roi
            for k in range(2, ((locList[w + 1][1]) - (locList[w][1])) - 2):
                for l in range(2, ((locList[w + 9][0]) - (locList[w][0])) - 2):
                    thres1 = abs(int(roi[k, l][0]) - int(origin[k, l][0]))
                    thres2 = abs(int(roi[k, l][1]) - int(origin[k, l][1]))
                    thres3 = abs(int(roi[k, l][2]) - int(origin[k, l][2]))
                    if thres1 < color_threshold \
                            and thres2 < color_threshold and thres3 < color_threshold:
                        # diff[k, l] = (0, 0, 0)
                        sf[locList[w][1]:locList[w + 1][1], locList[w][0]:locList[w + 9][0]][k, l] = (0, 0, 0)
                        nCount += 1
                    else:
                        avg += diff[k, l][0]
                        count += 1
            print(count)
            if count > 100 and count <900: ##200
                avg = avg / count
                # cv2.imshow('diff', diff)
                if avg > avg_threshold:
                    color[j][i] = 1
                    occupation[j][i] = True
                    pieceCount += 1
                elif avg < avg_threshold and avg > 0:
                    color[j][i] = 2
                    occupation[j][i] = True
                    pieceCount += 1
            else:
                color[j][i] = 0
                occupation[j][i] = False
            avg = 0
            count = 0
            nCount = 0
            # cv2.imshow('diff', diff)
            cv2.imshow('img', sf)

    for i in range(8):
        for j in range(8):
            pOccupation[i][j] = occupation[i][j]
    print(pieceCount)
    # print(color)
    # cv2.imshow('diff', diff)
    cv2.imshow("img", sf)
    if pieceCount == 32:
        # print(color)
        for i in range(8):
            d1["wp" + str(i + 1)] = str(chr((97 + i))) + str(2)
        d1["wr1"] = "a1"
        d1["wr2"] = "h1"
        d1["wh1"] = "b1"
        d1["wh2"] = "g1"
        d1["wb1"] = "c1"
        d1["wb2"] = "f1"
        d1["wq"] = "d1"
        d1["wk"] = "e1"

        for i in range(8):
            d1["bp" + str(i + 1)] = str(chr(97 + i)) + str(7)
        d1["br1"] = "a8"
        d1["br2"] = "h8"
        d1["bh1"] = "b8"
        d1["bh2"] = "g8"
        d1["bb1"] = "c8"
        d1["bb2"] = "f8"
        d1["bq"] = "d8"
        d1["bk"] = "e8"
        pColor = [[1, 1, 0, 0, 0, 0, 2, 2],
                  [1, 1, 0, 0, 0, 0, 2, 2],
                  [1, 1, 0, 0, 0, 0, 2, 2],
                  [1, 1, 0, 0, 0, 0, 2, 2],
                  [1, 1, 0, 0, 0, 0, 2, 2],
                  [1, 1, 0, 0, 0, 0, 2, 2],
                  [1, 1, 0, 0, 0, 0, 2, 2],
                  [1, 1, 0, 0, 0, 0, 2, 2]]
        # print(d1)
    else:
        print("number of pieces is invalid")
        cv2.waitKey()
        cv2.destroyAllWindows()
    # cv2.waitKey()
    pPieceCount = pieceCount
    pieceCount = 0

# img = cv2.imread("trya900.png")
# locList = boardDetect(img)
# f2 = cv2.imread("trya1000.png")
# init(f2)
# cv2.waitKey()
# f3 = cv2.imread("trya1001.png")
# pt = detect(f3, pPieceCount, pColor)
# for i in range(8):
#     for j in range(8):
#         pColor[i][j] = pt[i][j]
# cv2.waitKey()
# f3 = cv2.imread("trya10021.png")
# pt = detect(f3, pPieceCount, pColor)
# for i in range(8):
#     for j in range(8):
#         pColor[i][j] = pt[i][j]
# cv2.waitKey()
# f3 = cv2.imread("trya1001.png")
# pt = detect(f3, pPieceCount, pColor)
# for i in range(8):
#     for j in range(8):
#         pColor[i][j] = pt[i][j]
# cv2.waitKey()
# f3 = cv2.imread("trya1002.png")
# pt = detect(f3, pPieceCount, pColor)
# for i in range(8):
#     for j in range(8):
#         pColor[i][j] = pt[i][j]
# cv2.waitKey()
