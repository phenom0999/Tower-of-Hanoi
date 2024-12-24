
import pygame
import sys
import time


class hanoi():

    def __init__(self, disksize = 3):

        # Set initial number of disks
        self.n = disksize

        # Solution
        self.solution = []

        # Colors
        self.BACKGROUND = (7, 1, 43)
        self.COMPLIMENT = (80, 90, 26)
        self.BLACK = (0,0,0)
        self.GRAY = (75, 75, 75)
        self.LIGHTGRAY = (150, 150, 150)
        self.LIGHTERGRAY = (200,200,200)
        self.WHITE = (255, 255, 255)
        self.RED = (173, 37, 24)
        self.COLORS = [(27, 154, 127), (154, 27, 54), (118, 154, 27), (64, 27, 154)]

        # Create game
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption('Tower of Hanoi')
        self.size = self.width, self.height = 800, 400
        self.screen = pygame.display.set_mode(self.size,)
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        # Sounds
        self.whoosh_sound = pygame.mixer.Sound('sounds/whoosh.mp3')
        self.click_sound = pygame.mixer.Sound('sounds/click.mp3')

        # Fonts
        OPEN_SANS = "fonts/OpenSans-Regular.ttf"
        self.smallFont = pygame.font.Font(OPEN_SANS, 25)
        self.mediumFont = pygame.font.Font(OPEN_SANS, 28)
        self.mediumlargeFont = pygame.font.Font(OPEN_SANS, 30)
        self.largeFont = pygame.font.Font(OPEN_SANS, 60)
        self.largeFont.set_bold(True)
        self.smallFont.set_bold(True)

        # Images
        self.pause_button = pygame.image.load("images/pause.png").convert_alpha()
        self.play_button = pygame.image.load("images/play.png").convert_alpha()

        # Introduction page
        introduction = True

        # Main page
        main = False

        # Initially play
        self.play = True

        # Initial iteration:
        i = -1


        while True:

            # Check if quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                # Check for mouse click events

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # Check for left click
                    if pygame.mouse.get_pressed()[0]:

                        # Check if intro page is on
                        if introduction == True:

                            # Check for Up Button
                            if (
                                self.up_triangle[1][0] <= mouse_x <= self.up_triangle[2][0] and
                                self.up_triangle[0][1] <= mouse_y <= self.up_triangle[2][1]
                            ):
                                if self.n < 10:
                                    self.n += 1
                                    self.click_sound.play()

                            # Check for Down Button
                            if (
                                self.down_triangle[1][0] <= mouse_x <= self.down_triangle[2][0] and
                                self.down_triangle[0][1] >= mouse_y >= self.down_triangle[2][1]
                            ):
                                if self.n > 1:
                                    self.n -= 1
                                    self.click_sound.play()

                    if main == True:
                        # Check if play/pause button is clicked
                        click, _, _ = pygame.mouse.get_pressed()
                        if click == 1:
                            mouse = pygame.mouse.get_pos()
                            if self.playbuttonrect.collidepoint(mouse):
                                self.click_sound.play()
                                if self.play == True:
                                    self.play = False
                                else:
                                    self.play = True


            self.screen.fill(self.BACKGROUND)


            # Show introduction:
            if introduction:

                # Title
                title = self.largeFont.render(
                    "TOWER OF HANOI", True, self.WHITE)
                titleRect = title.get_rect()
                titleRect.center = ((self.width / 2), (self.height/2) - 130)
                self.screen.blit(title, titleRect)

                # Disk size button
                self.disksize()

                # Solve button
                buttonRect = pygame.Rect(0, 0, self.width/8, 40)
                buttonRect.center = ((self.width / 2), (self.height/2) + 100)
                buttonText = self.smallFont.render("SOLVE", True, self.BACKGROUND)
                buttonTextRect = buttonText.get_rect()
                buttonTextRect.center = buttonRect.center

                # For border 
                buttonRectBorder = pygame.Rect(0, 0, self.width/8 + 4, 40 + 4)
                buttonRectBorder.center = ((self.width / 2), (self.height/2) + 100)

                # Draw button
                pygame.draw.rect(self.screen, self.BLACK, buttonRectBorder, border_radius= 10)
                pygame.draw.rect(self.screen, self.LIGHTERGRAY, buttonRect, border_radius= 10)

                

                self.screen.blit(buttonText, buttonTextRect)

                # Check if solve button is clicked
                click, _, _ = pygame.mouse.get_pressed()
                if click == 1:
                    mouse = pygame.mouse.get_pos()
                    if buttonRect.collidepoint(mouse):
                        self.click_sound.play()
                        introduction = False
                        main = True
                        time.sleep(0.1)

                pygame.display.flip()
                pygame.time.Clock().tick(30)
                continue

            # main page
            if main:
                if i == -1:
                    # Initial disks in tower
                    self.A = list(range(self.n, 0, -1))
                    self.B = [0] * self.n
                    self.C = [0] * self.n

                    # Solve the problem:
                    self.solve(self.n, self.A, self.B, self.C)

                    # No. of steps:
                    self.n_steps = len(self.solution) + 1


                # Draw pause/play button
                self.playpause_button()

                # initially draw
                self.update_steps(i)
                self.draw_towers()

                self.update_disks(i)
                self.draw_disks()
                pygame.display.flip()

                time.sleep(0.8)
                pygame.time.Clock().tick(5)

                # Update iteration
                i = i + 1
                


                # Check if finish
                if i >= len(self.solution):
                    self.__init__(self.n)
                    
            

    def disksize(self):

        # Main Rect
        mainrect = pygame.Rect(0, 0, 135, 43)
        mainrect.center = (self.width/2, self.height/2-10)
        pygame.draw.rect(self.screen, self.BACKGROUND, mainrect)

        # Disk Rect
        diskrect = pygame.Rect(0, 0, mainrect.width*0.72, 43)
        diskrect.top = mainrect.top
        diskrect.left = mainrect.left
        disktext = self.mediumlargeFont.render("Disks", True, self.WHITE)
        disktextRect = disktext.get_rect()
        disktextRect.center = diskrect.center
        pygame.draw.rect(self.screen, self.COMPLIMENT, diskrect, border_radius= 7)
        self.screen.blit(disktext, disktextRect)

        # Disk size Rect
        blankrect = pygame.Rect(0, 0, mainrect.width*0.23, 43)
        blankrect.top = mainrect.top
        blankrect.right = mainrect.right
        sizetext = self.mediumFont.render(str(self.n), True, self.COMPLIMENT)
        sizetextRect = sizetext.get_rect()
        sizetextRect.center = blankrect.center
        pygame.draw.rect(self.screen, self.WHITE, blankrect, border_radius=7)
        self.screen.blit(sizetext, sizetextRect)

        # Draw size change buttons (Triangles)
        self.draw_size_change_buttons(blankrect)

    def draw_size_change_buttons(self, reference):

        triangle_width = 8
        triangle_height = 14

        # Triangle coordinates
        triangle1_x, triangle1_y = (
            reference.centerx), (reference.centery - 39)
        triangle2_x, triangle2_y = (
            reference.centerx), (reference.centery + 39)

        # Up triangle vertices
        self.up_triangle = [
            (triangle1_x, triangle1_y),
            ((triangle1_x - triangle_width),
             (triangle1_y + triangle_height)),
            ((triangle1_x + triangle_width),
             (triangle1_y + triangle_height))
        ]

        # Down triangle vertices
        self.down_triangle = [
            (triangle2_x, triangle2_y),
            ((triangle2_x - triangle_width),
             (triangle2_y - triangle_height)),
            ((triangle2_x + triangle_width),
             (triangle2_y - triangle_height))
        ]

        # Draw buttons
        pygame.draw.polygon(self.screen, self.LIGHTERGRAY, self.up_triangle)
        pygame.draw.polygon(self.screen, self.LIGHTERGRAY, self.down_triangle)

    def solve(self, n, source, aux, destination):

        if n == 1:
            self.solution.append((source, destination))
            return
        else:

            self.solve(n-1, source, destination, aux)
            self.solution.append((source, destination))
            self.solve(n-1, aux, source, destination)
            return


    def draw_towers(self):

        # Draw towers
        land = pygame.Rect(0, (self.height * 9/10),
                           self.width, (self.height * 1/6))
        pygame.draw.rect(self.screen, self.COMPLIMENT, land)
        self.towerHeight = (5/8 * self.height)
        self.towerWidth = (self.width * 1/50)
        self.rightspace = (self.width * ( 1 - 3/25)/6 + self.width * 1/50)
        pygame.draw.rect(self.screen, self.LIGHTGRAY, (self.rightspace,
                         (self.height * 11/40), self.towerWidth, self.towerHeight),border_top_left_radius=7, border_top_right_radius= 7)
        pygame.draw.rect(self.screen, self.LIGHTGRAY, (self.width/2,
                         (self.height * 11/40), self.towerWidth, self.towerHeight),border_top_left_radius=7, border_top_right_radius= 7)
        pygame.draw.rect(self.screen, self.LIGHTGRAY, (self.width - self.rightspace,
                         (self.height * 11/40), self.towerWidth, self.towerHeight),border_top_left_radius=7, border_top_right_radius= 7)



    def draw_disks(self):

        i = 1
        for disk in self.A:
            if disk != 0:
                DISKCOLOR = self.COLORS[disk%4]
                diskWidth = self.width * 3/50 + (7/300 * (disk-1) * self.width)
                diskHeight = (self.towerHeight - 20)/ 10
                pygame.draw.rect(self.screen,
                                 DISKCOLOR,
                                 ((self.rightspace + self.width/100) - diskWidth/2,
                                  (self.height * 9/10) - i * diskHeight,
                                  diskWidth,
                                  diskHeight), 
                                  border_radius=10)
                i += 1

        i = 1
        for disk in self.B:
            if disk != 0:
                DISKCOLOR = self.COLORS[disk%4]
                diskWidth = self.width * 3/50 + (7/300 * (disk-1) * self.width)
                diskHeight = (self.towerHeight - 20)/ 10
                pygame.draw.rect(self.screen,
                                 DISKCOLOR,
                                 ((self.width/2 + self.width/100) - diskWidth/2,
                                  (self.height * 9/10) - i * diskHeight,
                                  diskWidth,
                                  diskHeight),
                                  border_radius=10)
                i += 1

        i = 1
        for disk in self.C:
            if disk != 0:
                DISKCOLOR = self.COLORS[disk%4]
                diskWidth = self.width * 3/50 + (7/300 * (disk-1) * self.width)
                diskHeight = (self.towerHeight - 20)/ 10
                pygame.draw.rect(self.screen,
                                 DISKCOLOR,
                                 ((self.width - self.rightspace + self.width/100) - diskWidth/2,
                                  (self.height * 9/10) - i * diskHeight,
                                  diskWidth,
                                  diskHeight), 
                                  border_radius=10)
                i += 1
    



    def update_disks(self, iteration):

        if iteration == -1:
            return

        source, destination = self.solution[iteration]

        # Update the arrays of towers:
        self.whoosh_sound.play()
        self.push(destination, self.pop(source))


    def playpause_button(self):

        self.playbuttonrect = pygame.Rect(0, 0, 48, 48)
        self.playbuttonrect.left = self.width * 1/15
        self.playbuttonrect.top = self.height * 1/15

        self.play_button = pygame.transform.scale(self.play_button, (48,48))
        self.pause_button = pygame.transform.scale(self.pause_button, (48,48))

        if self.play == True:
            self.screen.blit(self.pause_button, self.playbuttonrect)
        else:
            self.screen.blit(self.play_button, self.playbuttonrect)
        

                
        
    
    def update_steps(self, iteration):
        
        n_stepStr = str(iteration + 2)
        totalstepStr = str(self.n_steps)

        stepStr = n_stepStr + "/" + totalstepStr

        # Main Rect
        count = len(stepStr)
        
        mainrect_width = (count-2) * 20 + 120

        mainrect = pygame.Rect(0, 0, mainrect_width, 40)
        mainrect.right = self.width * 14/15
        mainrect.top = self.height * 1/15
        pygame.draw.rect(self.screen, self.BACKGROUND, mainrect)

        # Disk Rect
        steprect = pygame.Rect(0, 0, mainrect.width*0.75, 40)
        steprect.top = mainrect.top
        steprect.left = mainrect.left
        disktext = self.mediumFont.render("Steps:", True, self.LIGHTERGRAY)
        disktextRect = disktext.get_rect()
        disktextRect.center = steprect.center
        pygame.draw.rect(self.screen, self.BACKGROUND, steprect)
        self.screen.blit(disktext, disktextRect)

        # Disk size Rect
        blankrect = pygame.Rect(0, 0, mainrect.width*0.25, 40)
        blankrect.top = mainrect.top
        blankrect.right = mainrect.right
        sizetext = self.mediumFont.render(stepStr, True, self.WHITE)
        sizetextRect = sizetext.get_rect()
        sizetextRect.center = blankrect.center
        pygame.draw.rect(self.screen, self.BACKGROUND, blankrect)
        self.screen.blit(sizetext, sizetextRect)



    def printall(self, A, B, C):
        print()
        print(A)
        print(B)
        print(C)

    def pop(self, arr):
        i = 1
        while (arr[len(arr)-i] == 0):
            i = i + 1

        num = arr[len(arr) - i]
        arr[len(arr)-i] = 0
        return num

    def push(self, arr, num):
        i = 0
        while (arr[i] != 0):
            i = i + 1

        arr[i] = num
        return  

hanoi()
