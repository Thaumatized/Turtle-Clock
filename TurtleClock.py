import turtle
import time
import math
import sys

Turtles = []
TurtleQueues = []
turtle.delay(1)
TurtleCount = 3
for i in range(TurtleCount):
    NewTurtle = turtle.Turtle()
    NewTurtle.shape("turtle")
    NewTurtle.speed(0)
    NewTurtle.penup()
    Turtles.append(NewTurtle)
    TurtleQueues.append([])

#Following are used to determine when to draw the clock arms
CurrentTime = 0
Hour = 0
Minute = 0
Second = 0
OldHour = 0
OldMinute = 0
OldSecond = 0
HourAngle = 0
MinuteAngle = 0
SecondAngle = 0

#Since I know some people will eventually read this code, here is how the Queues work.
#Each turtle has its own queue of instructions, which is handled as an array strings.
#Every instruction starts with a letter which notates the action of the instruction,
#and it is usually followed by a value. The value is whatever the turtle function that the action calls needs.
#
#The commands are as follows:
# F = forward
# R = right
# L = left
# U = penup
# D = pendown
# c = pencolor => changes the color the turtle draws and the outline of the turtle
# C = color => changes the color the turtle draws and the *ENTIRE* turtle's color
# S = pensize
# Z = undo, value is interpreted in the same way as for movements, so supplying the same value should undo the same amount.
# * = Sync => waits until all turtles have a * instruction. Value can be used as a debug comment to know where a sync instruction came in case of freezes. I used this by halting the program with ctrl+c and then lookign at the variables with thonny to see which one had a * left and where it was form.
#
# To draw with all the turtles simultaneously, fill up their queues by appending and then call ReadTurtleQueues
def ReadTurtleQueues(MaxStep = 5):
    while bool(TurtleQueues[0]) or bool(TurtleQueues[1]) or bool(TurtleQueues[2]):
        for i in range(TurtleCount):
            if bool(TurtleQueues[i]):
                Action = TurtleQueues[i][0][0:1]
                Amount = TurtleQueues[i][0][1:]
                if(Amount != "" and Action not in ["c", "C", "S", "*"]):
                    Amount = float(Amount)
                    if(Amount > MaxStep):
                        TurtleQueues[i][0] = Action + str(Amount - MaxStep)
                        Amount = MaxStep
                    else:
                        TurtleQueues[i].pop(0)
                elif Action == "*": #Sync!
                    AllTurtlesSynced=True
                    for i2 in range(TurtleCount):
                        AllTurtlesSynced = AllTurtlesSynced and TurtleQueues[i2][0][0:1] == "*"
                    if AllTurtlesSynced:
                        for i2 in range(TurtleCount):
                            TurtleQueues[i2].pop(0)
                else:
                        TurtleQueues[i].pop(0)
                
                # I know this is just the sort of place where you could use match; However since this is python it really doesn't matter. In other languages I would do it just for cleanliness, but for python I am totally ready to spend more time writing a comment which is frankly useless about it instead of actually doing it.
                if(Action == "F"):
                    Turtles[i].forward(Amount)
                elif(Action == "R"):
                    Turtles[i].right(Amount)
                elif(Action == "L"):
                    Turtles[i].left(Amount)
                elif(Action == "U"):
                    Turtles[i].penup()
                elif(Action == "D"):
                    Turtles[i].pendown()
                elif(Action == "c"):
                    Turtles[i].pencolor(Amount)
                elif(Action == "C"):
                    Turtles[i].color(Amount)
                elif(Action == "S"):
                    Turtles[i].pensize(float(Amount))
                elif(Action == "Z"):
                    Turtles[i].undo()
                elif(Action == "*"):
                    continue
                    # * = Syncpoint. Wait until every turtle has one.

