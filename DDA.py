import glfw
from OpenGL.GL import *

def dda_line(x1, y1, x2, y2):
    points = []
    
    dx = x2 - x1
    dy = y2 - y1
    
    # Determine number of steps
    steps = max(abs(dx), abs(dy))
    
    if steps == 0:
        return [(x1, y1)]
    
    # Calculate increment for each step
    x_inc = dx / steps
    y_inc = dy / steps
    
    # Starting point
    x, y = x1, y1
    
    for _ in range(int(steps) + 1):
        points.append((round(x), round(y)))
        x += x_inc
        y += y_inc
    
    return points

def draw_line_points(points):
    glBegin(GL_POINTS)
    for x, y in points:
        glVertex2f(x, y)
    glEnd()

def main():
    if not glfw.init():
        return
    
    width, height = 800, 600
    window = glfw.create_window(width, height, "DDA Line Drawing Algorithm", None, None)
    
    if not window:
        glfw.terminate()
        return
    
    glfw.make_context_current(window)
    
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, height, 0, -1, 1)  # 2D orthographic projection
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    glPointSize(2.0)
    
    lines = [
        (100, 100, 700, 500),  # Diagonal line
        (400, 50, 400, 550),   # Vertical line
        (50, 300, 750, 300),   # Horizontal line
        (200, 150, 600, 450),  # Another diagonal
        (150, 500, 650, 100),  # Diagonal with negative slope
    ]
    
    all_points = []
    for x1, y1, x2, y2 in lines:
        points = dda_line(x1, y1, x2, y2)
        all_points.extend(points)
    
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        
        glColor3f(1.0, 1.0, 1.0)
        
        draw_line_points(all_points)
        
        glfw.swap_buffers(window)
        glfw.poll_events()
    
    glfw.terminate()

if __name__ == "__main__":
    main()
