from machine import Pin,I2C
from ssd1306 import SSD1306_I2C
import utime

#Keypad definitions
matrixKeys = [['1','2','3','A'],
              ['4','5','6','B'],
              ['7','8','9','C'],
              ['*','0','#','D']]
rowPins = [2,3,4,5]
colPins = [6,7,8,9]

row = []
column = []

for item in rowPins:
    row.append(machine.Pin(item,machine.Pin.OUT))
for item in colPins:
    column.append(machine.Pin(item,machine.Pin.IN,machine.Pin.PULL_DOWN))
key = '0'
def scanKey():
    global key
    for rowKey in range(4):
        row[rowKey].value(1)#make one row high at a time
        for colKey in range(4):
            if column[colKey].value() == 1:
                key = matrixKeys[rowKey][colKey]
                print(f'you have pressed {key}')
                utime.sleep(0.3)
        row[rowKey].value(0)

testLed = machine.Pin(15,machine.Pin.OUT,machine.Pin.PULL_DOWN)

####################################################################
#Oled definitions
i2c = I2C(0,scl = Pin(17),sda = Pin(16))#create an object of the i2c

width = 128#of the oled in pixels
height = 64#of the oled in pixels

oled = SSD1306_I2C(width,height,i2c)#create an object of the oled

def draw_x(arr):
    xPos = arr[0]
    yPos = arr[1]
    oled.line(xPos,yPos,xPos+16,yPos+16,1)
    oled.line(xPos+16,yPos,xPos,yPos+16,1)
def draw_o(arr):
    xPos=arr[0]
    yPos =arr[1]
    oArray=[[0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],
            [0,0,0,1,1,0,0,0,0,0,1,1,0,0,0],
            [0,0,1,1,0,0,0,0,0,0,0,1,1,0,0],
            [0,0,1,0,0,0,0,0,0,0,0,0,1,0,0],
            [0,1,0,0,0,0,0,0,0,0,0,0,0,1,0],
            [0,1,0,0,0,0,0,0,0,0,0,0,0,1,0],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [0,1,0,0,0,0,0,0,0,0,0,0,0,1,0],
            [0,1,0,0,0,0,0,0,0,0,0,0,0,1,0],
            [0,0,1,0,0,0,0,0,0,0,0,0,1,0,0],
            [0,0,1,1,0,0,0,0,0,0,0,1,1,0,0],
            [0,0,0,1,1,0,0,0,0,0,1,1,0,0,0],
            [0,0,0,0,0,1,1,1,1,1,0,0,0,0,0]]
    for x in range(15):
      for y in range(15):
          oled.pixel(x+xPos,y+yPos,oArray[y][x])
def display(avatar,position):
    global key
    arrPos = [[10,0],[58,0],[101,0],[10,24],[58,24],[101,24],[10,46],[58,46],[101,46]]
    #oled.fill(0)
    oled.vline(43,0,64,1)#vertical line(x,y,length,color)
    oled.vline(86,0,64,1)
    oled.hline(0,21,128,1)
    oled.hline(0,42,128,1)
    if avatar == 'X':
        draw_x(arrPos[position-1])
    elif avatar == 'O':
        draw_o(arrPos[position-1])
    key = '0'
    oled.show()
def choose_avatar():
    avatar = ''
    oled.fill(0)
    oled.text('Choose your',0,0)
    oled.text('avatar player 1',0,10)
    oled.text('A --> X',0,20)
    oled.text('B --> O',0,30)
    oled.show()
    while avatar == '':
        print('start')
        global key
        key = '0'
        while key == '0':
            scanKey()
        if key == 'A':
            avatar = 'X'
            oled.fill(0)
            oled.text('Player 1 starts',0,0)
            oled.text('X avatar chosen',0,10)
            oled.text('choose numpad ',0,20)
            oled.text('position',0,30)
            oled.show()
        elif key == 'B':
            avatar = 'O'
            oled.fill(0)
            oled.text('Player 1 starts',0,0)
            oled.text('O avatar chosen',0,10)
            oled.text('choose numpad',0,20)
            oled.text('position',0,30)
            oled.show()
        else:
            oled.fill(0)
            oled.text('Wrong key',0,0)
            oled.text('Please Try again',0,10)
            oled.text('A --> X',0,20)
            oled.text('B --> O',0,30)
            oled.show()
        print('end')
    return avatar

