from turtle import Turtle

class AlienBombManager(Turtle):
    def __init__(self):
        super().__init__()
        self.bombs = []
        self.bomb_fall_speed = 9

    def MakeBomb(self, position_x, position_y):
        NewBomb = Turtle()
        NewBomb.penup()
        NewBomb.shape("circle")
        NewBomb.color("lime")
        NewBomb.shapesize(stretch_wid=0.5, stretch_len=0.5)
        NewBomb.goto(position_x, position_y-5)
        NewBomb.setheading(270)
        self.bombs.append(NewBomb)

    def moveBombs(self):
        for bomb in self.bombs:
            bomb.forward(self.bomb_fall_speed)

    def DetectLowerLimit(self):
        for bomb in self.bombs:
            if bomb.ycor() < - 290:
                self.DeleteBomb(bomb)

    def DeleteBomb(self, Bomb):
        Bomb.clear()
        Bomb.goto(3000, 3000)
        self.bombs.remove(Bomb)
        del Bomb
