from turtle import Turtle

class Barrier(Turtle):
    def __init__(self, x_position, y_position):
        super().__init__()
        self.bricks = []
        xcor = x_position
        ycor = y_position
        for row in range(0,5): #barrier rows
            for brick in range(0,60): # Barrier 'columns'
                if brick == 21 or brick == 41:
                    xcor +=20
                newBrick = BarrierBrick(xcor=xcor, ycor=ycor)
                self.bricks.append(newBrick)
                xcor += 8
            ycor += 9
            xcor = x_position

    def DeleteBrick(self, brick):
        brick.clear()
        brick.goto(3000, 3000)
        self.bricks.remove(brick)
        del brick

class BarrierBrick(Turtle):
    def __init__(self, xcor,ycor):
        super().__init__()
        self.shape("square")
        self.color("lime")
        self.penup()
        self.shapesize(stretch_wid=0.3, stretch_len=0.3)
        self.speed("fastest")
        self.goto(xcor,ycor)