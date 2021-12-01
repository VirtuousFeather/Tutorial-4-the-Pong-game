import pygame
from bar import Bar
from ball import Ball

class Sceneswitch():
    gameStarted = False
    isMultiplayer = False
    screenWidth = 700
    screenHeight = 500

    # Define some colors
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)

    # Open a new window
    size = (screenWidth, screenHeight)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Pong")

    barA = Bar(BLUE, 10, 100)
    barA.rect.x = 20
    barA.rect.y = 200

    barB = Bar(RED, 10, 100)
    barB.rect.x = 670
    barB.rect.y = 200

    ball = Ball(WHITE, 10, 10)
    ball.rect.x = 345
    ball.rect.y = 195

    # This will be a list that will contain all the sprites we intend to use in our game.
    all_sprites_list = pygame.sprite.Group()

    # Add the car to the list of objects
    all_sprites_list.add(barA)
    all_sprites_list.add(barB)
    all_sprites_list.add(ball)

    # The loop will carry on until the user exit the game (e.g. clicks the close button).
    carryOn = True

    # The clock will be used to control how fast the screen updates
    clock = pygame.time.Clock()

    # Initialise player scores
    scoreA = 0
    scoreB = 0

    def drawHomescreen(self):

            while self.carryOn:
                # --- Main event loop
                for event in pygame.event.get():  # User did something
                    if event.type == pygame.QUIT:  # If user clicked close
                        self.carryOn = False  # Flag that we are done so we exit this loop

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_x:  # Pressing the x Key will quit the game
                            self.carryOn = False

                # Draw black background
                self.screen.fill(self.BLACK)

                # Homescreen texts
                font = pygame.font.Font(None, 70)
                text = font.render("Choose your gamemode", False, self.WHITE)
                self.screen.blit(text, (self.screenWidth / 10, self.screenHeight / 8))

                font = pygame.font.Font(None, 54)
                text = font.render("Singleplayer", False, self.WHITE)
                self.screen.blit(text, (self.screenWidth / 10, self.screenHeight - 200))
                text = font.render("Multiplayer", False, self.WHITE)
                self.screen.blit(text, (self.screenWidth / 2 + 50, self.screenHeight - 200))

                # --- Go ahead and update the screen with what we've drawn.
                pygame.display.flip()

                # --- Limit to 60 frames per second
                self.clock.tick(60)

                for event in pygame.event.get():  # User did something
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = pygame.mouse.get_pos()  # If user clicks a mouse button
                        if mx > self.screenWidth / 10 and mx < self.screenWidth / 2 + 50 and my > self.screenHeight - 200 and my < self.screenHeight - 150:
                            self.isMultiplayer = False
                            self.gameStarted = True
                            self.carryOn = False
                            print("Singleplayer chosen!")
                        elif mx > self.screenWidth / 2 + 50 and mx < self.screenWidth and my > self.screenHeight - 200 and my < self.screenHeight - 150:
                            self.isMultiplayer = True
                            self.gameStarted = True
                            self.carryOn = False
                            print("Multiplayer chosen!")

    def drawGame(self):
            self.carryOn=True
            while self.carryOn:
                # --- Main event loop
                for event in pygame.event.get():  # User did something
                    if event.type == pygame.QUIT:  # If user clicked close
                        self.carryOn = False  # Flag that we are done so we exit this loop
                        break
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_x:  # Pressing the x Key will quit the game
                            self.carryOn = False

                # Moving the paddles when the use uses the arrow keys (player A) or "W/S" keys (player B) (Or in case of Singleplayer no keys for B)
                if self.isMultiplayer:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_w]:
                        self.barA.moveUp(5)
                    if keys[pygame.K_s]:
                        self.barA.moveDown(5)
                    if keys[pygame.K_UP]:
                        self.barB.moveUp(5)
                    if keys[pygame.K_DOWN]:
                        self.barB.moveDown(5)
                if not self.isMultiplayer:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_w]:
                        self.barA.moveUp(5)
                    if keys[pygame.K_s]:
                        self.barA.moveDown(5)

                    # CPU controls
                    if self.ball.rect.y < self.barB.rect.y + 50 and self.scoreA < 3:
                        self.barB.moveUp(4)
                    elif self.ball.rect.y < self.barB.rect.y + 50 and self.scoreA == 3:
                        self.barB.moveUp(5)
                    elif self.ball.rect.y < self.barB.rect.y + 50 and self.scoreA > 3:
                        self.barB.moveUp(6)
                    if self.ball.rect.y > self.barB.rect.y + 50 and self.scoreA < 3:
                        self.barB.moveDown(4)
                    elif self.ball.rect.y > self.barB.rect.y + 50 and self.scoreA == 3:
                        self.barB.moveDown(5)
                    elif self.ball.rect.y > self.barB.rect.y + 50 and self.scoreA > 3:
                        self.barB.moveDown(6)

                    # --- Game logic should go here
                self.all_sprites_list.update()

                # Check if the ball is bouncing against any of the 4 walls:
                if self.ball.rect.x >= 690:
                    self.scoreA += 1
                    self.ball.velocity[0] = -self.ball.velocity[0]
                if self.ball.rect.x <= 0:
                    self.scoreB += 1
                    self.ball.velocity[0] = -self.ball.velocity[0]
                if self.ball.rect.y > 490:
                    self.ball.velocity[1] = -self.ball.velocity[1]
                if self.ball.rect.y < 0:
                    self.ball.velocity[1] = -self.ball.velocity[1]

                    # Detect collisions between the ball and the paddles
                if pygame.sprite.collide_mask(self.ball, self.barA) or pygame.sprite.collide_mask(self.ball, self.barB):
                    self.ball.bounce()

                # --- Drawing code should go here
                # First, clear the screen to black.
                self.screen.fill(self.BLACK)
                # Draw the net
                pygame.draw.line(self.screen, self.WHITE, [349, 0], [349, 500], 5)

                # Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
                self. all_sprites_list.draw(self.screen)

                # Display scores:
                font = pygame.font.Font(None, 74)
                text = font.render("P1 score: " + str(self.scoreA), False, self.BLUE)
                self.screen.blit(text, (0, 10))
                text = font.render("P2 score: " + str(self.scoreB), False, self.RED)
                self.screen.blit(text, (420, 10))

                # --- Go ahead and update the screen with what we've drawn.
                pygame.display.flip()

                # --- Limit to 60 frames per second
                self.clock.tick(60)

    def switchscenes(self):
        if not self.gameStarted:
            self.drawHomescreen()

        if self.gameStarted:
            self.drawGame()