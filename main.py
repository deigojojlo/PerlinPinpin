import random
import math
import matplotlib.pyplot as plt

width, height = 100, 100
scale = 0.05
octaves = 6
persistence = 0.5

random.seed(42)
gradient = [[(random.random() * 2 - 1, random.random() * 2 - 1) for _ in range(width + 1)] for _ in range(height + 1)]

# Normalisation
for i in range(len(gradient)):
    for j in range(len(gradient[0])):
        x, y = gradient[i][j]
        length = math.sqrt(x**2 + y**2)
        gradient[i][j] = (x / length, y / length)

def smooth(x):
    return x**2 * (3 - 2 * x)

def dot_grid_gradient(ix, iy, x, y):
    dx = x - ix
    dy = y - iy
    return dx * gradient[ix][iy][0] + dy * gradient[ix][iy][1]

def perlin(x, y):
    x0, y0 = int(x), int(y)
    x1, y1 = x0 + 1, y0 + 1
    
    if x <= 0 or y <= 0 or x >= width or y >= height : return 0
    
    n0 = dot_grid_gradient(x0, y0, x, y)
    n1 = dot_grid_gradient(x1, y0, x, y)
    ix0 = n0 + smooth(x - x0) * (n1 - n0)

    n0 = dot_grid_gradient(x0, y1, x, y)
    n1 = dot_grid_gradient(x1, y1, x, y)
    ix1 = n0 + smooth(x - x0) * (n1 - n0)

    return ix0 + smooth(y - y0) * (ix1 - ix0)


tab = [[0] * width for _ in range(height)]
for i in range(height):
    for j in range(width):
        # rajoutons des octaves
        amplitude = 1
        max_value = 0
        frequency = scale
        for _ in range(octaves):
            tab[i][j] += amplitude * perlin(i * frequency, j * frequency)
            max_value += amplitude
            amplitude *= persistence
            frequency *= 2
        tab[i][j] /= max_value


plt.imshow(tab, cmap='viridis', origin='lower')
plt.colorbar()
plt.title("Bruit")
plt.show()