def choose_num():
    global key
    global acceptableValues
    global filledValues
    withinRange = False
    
    while withinRange == False:
        key = '0'
        while key == '0':
            scanKey()
        if int(key) in acceptableValues:
            acceptableValues.pop(acceptableValues.index(int(key)))
    
            print(acceptableValues)
            withinRange = True
        else:
            withinRange = False
            print('the position is already occupied')
    return int(key)


def check_win(numList):
    winCombos = [[1,2,3],[1,4,7],[1,5,9],[4,5,6],[2,5,8],[3,5,7],[7,8,9],[3,6,9]]
    if len(numList)<3:
        return False
    else:
        for winCombo in range(0,8):
            code = winCombos[winCombo]
            for nam in numList:
                if nam == code[0]:
                    code.remove(nam)
            if len(code)==0:
                return True
        else:
            return False
#animation
def animation():
    centerX = 64
    centerY = 32

    for level in range(1,67):
        utime.sleep(0.01)
        if level == 1:
            oled.fill(0)
            oled.pixel(centerX,centerY,1)
            oled.show()
        else:
            change = level-1
            xLeft = centerX-change
            xRight = centerX +change
            yTop = centerY + change
            yBottom = centerY -change
            #print(xLeft)
            #print(yTop)
            #print(xRight)
            #print(yBottom)
            oled.fill(0)
            oled.line(xLeft,yTop,xRight,yTop,1)
            oled.line(xRight,yTop,xRight,yBottom,1)
            oled.line(xLeft,yTop,xLeft,yBottom,1)
            oled.line(xLeft,yBottom,xRight,yBottom,1)
            oled.show()

def gameplay():
    animation()
    oled.fill(0)
    oled.text('WELCOME',30,0)
    oled.text('TO',50,10)
    oled.text('TIC-TAC-TOE',20,20)
    oled.show()
    utime.sleep(2)
    avt = choose_avatar()
    if avt == 'X':
        avt2 = 'O'
    elif avt == 'O':
        avt2 = 'X'
    activePlayer = 1
    play1 = []
    play2 = []
    win = False#check win
    oled.fill(0)
    #while nobody has won and there are still slots on the board
    while win == False and len(acceptableValues)>0:
        num = choose_num()
        if activePlayer == 1:
            display(avt,num)
            activePlayer = 2
            play1.append(num)
            play1.sort()
            win = check_win(play1)
            print(play1)
        elif activePlayer == 2:
            display(avt2,num)
            activePlayer = 1
            play2.append(num)
            play2.sort()
            win = check_win(play2)
            print(play2)
        if win and activePlayer == 2:
            print('player one has won')
            animation()
            oled.fill(0)
            oled.text('WINNER',30,10)
            oled.text('player 1',25,20)
            oled.show()
            break
        elif win and activePlayer == 1:
            print('Player two has won')
            animation()
            oled.fill(0)
            oled.text('WINNER',30,10)
            oled.text('player 2',25,20)
            oled.show()
            break
    else:
        print('it is a draw')
        oled.fill(0)
        oled.text('NO WINNER',30,10)
        oled.text('DRAW',40,20)
        oled.show()



while True:
    key = '0'
    acceptableValues = [1,2,3,4,5,6,7,8,9]
    gameplay()
    utime.sleep(3)
    oled.fill(0)
    oled.text('To restart',0,0)
    oled.text('press any key',0,10)
    oled.show()
    key = 'wrong'
    while key == 'wrong':
        scanKey()

    
