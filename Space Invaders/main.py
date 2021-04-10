import turtle
import os
import math
import random


# Establishes player default attributes and movement functionalities
class Player:
    def __init__(self):
        # Create player turtle
        self.turtle = turtle.Turtle()
        self.turtle.shape('player.gif')
        self.turtle.penup()
        self.turtle.speed(0)
        self.turtle.setposition(0, -250)
        self.turtle.setheading(90)
        self.step = 15

        self.bullet = turtle.Turtle()
        self.bullet.speed(0)
        self.bullet.shape('bullet.gif')
        self.bullet.shapesize(0.5, 0.5)
        self.bullet.penup()
        self.bullet.setheading(90)
        self.bullet_step = 20
        self.bullet.hideturtle()

    def move_left(self):
        x = self.turtle.xcor()
        x -= self.step
        if x < -280:
            x = -280
        self.turtle.setx(x)

    def move_right(self):
        x = self.turtle.xcor()
        x += self.step
        if x > 280:
            x = 280
        self.turtle.setx(x)

    def fire_bullet(self):
        if not self.bullet.isvisible():
            # set position of bullet just above player
            x = self.turtle.xcor()
            y = self.turtle.ycor() + 20
            self.bullet.setposition(x, y)
            os.system('afplay laser.wav&')
            self.bullet.showturtle()


# Establishes default attributes of enemies
class Enemy:
    def __init__(self):
        # Create enemies
        self.turtle = turtle.Turtle()
        self.turtle.shape('invader.gif')
        self.turtle.speed(0)
        self.turtle.penup()
        self.turtle.setposition(random.randint(-280, 280), random.randint(0, 280))
        self.turtle.setheading(270)
        self.x_step = 2
        self.y_step = 40

    def move(self):
        x = self.turtle.xcor()
        x += self.x_step
        if x > 280:
            x = 280
        self.turtle.setx(x)

    def move_down(self):
        y = self.turtle.ycor()
        y -= self.y_step
        if y < -250:
            y = -250
        self.turtle.sety(y)


def is_collision(t1, t2):
    # Distance between two turtles
    distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))

    # If distance between two turtles is less than 15 pixels, treat as collision.
    if distance < 15:
        os.system('afplay explosion.wav&')
        return True

    else:
        return False


# Setting up Screen
window = turtle.Screen()
window.bgcolor("black")
window.title("Space Invaders Concept")
window.bgpic("space_invaders_background.gif")

# Register Shapes
window.register_shape('invader.gif')
window.register_shape('player.gif')
window.register_shape('bullet.gif')

# Draw border
border_pen = turtle.Turtle()
border_pen.color('white')
border_pen.pensize(3)
border_pen.speed(0)
border_pen.penup()
border_pen.setposition(-300, -300)
border_pen.pendown()

for edge in range(4):
    border_pen.forward(600)
    border_pen.left(90)

border_pen.hideturtle()

# Create player
player = Player()

# Create fixed number of enemies
number_of_enemies = 5
enemies = []
for i in range(number_of_enemies):
    enemy = Enemy()
    enemies.append(enemy)

# Keyboard bindings
window.listen()  # turtle listens for key inputs
window.onkey(player.move_left, 'Left')
window.onkey(player.move_right, 'Right')
window.onkey(player.fire_bullet, 'space')

# Create scoring system
score = 0
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color('white')
score_pen.penup()
score_pen.setposition(-290, 275)
score_string = f'Score: {score}'
score_pen.write(score_string, False, "left", ("Arial", 16, "normal"))
score_pen.hideturtle()

# Main game loop
playing = True
while playing is True:

    for enemy in enemies:
        enemy.move()

        if enemy.turtle.xcor() >= 280 or enemy.turtle.xcor() <= -280:       # boundary
            for enemy in enemies:
                enemy.x_step *= -1                                          # move horizontally in the opposite direction

            for enemy in enemies:
                enemy.move_down()                                           # shift down all enemies when one reaches boundary

        if is_collision(player.bullet, enemy.turtle) is True:
            # Reset enemy
            enemy.turtle.hideturtle()
            enemy.turtle.setposition(random.randint(-280, 280), random.randint(0, 280))
            enemy.turtle.showturtle()
            # Reset bullet
            player.bullet.setposition(0, -400)
            player.bullet.hideturtle()

            # Update Score
            score += 10
            score_string = f'Score: {score}'
            score_pen.clear()                                                       # clear writing first
            score_pen.write(score_string, False, "left", ("Arial", 16, "normal"))   # then rewrite score

        if is_collision(player.turtle, enemy.turtle):
            player.turtle.hideturtle()
            for enemy in enemies:
                enemy.turtle.hideturtle()

            print('Game Over')
            window.clear()
            window.title('Game Over')
            playing = False
            break

    # move bullet up if bullet is on screen
    if player.bullet.isvisible():
        y = player.bullet.ycor()
        y += player.bullet_step
        player.bullet.sety(y)

    # check if bullet has exceeded boundaries
    if player.bullet.ycor() > 290:
        player.bullet.hideturtle()






