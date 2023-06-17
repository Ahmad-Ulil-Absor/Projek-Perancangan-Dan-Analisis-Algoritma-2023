import pygame
import random
import time

# Dimensi labirin
MAZE_WIDTH = 450
MAZE_HEIGHT = 450

# Dimensi droid dan tombol
DROID_SIZE = 30
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 40

# Warna
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Kecepatan gerakan droid (dalam detik)
MOVE_DELAY = 0.3

# Inisialisasi pygame
pygame.init()
screen = pygame.display.set_mode((MAZE_WIDTH + BUTTON_WIDTH + 40, MAZE_HEIGHT))
pygame.display.set_caption("Ahmad Ulil Absor 2101020031 (Seek And Hide)")

# Matriks labirin
maze = [[1 for _ in range(15)] for _ in range(15)]

# Inisialisasi droid merah dan droid hijau
red_droid_x = [0]
red_droid_y = [0]
green_droid_x = 14
green_droid_y = 14

# Inisialisasi tombol
button_x = MAZE_WIDTH + 20
shuffle_button_y = 20
start_button_y = 70
stop_button_y = 120
add_red_button_y = 170
remove_red_button_y = 220
random_red_button_y = 270
random_green_button_y = 320
view_green_button_y = 370

# Status permainan
game_started = False

