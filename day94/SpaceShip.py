from turtle import Turtle

class SpaceShip(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.shape("ship")
        self.color("lime")
        self.setheading(90)
        self.shapesize(stretch_wid=2, stretch_len=2)
        self.respawn()

    def respawn(self):
        self.clear()
        self.goto(0,-260)

    def go_right(self):
        new_y = self.ycor()
        new_x = self.xcor() + 25
        self.goto(new_x, new_y)

    def go_left(self):
        new_y = self.ycor()
        new_x = self.xcor() - 25
        self.goto(new_x, new_y)