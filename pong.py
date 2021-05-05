import turtle
# simple for graphics

wn = turtle.Screen()
# this creates a window
wn.title('Pong by Judith')
wn.bgcolor('black')
wn.setup(width=800, height=600)
wn.tracer(0)
# stops the window from updating, so we have to manually do that

# Paddle A

paddleA = turtle.Turtle()  # this creates an object
paddleA.speed(0)  # speed of the animation is set to max
paddleA.shape('square')
paddleA.color('orange')
paddleA.shapesize(stretch_wid=5, stretch_len=1)
paddleA.penup()
paddleA.goto(-350, 0)  # starting position

# Paddle B

paddleB = turtle.Turtle()  # this creates an object
paddleB.speed(0)  # speed of the animation is set to max
paddleB.shape('square')
paddleB.color('white')
paddleB.shapesize(stretch_wid=5, stretch_len=1)
paddleB.penup()
paddleB.goto(+350, 0)  # starting position

# Ball
ball = turtle.Turtle()  # this creates an object
ball.speed(0)  # speed of the animation is set to max
ball.shape('square')
ball.color('green')
ball.penup()
ball.goto(0, 0)  # starting position

# every time the ball moves, it moves by X px
ball.dx = 0.2
ball.dy = 0.2

# Score

scoreA = 0
scoreB = 0

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.color('red')
pen.penup()  # we don't want to see a line every time it moves
pen.hideturtle()
pen.goto(0, 260)
pen.write('Player A: {}  |  Player B: {}'.format(scoreA, scoreB), align='center',
          font=('Courier', 24, 'normal'))


# Paddle methods


def paddleA_up():
    y = paddleA.ycor()  # returns the y coordinate
    y += 20
    paddleA.sety(y)


def paddleA_down():
    y = paddleA.ycor()  # returns the y coordinate
    y -= 20
    paddleA.sety(y)


def paddleB_up():
    y = paddleB.ycor()  # returns the y coordinate
    y += 20
    paddleB.sety(y)


def paddleB_down():
    y = paddleB.ycor()  # returns the y coordinate
    y -= 20
    paddleB.sety(y)


# Keyboard binding

wn.listen()
wn.onkeypress(paddleA_up, 'w')
wn.onkeypress(paddleA_down, 's')
wn.onkeypress(paddleB_up, 'Up')
wn.onkeypress(paddleB_down, 'Down')

# Main game loop, all main functions go here


while True:
    wn.update()
    # every time the loop runs, it updates the screen

    # move the ball
    ball.setx(ball.xcor()+ball.dx)
    ball.sety(ball.ycor()+ball.dy)

    # border checking
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1  # this reverses the direction

    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1

    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball.dx *= -1
        scoreA += 1
        pen.clear()
        pen.write('Player A: {}  |  Player B: {}'.format(scoreA, scoreB), align='center',
                  font=('Courier', 24, 'normal'))

    if ball.xcor() < -390:
        ball.goto(0, 0)
        ball.dx *= -1
        scoreB += 1
        pen.clear()
        pen.write('Player A: {}  |  Player B: {}'.format(scoreA, scoreB), align='center',
                  font=('Courier', 24, 'normal'))

    # handle collisions
    if (ball.xcor() > 340 and ball.xcor() < 350) and (ball.ycor() < paddleB.ycor()+40 and ball.ycor() > paddleB.ycor()-40):
        ball.setx(340)
        ball.dx *= -1

    if (ball.xcor() < -340 and ball.xcor() > -350) and (ball.ycor() < paddleA.ycor()+40 and ball.ycor() > paddleA.ycor()-40):
        ball.setx(-340)
        ball.dx *= -1
