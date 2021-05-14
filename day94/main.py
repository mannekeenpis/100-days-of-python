from turtle import Screen
from AlienFleet import Fleet
from SpaceShip import SpaceShip
from Barrier import Barrier
from Scoreboard import Scoreboard
from time import sleep
from bullet import Bullet
import random
from AlienBomb import AlienBombManager

screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("Space Invasion!!")
screen.tracer(0)
screen.register_shape('ship', ((-10,0),(0,10),(10,0)))
screen.register_shape('alien.gif')


def FireBullet():
    global bullet
    if bullet == None:
        bullet = Bullet(position_x=player.xcor(), position_y=player.ycor())


def DeleteBullet():
    global bullet
    bullet.goto(3000,3000)
    bullet.clear()
    del bullet
    bullet = None


def RandomAlienBomb():
    random_chance = random.randint(1, 12)
    if random_chance == 1:
        random_alien = random.choice(fleet.aliens)
        bomb.MakeBomb(position_x=random_alien.xcor(), position_y=random_alien.ycor())


player = SpaceShip()
barrier1 = Barrier(-260, -220)
fleet = Fleet(-240, 160)
bomb = AlienBombManager()
bullet = None
scoreboard = Scoreboard()

# Initialise game
screen.update()
screen.listen()
screen.onkey(player.go_left, "a")
screen.onkey(player.go_right, "d")
screen.onkey(FireBullet, "space")
game_is_on = True
while game_is_on == True:
    sleep(0.0001)
    screen.update()
    if len(fleet.aliens) <=0:
        scoreboard.GameOver(Reason="Won")
        game_is_on = False
    if scoreboard.lives <= 0:
        scoreboard.GameOver(Reason="Lives")
        game_is_on = False

    # ALIEN MOVES
    fleet.MoveFleet()
    fleet.DetectLeftRightBoundaries()
    if fleet.DetectLowerBoundary() == True:
        scoreboard.GameOver(Reason="Invaded")
        game_is_on = False

    # ALIEN BOMB ACTIONS
    RandomAlienBomb()
    bomb.moveBombs()
    bomb.DetectLowerLimit()
    for bombx in bomb.bombs:
        if player.distance(bombx) < 20:
            scoreboard.RemoveLife()
            bomb.DeleteBomb(Bomb=bombx)
            player.respawn()
            continue
        for brick in barrier1.bricks:
            if bombx.distance(brick) < 7:
                barrier1.DeleteBrick(brick=brick)
                bomb.DeleteBomb(Bomb=bombx)
                continue

    # PLAYER BULLET ACTIONS
    if bullet != None:
        bullet.BulletMove()
        if bullet.DetectTopLimit() == True:
            DeleteBullet()
        else:
            for brick in barrier1.bricks:
                if bullet.distance(brick) <8:
                    barrier1.DeleteBrick(brick=brick)
                    DeleteBullet()
                    break
            if bullet != None:
                for alien in fleet.aliens:
                    if bullet.distance(alien) <10:
                        fleet.DeleteAlien(alien)
                        scoreboard.score += 20
                        scoreboard.RefreshScore()
                        DeleteBullet()
                        break
            if bullet != None:
                for bombx in bomb.bombs:
                    if bullet.distance(bombx) <5:
                        bomb.DeleteBomb(bombx)
                        scoreboard.score += 5
                        scoreboard.RefreshScore()
                        DeleteBullet()
                        break

screen.mainloop()
screen.exitonclick()