# Mengacak labirin
def shuffle_maze():
    global maze
    maze = [[1 for _ in range(15)] for _ in range(15)]

    stack = [(0, 0)]
    while stack:
        x, y = stack[-1]
        maze[x][y] = 0

        neighbors = []
        if x > 1 and maze[x - 2][y] == 1:
            neighbors.append((x - 2, y))
        if x < 13 and maze[x + 2][y] == 1:
            neighbors.append((x + 2, y))
        if y > 1 and maze[x][y - 2] == 1:
            neighbors.append((x, y - 2))
        if y < 13 and maze[x][y + 2] == 1:
            neighbors.append((x, y + 2))

        if neighbors:
            nx, ny = random.choice(neighbors)
            maze[(x + nx) // 2][(y + ny) // 2] = 0
            stack.append((nx, ny))
        else:
            stack.pop()

# Menggambar labirin
def draw_maze():
    for i in range(15):
        for j in range(15):
            color = WHITE if maze[i][j] == 0 else BLACK
            pygame.draw.rect(screen, color, (j * DROID_SIZE, i * DROID_SIZE, DROID_SIZE, DROID_SIZE))

# Menggambar droid merah
def draw_red_droid():
    for i in range(len(red_droid_x)):
        pygame.draw.rect(screen, RED, (red_droid_y[i] * DROID_SIZE, red_droid_x[i] * DROID_SIZE, DROID_SIZE, DROID_SIZE))

# Menggambar droid hijau
def draw_green_droid():
    pygame.draw.rect(screen, GREEN, (green_droid_y * DROID_SIZE, green_droid_x * DROID_SIZE, DROID_SIZE, DROID_SIZE))

# Menggambar tombol
def draw_buttons():
    font = pygame.font.Font(None, 24)

    shuffle_text = font.render("RPeta", True, BLACK)
    start_text = font.render("Start", True, BLACK)
    stop_text = font.render("Stop", True, BLACK)
    add_red_text = font.render("AddRed", True, BLACK)
    remove_red_text = font.render("RMVRed", True, BLACK)
    random_red_text = font.render("RRed", True, BLACK)
    random_green_text = font.render("RGreen", True, BLACK)
    view_green_text = font.render("ViewGreen", True, BLACK)
    
    pygame.draw.rect(screen, WHITE, (button_x, shuffle_button_y, BUTTON_WIDTH, BUTTON_HEIGHT))
    pygame.draw.rect(screen, WHITE, (button_x, start_button_y, BUTTON_WIDTH, BUTTON_HEIGHT))
    pygame.draw.rect(screen, WHITE, (button_x, stop_button_y, BUTTON_WIDTH, BUTTON_HEIGHT))
    pygame.draw.rect(screen, WHITE, (button_x, add_red_button_y, BUTTON_WIDTH, BUTTON_HEIGHT))
    pygame.draw.rect(screen, WHITE, (button_x, remove_red_button_y, BUTTON_WIDTH, BUTTON_HEIGHT))
    pygame.draw.rect(screen, WHITE, (button_x, random_red_button_y, BUTTON_WIDTH, BUTTON_HEIGHT))
    pygame.draw.rect(screen, WHITE, (button_x, random_green_button_y, BUTTON_WIDTH, BUTTON_HEIGHT))
    pygame.draw.rect(screen, WHITE, (button_x, view_green_button_y, BUTTON_WIDTH, BUTTON_HEIGHT))

    screen.blit(shuffle_text, (button_x + 10, shuffle_button_y + 10))
    screen.blit(start_text, (button_x + 10, start_button_y + 10))
    screen.blit(stop_text, (button_x + 10, stop_button_y + 10))
    screen.blit(add_red_text, (button_x + 10, add_red_button_y + 10))
    screen.blit(remove_red_text, (button_x + 10, remove_red_button_y + 10))
    screen.blit(random_red_text, (button_x + 10, random_red_button_y + 10))
    screen.blit(random_green_text, (button_x + 10, random_green_button_y + 10))
    screen.blit(view_green_text, (button_x + 10, view_green_button_y + 10))

# Mengecek apakah dua droid bertemu
def check_collision():
    for i in range(len(red_droid_x)):
        if red_droid_x[i] == green_droid_x and red_droid_y[i] == green_droid_y:
            return True
    return False

# Loop utama permainan
def game_loop():
    global game_started
    running = True
    shuffle_maze()

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if button_x <= mouse_x <= button_x + BUTTON_WIDTH:
                    if shuffle_button_y <= mouse_y <= shuffle_button_y + BUTTON_HEIGHT:
                        shuffle_maze()
                    elif start_button_y <= mouse_y <= start_button_y + BUTTON_HEIGHT and not game_started:
                        game_started = True
                    elif stop_button_y <= mouse_y <= stop_button_y + BUTTON_HEIGHT and game_started:
                        game_started = False
                    elif random_red_button_y <= mouse_y <= random_red_button_y + BUTTON_HEIGHT:
                        random_red_droid()
                    elif random_green_button_y <= mouse_y <= random_green_button_y + BUTTON_HEIGHT:
                        random_green_droid()
                    elif add_red_button_y <= mouse_y <= add_red_button_y + BUTTON_HEIGHT:
                        add_red_droid()
                    elif remove_red_button_y <= mouse_y <= remove_red_button_y + BUTTON_HEIGHT:
                        remove_red_droid()
                    elif view_green_button_y <= mouse_y <= view_green_button_y + BUTTON_HEIGHT:
                        view_green_droid()            

        draw_maze()
        if game_started:
            red_move()
            green_move()
        draw_red_droid()
        draw_green_droid()
        draw_buttons()

        if check_collision():
            font = pygame.font.Font(None, 45)
            text = font.render("Game Over", True, RED)
            screen.blit(text, (MAZE_WIDTH // 2 - 80, MAZE_HEIGHT // 2 - 18))
            game_started = False
            

        pygame.display.update()

        # Menambahkan delay agar gerakan lebih terlihat
        pygame.time.delay(150)

    pygame.quit()

# Gerakan droid merah (pencari)
def red_move():
    global red_droid_x, red_droid_y
    if not check_collision():
        for i in range(len(red_droid_x)):
            if red_droid_x[i] < green_droid_x and maze[red_droid_x[i] + 1][red_droid_y[i]] == 0:
                red_droid_x[i] += 1
            elif red_droid_x[i] > green_droid_x and maze[red_droid_x[i] - 1][red_droid_y[i]] == 0:
                red_droid_x[i] -= 1
            elif red_droid_y[i] < green_droid_y and maze[red_droid_x[i]][red_droid_y[i] + 1] == 0:
                red_droid_y[i] += 1
            elif red_droid_y[i] > green_droid_y and maze[red_droid_x[i]][red_droid_y[i] - 1] == 0:
                red_droid_y[i] -= 1

# Gerakan droid hijau (penghindar)
def green_move():
    global green_droid_x, green_droid_y

    if not check_collision():
        directions = []

        if green_droid_x > 0 and maze[green_droid_x - 1][green_droid_y] == 0:
            directions.append("UP")
        if green_droid_x < 14 and maze[green_droid_x + 1][green_droid_y] == 0:
            directions.append("DOWN")
        if green_droid_y > 0 and maze[green_droid_x][green_droid_y - 1] == 0:
            directions.append("LEFT")
        if green_droid_y < 14 and maze[green_droid_x][green_droid_y + 1] == 0:
            directions.append("RIGHT")

        if directions:
            direction = random.choice(directions)

            if direction == "UP":
                green_droid_x -= 1
            elif direction == "DOWN":
                green_droid_x += 1
            elif direction == "LEFT":
                green_droid_y -= 1
            elif direction == "RIGHT":
                green_droid_y += 1
                
# Menghentikan gerakan droid
def stop_move():
    pass

# Droid merah posisi acak
def random_red_droid():
    global red_droid_x, red_droid_y
    if maze[red_droid_x[0]][red_droid_y[0]] == 0:
        while True:
            x = random.randint(0, 14)
            y = random.randint(0, 14)
            if maze[x][y] == 0 and (x != red_droid_x[0] or y != red_droid_y[0]):
                red_droid_x[0] = x
                red_droid_y[0] = y
                break

# Droid hijau posisi acak
def random_green_droid():
    global green_droid_x, green_droid_y
    if maze[green_droid_x][green_droid_y] == 0:
        while True:
            x = random.randint(0, 14)
            y = random.randint(0, 14)
            if maze[x][y] == 0 and (x != green_droid_x or y != green_droid_y):
                green_droid_x = x
                green_droid_y = y
                break

# Menambahkan droid merah
def add_red_droid():
    global red_droid_x, red_droid_y
    if maze[red_droid_x[0]][red_droid_y[0]] == 0:
        while True:
            x = random.randint(0, 14)
            y = random.randint(0, 14)
            if maze[x][y] == 0 and (x != green_droid_x or y != green_droid_y):
                red_droid_x.append(x)
                red_droid_y.append(y)
                break

# Menghapus droid merah 
def remove_red_droid():
    if len(red_droid_x) > 1:
        red_droid_x.pop()
        red_droid_y.pop()

# Pandangan droid hijau
def view_green_droid():
    global maze
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == 1:
                maze[i][j] = 0
                
# Memulai permainan
game_loop()