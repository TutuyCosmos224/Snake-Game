import turtle
import time
import random

delay = 200                             # speed of snake

# screen
game = turtle.Screen()                 
contact = 0
seconds = 0
game.title(f'Snake Game | Contacted: {contact} Time: {seconds}')
game.bgcolor("white")
game.setup(width=500, height=500)
game.tracer(0)

# parameters for title
contact_check = False                   
time_start = time.time()

# starting game message
text = turtle.Turtle()                  
text.speed(0)
text.shape("square")
text.color("black")
text.penup()
text.goto(0,140)
content ="""
    Welcome to Hansen Emanuel's Snake Game!
    You have to use your arrow keys to move the snake around, try
    to consume all the food, and don't let the monster catches you!
            
    Click anywhere on the screen to start the game..."""
text.write(content, align="center", font=("Verdana", 10, "normal"))
text.hideturtle()

# snake head
snake_head = turtle.Turtle()            
snake_head.speed(0)
snake_head.color("red")
snake_head.shape("square")
snake_head.penup()
snake_head.goto(0,0)
snake_headDirection = "stop"
previousDirection = "stop"

# body of the snake
body = []       
for i in range (0,5):
    body_segment = turtle.Turtle()
    body_segment.speed(0)
    body_segment.color("blue","black")
    body_segment.shape("square")
    body_segment.penup()
    body_segment.goto(-10000,-10000)
    body.append(body_segment)

# monster
monster = turtle.Turtle()               
monster.speed(0)
monster.color("purple")
monster.shape("square")
monster.penup()
xcoor = random.randint(-230,230)
ycoor = random.randint(-230,-180)
monster.goto(xcoor,ycoor)

food_list = []                          # food list

total = 0                               # the number of times the body lengthens

temp = delay                            # parameters for changing speed
extended_delay = delay + 100

start_counter = 0                       # to make sure the program only start once with a click

pause_check = False                     # to check if the program is paused

paused_time = 0                         # to paused the timer
paused_start = 0

game_stop = False                       # parameter to stop the game


def keyBindings(x):                      # game input    
    if x == True: 
        game.listen()
        game.onkeypress(move_up,"Up")
        game.onkeypress(move_down,"Down")
        game.onkeypress(move_left,"Left")
        game.onkeypress(move_right,"Right")
    elif x == False:
        game.listen()
        game.onkeypress(stop_move, "Up")
        game.onkeypress(stop_move, "Down")
        game.onkeypress(stop_move, "Left")
        game.onkeypress(stop_move, "Right")

def start(x,y):                         # start of the game:
    global start_counter
    text.clear()
    if start_counter < 1:
        for i in range (1,10):          # Displaying food on the screen
            food = turtle.Turtle()
            food.speed(0)
            food.color("black")
            food.penup()
            food.hideturtle()
            x = 0
            y = 0
            x = random.randint(-230,230)
            y = random.randint(-230,230)
            food.goto(x,y)
            food.write(i, align="center",font = ("Arial",9,"normal"))
            food_list.append(food)
        start_counter += 1

    keyBindings(True)
    
def move_up():                          # direction
    global snake_headDirection    
    snake_headDirection = "up"

def move_down():
    global snake_headDirection
    snake_headDirection = "down"

def move_left():
    global snake_headDirection    
    snake_headDirection = "left"

def move_right():
    global snake_headDirection
    snake_headDirection = "right"

def stop_move():
    global snake_headDirection
    snake_headDirection = "stop"