def DrawClock():
    #Rotate the turtles to face their correct starting orientations
    TurtleQueues[0].append("L90")
    TurtleQueues[1].append("R30")
    TurtleQueues[2].append("R150")
    
    #Start of drawing the clock
    for i in range(3):

        TurtleQueues[i].append("* Start of DrawClock()")
        TurtleQueues[i].append("S15")
        TurtleQueues[i].append("F" + str(Radius))
        TurtleQueues[i].append("R90")

        Circumference = Radius*2*math.pi
        Steps = 720
        MySteps = int(Steps/3)

        StepAngle = 360/Steps
        StepLength = Circumference/Steps
        
        TurtleQueues[i].append("D")

        TurtleQueues[i].append("F" + str(StepLength/2))
        for j in range(MySteps-1):
            TurtleQueues[i].append("R" + str(StepAngle))
            TurtleQueues[i].append("F" + str(StepLength))
        TurtleQueues[i].append("R" + str(StepAngle))
        TurtleQueues[i].append("F" + str(StepLength/2))
        
        TurtleQueues[i].append("U")
        TurtleQueues[i].append("R90")
        TurtleQueues[i].append("F" + str(Radius))

        #Little lines to indicate minutes/hours
        for j in range(20):
            if(j%5 == 0):
                TurtleQueues[i].append("S5") # Hours
            else:
                TurtleQueues[i].append("S1") # Minutes
            TurtleQueues[i].append("F" + str(Radius*0.9))
            TurtleQueues[i].append("D")
            TurtleQueues[i].append("F" + str(Radius*0.05))
            TurtleQueues[i].append("U")
            TurtleQueues[i].append("R180")
            TurtleQueues[i].append("F" + str(Radius*0.95))
            TurtleQueues[i].append("R6")
            
        TurtleQueues[i].append("L" + str(60 + (i * 120)))#Bring the turtles back upright
        
    ReadTurtleQueues()
    #End of drawing the clock

def InitClockArms():
    global Hour, OldHour, HourAngle, Minute, OldMinute, MinuteAngle, Second, OldSecond, SecondAngle
    CurrentTime = time.localtime()
    Hour = CurrentTime[3]
    Minute = CurrentTime[4]
    Second = CurrentTime[5]
    OldHour = Hour
    OldMinute = Minute
    OldSecond = Second
    HourAngle = 360/12*(Hour%12)
    TurtleQueues[0].append("S5")
    TurtleQueues[0].append("D")
    TurtleQueues[0].append("R"+str(HourAngle))
    TurtleQueues[0].append("* Init Clock arms hour")
    TurtleQueues[0].append("F" + str(Radius/2))
    TurtleQueues[0].append("U")
    TurtleQueues[0].append("F" + str(Radius/3))
    MinuteAngle = 360/60*Minute
    TurtleQueues[1].append("S3")
    TurtleQueues[1].append("D")
    TurtleQueues[1].append("R"+str(MinuteAngle))
    TurtleQueues[1].append("* Init Clock arms minute")
    TurtleQueues[1].append("F" + str(Radius/6*5))
    SecondAngle = 360/60*Second
    TurtleQueues[2].append("C#FF0000")
    TurtleQueues[2].append("D")
    TurtleQueues[2].append("R"+str(SecondAngle))
    TurtleQueues[2].append("* Init Clock arms second")
    TurtleQueues[2].append("F" + str(Radius/6*5))
    ReadTurtleQueues(30)

def SyncedHome():
    #NOTE turtle angle is in a counter clockwise direction
    #Vertical Home
    for i in range(3):
        TurtleRot = Turtles[i].heading()
        if(Turtles[i].ycor() < 0):
            TurtleQueues[i].append("L" + str(90 - TurtleRot)) # Look Up
            TurtleQueues[i].append("*  sync home 1") # Sync up -> rotate all turtles before moving
            TurtleQueues[i].append("F" + str(-Turtles[i].ycor()))
            TurtleQueues[i].append("* sync home 2") # Sync up -> rotate all turtles after moving
            TurtleRot = 90
        elif(Turtles[i].ycor() > 0):
            TurtleQueues[i].append("L" + str(270 - TurtleRot)) # Look Down
            TurtleQueues[i].append("* sync home 3") # Sync up -> rotate all turtles before moving
            TurtleQueues[i].append("F" + str(Turtles[i].ycor()))
            TurtleQueues[i].append("* sync home 4") # Sync up -> rotate all turtles after moving
            TurtleRot = 270
        else:
            TurtleQueues[i].append("* sync home 5") # When syncing we need to sync all the turtles regardless of if they move.
            TurtleQueues[i].append("* sync home 6")
        
        if(Turtles[i].xcor() <= 0):
            TurtleQueues[i].append("L" + str(0 - TurtleRot)) # Look Right
            TurtleQueues[i].append("* sync home 7") # Sync up -> rotate all turtles before moving
            TurtleQueues[i].append("F" + str(-Turtles[i].xcor()))
        else: # GO BACK
            TurtleQueues[i].append("L" + str(180 - TurtleRot)) # Look Left
            TurtleQueues[i].append("* sync home 8") # Sync up -> rotate all turtles before moving
            TurtleQueues[i].append("F" + str(Turtles[i].xcor()))
            TurtleQueues[i].append("R180")      
    ReadTurtleQueues()
        

