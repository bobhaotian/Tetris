import pygame
import random
shapes = [
    [[1, 5, 9, 13], [4, 5, 6, 7]],
    [[4, 5, 9, 10], [2, 6, 5, 9]],
    [[6, 7, 9, 10], [1, 5, 6, 10]],
    [[2, 1, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
    [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
    [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
    [[1, 2, 5, 6]],
    ]

#colors of blocks
shapeColors = [(0, 0, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

width = 700
height = 600
game_height = 400
game_width = 100
blockSize = 20
topLeft_x = (width - game_width) // 2
topLeft_y = height - game_height - 55

class Blocks:
    x = 0
    y = 0
    def __init__(self, x, y,shape):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(shapes) - 1)
        self.color = random.randint(1, len(shapeColors) - 1)
        self.rotation = 0
    def image(self):
        return shapes[self.type][self.rotation]
    def rotate(self):
        self.rotation = (self.rotation + 1) % len(shapes[self.type])

class Tetris:
    speed = 1
    score = 0
    state = "start"
    field = []
    height = 0
    width = 0
    zoom = 25
    x = 100
    y = 70
    block = None
    nextblock=None
    
    #setting of board

    def __init__(self, height, width):
        self.height = height
        self.width = width
        for i in range(height):
            new = []
            for j in range(width):
                new.append(0)
            self.field.append(new)

    #Creates new blocks
    def new_block(self):
        self.block = Blocks(3, 0,random.randint(0, len(shapes) - 1))
    #randomly create blocks
    def next_block(self):
        self.nextblock=Blocks(3, 0, random.randint(0, len(shapes) - 1))

    #Checks if the blocks touch the top of the board
    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.block.image():
                    if i + self.block.y > self.height-1 or \
                            j + self.block.x > self.width - 1 or \
                            j + self.block.x < 0 or \
                            self.field[i + self.block.y][j + self.block.x] > 0:
                        intersection = True
        return intersection

    #break the formed lines
    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            count = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    count += 1
            if count == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2

    def draw_next_block(self,screen):

        font = pygame.font.SysFont("comicsans", 25)
        label = font.render("Next Shape", True, (255,128,128))
        screen.blit(label,(topLeft_x+27+game_width/1-(label.get_width()/90),213))
        sx = topLeft_x + game_width + 50
        sy = topLeft_y + game_height/2 - 90
        pygame.draw.rect(screen, (255,205,10), (92, 65, 265, 33), 30)
        for i in range(4):
                for j in range(4):
                    p = j+i * 4
                    if p in self.nextblock.image():
                        pygame.draw.rect(screen, shapeColors[self.nextblock.color],(sx + j*25, sy + i*25, 25, 25), 3)
        pygame.display.update()
    #force the block immediately going to the bottom
    def movebottom(self):
        while self.intersects()==False:
            self.block.y += 1
        self.block.y -= 1
        self.stop()

    #Down one unit
    def moveDown(self):
        self.block.y += 1
        if self.intersects()==True:
            self.block.y -= 1
            self.stop()

    # This function runs once the block reaches the bottom. 
    def stop(self):
        for i in range(4):
            for j in range(4):
                z = i*4 + j
                if z in self.block.image():
                    self.field[i + self.block.y][j + self.block.x] = self.block.color
        self.break_lines()
        self.new_block()
        self.block=self.nextblock
        self.next_block()
        if self.intersects():
            self.state = "gameover"
    #This function moves the block horizontally
    def moveHoriz(self, dx):
        old_x = self.block.x
        self.block.x += dx
        if self.intersects():
            self.block.x = old_x

    #This function rotates the block 
    def rotate(self):
        old_rotation = self.block.rotation
        self.block.rotate()
        if self.intersects():
            self.block.rotation = old_rotation

pygame.font.init()

def startGame():
    done = False
    clock = pygame.time.Clock()
    fps = 25
    game = Tetris(20, 10)
    counter = 0

    pressing_down = False
    
    while not done:
        #Create a new block if there is no moving block
        if game.block is None:
            game.new_block()
        if game.nextblock is None:
            game.next_block()
        counter += 1 #Keeping track if the time 
        if counter > 100000:
            counter = 0

        #Moving the block continuously with time or when down key is pressed
        if counter % (fps // game.speed // 2) == 0 or pressing_down:
            if game.state == "start":
                game.moveDown()
        #Checking which key is pressed and running corresponding function
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.rotate()
                if event.key == pygame.K_DOWN:
                    game.moveDown()
                if event.key == pygame.K_LEFT:
                    game.moveHoriz(-1)
                if event.key == pygame.K_RIGHT:
                    game.moveHoriz(1)
                if event.key == pygame.K_SPACE:
                    game.movebottom()
                if event.key == pygame.K_ESCAPE:
                    game.__init__(20, 10)

        screen.fill('#FFFFFF')

        #Updating the game board regularly
        for i in range(game.height):
            for j in range(game.width):
                pygame.draw.rect(screen, '#B2BEB5', [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
                if game.field[i][j] > 0:
                    pygame.draw.rect(screen, shapeColors[game.field[i][j]],
                                     [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

        #Updating the board with the moving block
        if game.block is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in game.block.image():
                        pygame.draw.rect(screen, shapeColors[game.block.color],
                                         [game.x + game.zoom * (j + game.block.x) + 1,
                                          game.y + game.zoom * (i + game.block.y) + 1,
                                          game.zoom - 2, game.zoom - 2])

        #Showing the score
        font = pygame.font.SysFont('Comicsans', 40, True, False)
        font1 = pygame.font.SysFont('Comicsans', 25, True, False)
        text = font.render("Score: " + str(game.score), True, '#000000')
        text_game_over = font.render("Game Over", True, '#000000')
        text_game_over1 = font.render("Press ESC", True, '#000000')

        #Ending the game if state is gameover
        screen.blit(text, [300, 0])
        if game.state == "gameover":
            screen.blit(text_game_over, [300, 200])
            screen.blit(text_game_over1, [300, 265])
       
        game.draw_next_block(screen)

        pygame.display.flip()
        clock.tick(fps)


screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tetris by DataFlair")
run = True
while run:
    screen.fill((16, 57, 44 ))
    font = pygame.font.SysFont("Comicsans", 60, bold=True)
    label = font.render("Press any key to begin!", True, '#FFFFFF')

    screen.blit(label, (10, 300 ))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            startGame()
pygame.quit()

