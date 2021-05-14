from turtle import Turtle

class Bullet(Turtle):
    def __init__(self, position_x, position_y):
        super().__init__()
        self.penup()
        self.shape("circle")
        self.color("lime")
        self.shapesize(stretch_wid=0.2, stretch_len=0.6)
        self.bullet_speed = 13
        self.goto(position_x, position_y+20)
        self.setheading(90)

    def BulletMove(self):
        self.forward(self.bullet_speed)

    def DetectTopLimit(self):
        if self.ycor() > 260:
            self.hideturtle()
            self.clear()
            self.goto(2000,2000)
            return True
        return False

    def DestroyBullet(self):
        print("Bullet destroyed")
        self.goto(1000, 1000)
        self.hideturtle()
