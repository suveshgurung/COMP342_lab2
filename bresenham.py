import glfw
from OpenGL.GL import *

def bresenham_line(x1, y1, x2, y2):
    points = []
    
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    
    x_step = 1 if x2 > x1 else -1
    y_step = 1 if y2 > y1 else -1
    
    x, y = x1, y1
    
    # Case 1: |m| < 1
    if dx > dy:
        p = 2 * dy - dx  # Initial decision parameter
        
        for _ in range(dx + 1):
            points.append((x, y))
            
            if p >= 0:
                y += y_step
                p += 2 * (dy - dx)
            else:
                p += 2 * dy
            
            x += x_step
    
    # Case 2: |m| >= 1
    else:
        p = 2 * dx - dy  # Initial decision parameter
        
        for _ in range(dy + 1):
            points.append((x, y))
            
            if p >= 0:
                x += x_step
                p += 2 * (dx - dy)
            else:
                p += 2 * dx
            
            y += y_step
    
    return points

def draw_line_points(points, color=(1.0, 1.0, 1.0)):
    glColor3f(*color)
    glBegin(GL_POINTS)
    for x, y in points:
        glVertex2f(x, y)
    glEnd()

def main():
    if not glfw.init():
        return
    
    width, height = 800, 600
    window = glfw.create_window(width, height, "Bresenham Line Drawing Algorithm", None, None)
    
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
    
    glPointSize(3.0)
    
    lines = [
        #Gentle slopes (|m| < 1) - Red
        ((100, 300, 400, 350), (1.0, 0.0, 0.0)),
        ((100, 200, 400, 150), (1.0, 0.0, 0.0)),
        ((450, 300, 750, 300), (1.0, 0.0, 0.0)),
        
        # Steep slopes (|m| >= 1) - Green
        ((200, 100, 250, 500), (0.0, 1.0, 0.0)),
        ((350, 500, 400, 100), (0.0, 1.0, 0.0)),
        ((600, 100, 600, 500), (0.0, 1.0, 0.0)),
        
        # 45-degree lines (|m| = 1) - Blue
        ((100, 100, 300, 300), (0.0, 0.0, 1.0)),
        ((500, 100, 700, 300), (0.0, 0.0, 1.0)),
        
        # Mixed slopes - Yellow
        ((50, 450, 350, 100), (1.0, 1.0, 0.0)), 
        ((450, 450, 750, 150), (1.0, 1.0, 0.0)),
    ]
    
    all_line_data = []
    for (x1, y1, x2, y2), color in lines:
        points = bresenham_line(x1, y1, x2, y2)
        all_line_data.append((points, color))
        
        # Print info about the line
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        slope_type = "|m| < 1" if dx > dy else ("|m| >= 1" if dx < dy else "|m| = 1")
        print(f"Line ({x1},{y1}) to ({x2},{y2}): dx={dx}, dy={dy}, {slope_type}, points={len(points)}")
    
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
        glClearColor(0.1, 0.1, 0.1, 1.0)
        
        for points, color in all_line_data:
            draw_line_points(points, color)
        
        glfw.swap_buffers(window)
        glfw.poll_events()
    
    glfw.terminate()

if __name__ == "__main__":
    main()
