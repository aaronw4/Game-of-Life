import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def random_grid(N):
    return np.random.choice([1, 0], N*N, p=[0.2, 0.8]).reshape(N, N)
 
def add_circle(i, j, grid):
    circle = np.array([
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ])
    grid[i, j] = circle

def update(frame_number, img, grid, N):
    new_grid = grid.copy()
    for i in range(N):
        for j in range(N):
            total = int(
                grid[i, (j-1)%N] + grid[i, (j+1)%N] + grid[(i-1)%N, j] 
                + grid[(i+1)%N, j] + grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] 
                + grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N]
            )
            if grid[i, j] == 1:
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
    parser.add_argument('--mov-file', dest='movfile', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
    parser.add_argument('--circle', action='store_true', required=False)
    parser.add_argument('--gosper', action='store_true', required=False)
    args = parser.parse_args()

    N = 25

    update_interval = 50
    if args.interval:
        update_interval = int(args.interval)

    grid = np.array([])
    if args.circle:
        grid = np.zeros(N*N).reshape(N, N)
        add_circle(12, 12, grid)
    else:
        grid = random_grid(N)

    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(
        fig, 
        update, 
        fargs=(img, grid, N, ),
        frames=10, 
        interval=update_interval, 
        save_count=50
    )

if __name__ == '__main__':
    execute()