def movement_Snake():                   # movement of the snake, including body
    global game_stop, snake_headDirection, paused_time, pause_check
    if game_stop == False:
        if (snake_headDirection == "up" and snake_head.ycor() < 240) or (snake_headDirection == "down" and snake_head.ycor() > -240) or (snake_headDirection == "left" and snake_head.xcor() > -240) or (snake_headDirection == "right" and snake_head.xcor() < 240):
            for i in range (len(body)-1,0,-1):           # Put the body segments behind the head
                x = body[i-1].xcor()
                y = body[i-1].ycor()
                body[i].goto(x,y)
                body[i].showturtle()

            x = snake_head.xcor()
            y = snake_head.ycor()
            body[0].goto(x,y)
            body[0].showturtle()

        if snake_headDirection == "up" and snake_head.ycor() < 240:
            y = snake_head.ycor()
            snake_head.sety(y + 20)

        if snake_headDirection == "down" and snake_head.ycor() > -240:
            y = snake_head.ycor()
            snake_head.sety(y - 20)

        if snake_headDirection == "left" and snake_head.xcor() > -240:
            x = snake_head.xcor()
            snake_head.setx(x - 20)

        if snake_headDirection == "right" and snake_head.xcor() < 240:
            x = snake_head.xcor()
            snake_head.setx(x + 20)

        if pause_check == False:
            seconds = int(time.time()-time_start - paused_time)          # To give update for timer and contacted in the title everytime it moves
            game.title(f'Snake Game | Contacted: {contact} Time: {seconds}')

        game.ontimer(movement_Snake,delay)

def movement_Monster():                    # Movement of the monster
    global contact, contact_check, temp, game_stop, snake_headDirection
    if game_stop == False:
        if snake_headDirection != "stop":
            snake_x = snake_head.xcor()
            snake_y = snake_head.ycor()
            monster_x = monster.xcor()
            monster_y = monster.ycor()
            difference_x = monster_x - snake_x
            difference_y = monster_y - snake_y
            
            if abs(difference_x) >= abs(difference_y):
                if difference_x > 0:
                    x = monster.xcor()
                    monster.setx(x - 20)
                if difference_x < 0:
                    x = monster.xcor()
                    monster.setx(x + 20)
            else:
                if difference_y > 0:
                    y = monster.ycor()
                    monster.sety(y - 20)
                if difference_y < 0:
                    y = monster.ycor()
                    monster.sety(y + 20)
    
        check = 0

        for n in body:              # Checking for monster's contact with snake body
            if n.distance(monster) < 20 and contact_check == False:
                contact += 1
                contact_check = True
            if n.distance(monster) > 20:
                check += 1

        if check == len(body):
            contact_check = False

        game.ontimer(movement_Monster,random.randint(temp-50,temp+400))    

def eatFood():                      # function for when a food was eaten
    index = 0
    total = 0

    while index < len(food_list):               # looking which food was eaten
        if food_list[index].distance(snake_head) < 15:
            food_list[index].goto(10000,-10000) 
            food_list[index].clear()
            total = total + index + 1
        index += 1

    for i in range (0,total):                   # creating body segments
        body_segment = turtle.Turtle()
        body_segment.speed(0)
        body_segment.color("blue","black")
        body_segment.shape("square")
        body_segment.penup()
        body_segment.goto(10000,10000)
        body.append(body_segment)

def pause_game():                   # function for pausing the game               
    global snake_headDirection, previousDirection, paused_time, paused_start, stop_move, pause_check
    if snake_headDirection != "stop":
        previousDirection = snake_headDirection
        stop_move()
        paused_start = time.time()
        keyBindings(False)
        pause_check = True
    else:
        snake_headDirection = previousDirection
        paused_time += int(time.time() - paused_start)
        keyBindings(True)
        pause_check = False

# player input        
game.listen()
game.onscreenclick(start)
game.onkeypress(pause_game,"space")

movement_Snake()
movement_Monster()

while True:                             # main loop
    game.update()

    eatFood()

    for n in body:                      # if there is new body segments, delay added
        x = n.xcor()
        y = n.ycor()
        if x == 10000 and y == 10000:
            delay = extended_delay
            break
        else:
            delay = temp

    if snake_head.distance(monster) < 20:
        game.update()
        snake_head.write("GAME OVER!!!  ",align = "center", font = ("Verdana", 16, "bold"))
        game_stop = True
        break

    if len(body) == 50 and delay == temp:
        game.update()
        snake_head.write("WINNER!!!  ",align = "center", font = ("Verdana", 16, "bold"))
        game_stop = True
        break

game.mainloop()