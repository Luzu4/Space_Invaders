import turtle
import time

INVADERS_POS = [(50, 0), (100, 0), (150, 0)]


class Ship(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.fillcolor('red')
        self.pencolor('white')
        self.shapesize(3, 3, 3)
        self.penup()
        self.left(90)
        self.setposition(0,-250)


class Invaders(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.color('white')
        self.penup()
        self.right(90)


class Bullet(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape('square')
        self.shapesize(0.1, 0.1, 0.1)
        self.color('white')
        self.penup()

class Game:
    def __init__(self):
        self.window = turtle.Screen()
        self.window.setup(800, 600)
        self.window.bgcolor('black')
        self.window.tracer(0)
        self.window.title('Space Invaders')
        self.invaders_ships = []
        self.bullets = []
        self.speed = 5
        self.plane = Ship()
        self.set_invaders()
        self.window.onkeypress(self.move_left, 'Left')
        self.window.onkeypress(self.move_right, 'Right')
        self.window.onkey(self.fire, 'space')
        self.move()
        self.window.listen()
        self.window.mainloop()

    def move_right(self):
        self.plane.goto(self.plane.xcor()+5, self.plane.ycor())

    def move_left(self):
        self.plane.goto(self.plane.xcor()-5, self.plane.ycor())

    def set_invaders(self):
        for invader in INVADERS_POS:
            invader_ship = Invaders()
            self.invaders_ships.append(invader_ship)
            invader_ship.setposition(invader[0], invader[1])

    def fire(self):
        rocket = Bullet()
        rocket.setposition(self.plane.xcor(), self.plane.ycor())
        self.bullets.append(rocket)

    def move(self):
        if self.invaders_ships[0].xcor() > 200 or self.invaders_ships[0].xcor() < -200:
            self.speed *= -1
        for ship in self.invaders_ships:
            ship.goto(ship.xcor() + self.speed, ship.ycor())
        self.window.update()
        self.window.ontimer(self.move)
        for rocket in self.bullets:
            rocket.goto(rocket.xcor(), rocket.ycor() + 5)
            for ship in self.invaders_ships:
                if ship.xcor() - 10 <= rocket.xcor() <= ship.xcor() + 10 and\
                        ship.ycor() - 10 <= rocket.ycor() <= ship.ycor() + 10:
                    self.invaders_ships.remove(ship)
                    ship.color('black')
        time.sleep(0.01)

game = Game()