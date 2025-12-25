import glfw
from OpenGL.GL import *

def plot_circle_points(xc, yc, x, y, points):
    points.extend([
        (xc + x, yc + y),  # Octant 1
        (xc - x, yc + y),  # Octant 4
        (xc + x, yc - y),  # Octant 8
        (xc - x, yc - y),  # Octant 5
        (xc + y, yc + x),  # Octant 2
        (xc - y, yc + x),  # Octant 3
        (xc + y, yc - x),  # Octant 7
        (xc - y, yc - x),  # Octant 6
    ])

def midpoint_circle(xc, yc, r):
    points = []
    
    x = 0
    y = r
    
    p = 1 - r
    
    plot_circle_points(xc, yc, x, y, points)
    
    # Iterate until x >= y
    while x < y:
        x += 1
        
        if p < 0:
            # Mid-point is inside the circle
            p += 2 * x + 1
        else:
            # Mid-point is outside the circle
            y -= 1
            p += 2 * (x - y) + 1
        
        # Plot points in all 8 octants
        plot_circle_points(xc, yc, x, y, points)
    
    return points

def draw_points(points, color=(1.0, 1.0, 1.0)):
    glColor3f(*color)
    glBegin(GL_POINTS)
    for x, y in points:
        glVertex2f(x, y)
    glEnd()

def draw_filled_circle(xc, yc, r, color=(1.0, 1.0, 1.0)):
    """
    Optional: Draw a filled circle using the mid-point algorithm
    by drawing horizontal lines between symmetric points
    """
    glColor4f(*color, 0.3)  # Semi-transparent fill
    
    x = 0
    y = r
    p = 1 - r
    
    glBegin(GL_LINES)
    for i in range(-r, r + 1):
        glVertex2f(xc - r, yc + i)
        glVertex2f(xc + r, yc + i)
    glEnd()

def main():
    if not glfw.init():
        return
    
    width, height = 800, 600
    window = glfw.create_window(width, height, "Mid-Point Circle Drawing Algorithm", None, None)
    
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
    
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    glPointSize(2.0)
    
    # Define circles to draw
    circles = [
        # (center_x, center_y, radius, color)
        (200, 150, 80, (1.0, 0.0, 0.0)),    # Red circle
        (400, 300, 120, (0.0, 1.0, 0.0)),   # Green circle (center)
        (600, 150, 60, (0.0, 0.0, 1.0)),    # Blue circle
        (200, 450, 100, (1.0, 1.0, 0.0)),   # Yellow circle
        (600, 450, 90, (1.0, 0.0, 1.0)),    # Magenta circle
        (400, 150, 40, (0.0, 1.0, 1.0)),    # Cyan circle (small)
    ]
    
    # Calculate all circle points using mid-point algorithm
    all_circle_data = []
    for xc, yc, r, color in circles:
        points = midpoint_circle(xc, yc, r)
        all_circle_data.append((points, color))
        
        print(f"Circle at ({xc},{yc}) with radius {r}: {len(points)} points generated")
    
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
        glClearColor(0.05, 0.05, 0.05, 1.0)
        
        for points, color in all_circle_data:
            draw_points(points, color)
        
        glfw.swap_buffers(window)
        glfw.poll_events()
    
    glfw.terminate()

if __name__ == "__main__":
    main()
