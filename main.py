import turtle
import time
import random
from operator import itemgetter

ALIGNMENT = "center"
FONT = ("Courier", 24, "normal")
HIGH_SCORE = 0
INVADERS_DOWN_SPEED = 500
INVADERS_POS = [(-150, 90), (-150, 60), (-150, 30), (-150, 0),
                (50, 0), (100, 0), (150, 0), (0, 0), (-50, 0), (-100, 0),
                (50, 30), (100, 30), (150, 30), (0, 30), (-50, 30), (-100, 30),
                (50, 60), (100, 60), (0, 60), (-50, 60), (-100, 60),
                (50, 90), (100, 90), (0, 90), (-50, 90), (-100, 90), (150, 60), (150, 90)]

# Sort list for
INVADERS_POS.sort(key=itemgetter(0))

turtle.register_shape("smallinvader.gif")
turtle.register_shape("smallship.gif")
turtle.register_shape("spaceinvaders.gif")

class Ship(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape('smallship.gif')
        self.shapesize(3, 3, 3)
        self.penup()
        self.left(90)
        self.setposition(0, -250)


class Invaders(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape('smallinvader.gif')
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
        self.shapesize(0.2, 0.2, 0.2)
        self.color('red')
        self.penup()


class Scoreboard(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.penup()
        self.color('white')
        self.goto(0, 250)
        self.hideturtle()
        self.update_scoreboard()

    def update_scoreboard(self):
        self.write(f'Score: {self.score}, HIGH SCORE: {HIGH_SCORE}', align=ALIGNMENT, font=FONT)

    def increase_score(self):
        global HIGH_SCORE
        self.score += 100
        if HIGH_SCORE < self.score:
            HIGH_SCORE += 100
        self.clear()
        self.update_scoreboard()


class Title(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape('spaceinvaders.gif')
        self.goto(0,200)

class Game:
    def __init__(self):
        self.window = turtle.Screen()
        self.window.setup(800, 600)
        self.window.tracer(0)
        self.menu()
        self.window.mainloop()

    def make_square(self,pen):
        pen.forward(120)
        pen.left(90)
        pen.forward(30)
        pen.left(90)

    def menu(self):
        self.window.clearscreen()
        self.window.bgcolor('black')
        title = Title()
        self.window.tracer(0)
        pen = turtle.Turtle()
        pen.pencolor('white')
        pen.hideturtle()
        pen.goto(-60, 0)
        for i in range(2):
            self.make_square(pen)
        pen.penup()
        pen.goto(-53,6)
        pen.write('New Game', font=('Arial', 12, 'normal'))
        pen.goto(-60,-60)
        pen.pendown()
        for i in range(2):
            self.make_square(pen)
        pen.penup()
        pen.goto(-53,-54)
        pen.write('Difficulty', font=('Arial', 12, 'normal'))

        def button_click(x, y):
            if -60 <= x <= 60 and 0 <= y <= 30:
                self.new_game()
            if -60 <= x <= 60 and -60 <= y <= -30:
                self.difficult_choice()

        turtle.onscreenclick(button_click, 1)
        turtle.listen()
        turtle.done()

    def difficult_choice(self):
        self.window.clearscreen()
        self.window.bgcolor('black')
        title = Title()
        self.window.tracer(0)
        pen = turtle.Turtle()
        pen.pencolor('white')
        pen.hideturtle()
        pen.goto(-60, 0)
        for i in range(2):
            self.make_square(pen)
        pen.penup()
        pen.goto(-53, 6)
        pen.write('EASY', font=('Arial', 12, 'normal'))
        pen.goto(-60, -60)
        pen.pendown()
        for i in range(2):
            self.make_square(pen)
        pen.penup()
        pen.goto(-53,-54)
        pen.write('HARD', font=('Arial', 12, 'normal'))

        def button_click(x, y):
            global INVADERS_DOWN_SPEED
            if -60 <= x <= 60 and 0 <= y <= 30:
                INVADERS_DOWN_SPEED = 500
                self.menu()
            if -60 <= x <= 60 and -60 <= y <= -30:
                INVADERS_DOWN_SPEED = 50
                self.menu()

        turtle.onscreenclick(button_click, 1)
        turtle.listen()
        turtle.done()

    def new_game(self):
        self.window.clearscreen()
        self.window.bgpic('space.gif')
        # self.window.bgcolor('black')
        self.window.tracer(0)
        self.window.title('Space Invaders')
        self.invaders_ships = []
        self.bullets = []
        self.invaders_bullets = []
        self.count = 0
        self.heights = 0
        self.count_heights = 0
        self.speed = 2
        self.plane = Ship()
        self.scoreboard = Scoreboard()
        self.set_invaders()
        self.window.onkeypress(self.move_left, 'Left')
        self.window.onkeypress(self.move_right, 'Right')
        self.window.onkey(self.fire, 'space')
        self.move()
        self.window.listen()

    def move_right(self):
        if self.plane.xcor() < 400:
            self.plane.goto(self.plane.xcor() + 5, self.plane.ycor())

    def move_left(self):
        if self.plane.xcor() > -400:
            self.plane.goto(self.plane.xcor() - 5, self.plane.ycor())

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

    def move(self):
        if self.invaders_ships[len(self.invaders_ships) - 1].xcor() >= 400 or self.invaders_ships[0].xcor() <= -400:
            self.speed *= -1
        for ship in self.invaders_ships:
            if ship.ycor() <= self.plane.ycor():
                self.new_game()
            ship.goto(ship.xcor() + self.speed, ship.ycor() + self.heights)
        for invader_rocket in self.invaders_bullets:
            invader_rocket.goto(invader_rocket.xcor(), invader_rocket.ycor() - 5)
            if self.plane.xcor() - 20 <= invader_rocket.xcor() <= self.plane.xcor() + 20 and \
                    self.plane.ycor() - 5 <= invader_rocket.ycor() <= self.plane.ycor() + 5:
                print('You Lose!')
                self.new_game()
        for rocket in self.bullets:
            rocket.goto(rocket.xcor(), rocket.ycor() + 5)
            for ship in self.invaders_ships:
                if ship.xcor() - 10 <= rocket.xcor() <= ship.xcor() + 10 and \
                        ship.ycor() - 10 <= rocket.ycor() <= ship.ycor() + 10:
                    self.invaders_ships.remove(ship)
                    self.bullets.remove(rocket)
                    rocket.hideturtle()
                    ship.hideturtle()
                    self.scoreboard.increase_score()
        self.count += 1
        self.count_heights += 1
        self.heights = 0
        if len(self.invaders_ships) == 0:
            self.new_game()
        if self.count_heights == INVADERS_DOWN_SPEED:
            self.heights = -10
            self.count_heights = 0
        if self.count == 50:
            random_number = random.randint(0, len(self.invaders_ships) - 1)
            self.invader_fire(self.invaders_ships[random_number].xcor(), self.invaders_ships[random_number].ycor())
            self.count = 0
        self.window.update()
        time.sleep(0.01)
        self.window.ontimer(self.move)


game = Game()
