import turtle
import random

def firework():
    radius = random.randint(50, 120)
    angle_step = random.randint(10, 20)
    color = random.choice(['red', 'yellow', 'blue', 'green', 'purple', 'orange', 'white'])
    turtle.color(color)
    turtle.pensize(2)
    for angle in range(0, 360, angle_step):
        turtle.setheading(angle)
        turtle.forward(radius)
        turtle.backward(radius)

def main():
    screen = turtle.Screen()
    screen.bgcolor('black')
    turtle.speed(0)
    turtle.hideturtle()

    for _ in range(10):
        x = random.randint(-200, 200)
        y = random.randint(-200, 200)
        turtle.penup()
        turtle.goto(x, y)
        turtle.pendown()
        firework()

    screen.exitonclick()

if __name__ == '__main__':
    main()