def InitClock():
    for i in range(3):
            TurtleQueues[i].append("U")
            TurtleQueues[i].append("C#000000")
            Turtles[i].clear()
    SyncedHome()
    DrawClock()
    InitClockArms()

def RefreshClock():
    global Hour, OldHour, HourAngle, Minute, OldMinute, MinuteAngle, Second, OldSecond, SecondAngle
    
    RefreshHour = OldHour != Hour
    RefreshMinute = OldMinute != Minute
    RefreshSecond = OldSecond != Second
        
    if RefreshHour:
        OldHourAngle = HourAngle
        HourAngle = 360/12*(Hour%12)
        #These come in two because the steps need to match the drawing of the hand in order to not slowly drift out of sync.
        TurtleQueues[0].append("Z"+ str(Radius/2))
        TurtleQueues[0].append("Z") # This undoes the lifting of the pen.
        TurtleQueues[0].append("Z" + str(Radius/3))

        TurtleQueues[0].append("S5")
        TurtleQueues[0].append("C#000000")
        TurtleQueues[0].append("R"+str(HourAngle - OldHourAngle))
        TurtleQueues[0].append("* From refreshing hour")
        TurtleQueues[0].append("F" + str(Radius/2))
        TurtleQueues[0].append("U")
        TurtleQueues[0].append("F" + str(Radius/3))

        OldHour = Hour
    else:
        TurtleQueues[0].append("* From not refreshing hour")
    
    if RefreshMinute:
        OldMinuteAngle = MinuteAngle
        MinuteAngle = 360/60*Minute
        TurtleQueues[1].append("Z" + str(Radius/6*5))

        TurtleQueues[1].append("S3")
        TurtleQueues[1].append("C#000000")
        TurtleQueues[1].append("R"+str(MinuteAngle - OldMinuteAngle))
        TurtleQueues[1].append("* From refreshing minute")
        TurtleQueues[1].append("F" + str(Radius/6*5))

        OldMinute = Minute
    else:
        TurtleQueues[1].append("* From not refreshing minute")
        
    if RefreshSecond:
        OldSecondAngle = SecondAngle
        SecondAngle = 360/60*Second
        TurtleQueues[2].append("Z" + str(Radius/6*5))

        TurtleQueues[2].append("S1")
        TurtleQueues[2].append("C#FF0000")
        TurtleQueues[2].append("R"+str(SecondAngle - OldSecondAngle))
        TurtleQueues[2].append("* From refreshing second")
        TurtleQueues[2].append("F" + str(Radius/6*5))

        OldSecond = Second
    else:
        TurtleQueues[2].append("* From not refreshing second")
        
    ReadTurtleQueues(30)
    
WindowSize = (turtle.window_width(), turtle.window_height())
Radius = min(turtle.window_width(), turtle.window_height()) * 0.8 / 2

if("-f" in sys.argv):
    turtle.delay(0)

InitClock()
turtle.delay(10)
while True:
    if WindowSize != (turtle.window_width(), turtle.window_height()):
        WindowSize = (turtle.window_width(), turtle.window_height())
        Radius = min(turtle.window_width(), turtle.window_height()) * 0.8 / 2
        turtle.delay(0)
        InitClock()
        turtle.delay(10)

    CurrentTime = time.localtime()
    if Second == CurrentTime[5]:
        # (1 (time.time() - int(time.time()))) would get us exactly to the next second,
        # except in practice there seem to seems to be too much variation in the delay
        # => 0.1 won't skip seconds or refresh immiditealy after the first update is done.
        time.sleep(0.1)
        continue

    Hour = CurrentTime[3]
    Minute = CurrentTime[4]
    Second = CurrentTime[5]
    
    RefreshClock()
