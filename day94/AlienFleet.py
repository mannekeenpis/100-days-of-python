from turtle import Turtle

class Fleet(Turtle):
    def __init__(self, x_position, y_position):
        super().__init__()
        self.aliens = []
        xcor = x_position
        ycor = y_position
        for row in range(0,3): #barrier rows
            for alien in range(0,8): # Barrier 'columns'
                newAlien = Alien(xcor=xcor, ycor=ycor)
                self.aliens.append(newAlien)
                xcor += 45
            ycor += 40
            xcor = x_position

    def MoveFleet(self):
        for alien in self.aliens:
            alien.forward(alien.speed)

    def changeFleetDirection(self):
        self.FleetDescent()
        for alien in self.aliens:
            if alien.heading() == 0:
                alien.setheading(180)
            else:
                alien.setheading(0)

    def DetectLeftRightBoundaries(self):
        for alien in self.aliens:
            if alien.xcor() > 265 or alien.xcor() < -265:
                self.changeFleetDirection()
                break

    def DetectLowerBoundary(self):
        for alien in self.aliens:
            if alien.ycor() < -190:
                return True

    def FleetDescent(self):
        for alien in self.aliens:
            alien.speed *= 1.01
            alien.goto(alien.xcor(), alien.ycor()-5)

    def DeleteAlien(self, Alien):
        Alien.clear()
        Alien.goto(3000, 3000)
        self.aliens.remove(Alien)
        del Alien

class Alien(Turtle):
    def __init__(self, xcor,ycor):
        super().__init__()
        self.shape('alien.gif')
        self.color("lime")
        self.penup()
        self.shapesize(stretch_wid=1.2, stretch_len=1.2)
        self.speed("fastest")
        self.goto(xcor,ycor)
        self.setheading(0)
        self.speed = 4