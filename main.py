import turtle
import time
import random
INVADERS_POS = [(50, 0), (100, 0), (150, 0),(0, 0), (-50, 0), (-100, 0), (-150, 0),
                (50, 30), (100, 30), (150, 30),(0, 30), (-50, 30), (-100, 30), (-150, 30),
                (50, 60), (100, 60), (150, 60), (0, 60), (-50, 60), (-100, 60), (-150, 60),
                (50, 90), (100, 90), (150, 90), (0, 90), (-50, 90), (-100, 90), (-150, 90)
                ]


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


class InvaderBullet(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape('square')
        self.shapesize(0.1, 0.1, 0.1)
        self.color('red')
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
        self.invaders_bullets = []
        self.count = 0
        self.speed = 2
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

    def invader_fire(self, x, y):
        invader_rocket = InvaderBullet()
        invader_rocket.setposition(x, y)
        self.invaders_bullets.append(invader_rocket)

    def new_game(self):
        self.window.clearscreen()
        self.__init__()

    def move(self):
        if self.invaders_ships[0].xcor() > 200 or self.invaders_ships[0].xcor() < -200:
            self.speed *= -1
        for ship in self.invaders_ships:
            ship.goto(ship.xcor() + self.speed, ship.ycor())
        self.window.update()

        for invader_rocket in self.invaders_bullets:
            invader_rocket.goto(invader_rocket.xcor(), invader_rocket.ycor() - 5)
            if self.plane.xcor() - 20 <= invader_rocket.xcor() <= self.plane.xcor() + 20 and\
                self.plane.ycor() - 5 <= invader_rocket.ycor() <= self.plane.ycor() + 5:
                print('You Lose!')
                self.new_game()
        for rocket in self.bullets:
            rocket.goto(rocket.xcor(), rocket.ycor() + 5)
            for ship in self.invaders_ships:
                if ship.xcor() - 10 <= rocket.xcor() <= ship.xcor() + 10 and\
                        ship.ycor() - 10 <= rocket.ycor() <= ship.ycor() + 10:
                    self.invaders_ships.remove(ship)
                    self.bullets.remove(rocket)
                    rocket.color('black')
                    ship.color('black')
        self.count += 1
        if self.count == 50:
            random_number = random.randint(0, len(self.invaders_ships) - 1)
            self.invader_fire(self.invaders_ships[random_number].xcor(), self.invaders_ships[random_number].ycor())
            self.count = 0

        time.sleep(0.01)
        self.window.ontimer(self.move)
game = Game()
