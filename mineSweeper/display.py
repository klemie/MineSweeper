
import pygame
from colors import colours
import grid as g
import time


print("(COLS, ROWS, CELL SIZE, # BOMBS)")
print("GameModes: Easy(10, 10, 50, 10), Normal(28, 18, 20, 40), Hard(24, 24, 30, 99)")
print("")
grid = g.Grid(str(input("GameMode:")))


pygame.init()

# Set the width and height of the screen [width, height]
size = (grid.numCols * grid.cell_size, grid.numRows * grid.cell_size)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("MineSweepy")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
startTime = time.time()
# -------- Main Program Loop -----------
while not done:

    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            if grid.flags > 0:
                grid.click_right()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if grid.lose == False:
                grid.click()
    # --- Game logic should go here

    # --- Screen-clearing code goes here

    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.

    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.fill(colours["white"])

    # --- Drawing code should go here
    timer = str(int(time.time() - startTime))
    print(timer)

    grid.draw_grid(screen)

    flag_time = str(grid.flags)

    pygame.display.set_caption(
        "MineSweepy" + " "+"TIME:" + " "+timer + "Flags" + flag_time)
    pygame.display.flip()
    if grid.win(screen):
        time.sleep(9999)

    # --- Go ahead and update the screen with what we've drawn.

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()
