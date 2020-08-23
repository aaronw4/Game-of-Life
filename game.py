import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def random_grid(N):
    return np.random.choice([1, 0], N*N, p=[0.2, 0.8]).reshape(N, N)
    #Creates random grid of NxN with a 20% chance of 1 and 80% chance of 0
 
def add_circle(i, j, grid):
    # 1 is alive and 0 is dead
    circle = np.array([
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ])
    grid[i:i+3, j:j+3] = circle
    #Creates a 3 x 3 grid sets that to cirlce

def add_pulsar(i, j, grid):
    pulsar = np.array([
        [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
        [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
        [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0]
    ])
    grid[i:i+13, j:j+13] = pulsar

def add_double_circle(i, j, grid):
    double_circle = np.array([
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [0, 1, 1, 1, 0]
    ])
    grid[i:i+12, j:j+5] = double_circle

def update(frame_number, img, grid, N):
    #frame_number is passed in by animation
    new_grid = grid.copy()
    for i in range(N):
        for j in range(N):
            total = int(
                grid[i, (j-1)%N] + grid[i, (j+1)%N] + grid[(i-1)%N, j] 
                + grid[(i+1)%N, j] + grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] 
                + grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N]
            ) #adds up all the numbers in neighbooring cells
            if grid[i, j] == 1:
            #Rules of the game
                if (total < 2):
                    new_grid[i, j] = 0
                elif total > 3:
                    new_grid[i, j] = 0
            else:
                if total == 3:
                    new_grid[i, j] = 1

    img.set_data(new_grid)
    grid[:] = new_grid[:]
    return img

def execute():
    parser = argparse.ArgumentParser(description="Conway's Game of Life")
    #Commands that are entered in the terminal
    parser.add_argument('--mov-file', dest='movfile', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
    parser.add_argument('--pulsar', action='store_true', required=False)
    parser.add_argument('--double_circle', action='store_true', required=False)
    args = parser.parse_args()

    #Grid size is 25 x 25
    N = 25

    update_interval = 500
    if args.interval:
        update_interval = int(args.interval)

    grid = np.array([])
    if args.pulsar:
        grid = np.zeros(N*N).reshape(N, N)
        add_pulsar(6, 6, grid)
    elif args.double_circle:
        grid = np.zeros(N*N).reshape(N, N)
        add_double_circle(6, 10, grid)
    else:
        grid = random_grid(N)

    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(
        fig, 
        update, 
        fargs=(img, grid, N),
        frames=10, 
        interval=update_interval, 
        save_count=50
    )
    if args.movfile:
        ani.save(args.movefile, fps=30, extra_args=['-vcodec', 'libx264'])

    plt.show()

if __name__ == '__main__':
    execute()
