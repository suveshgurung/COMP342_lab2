import glfw
from OpenGL.GL import *
import math

def plot_ellipse_points(xc, yc, x, y, points):
    points.extend([
        (xc + x, yc + y),  # Quadrant 1
        (xc - x, yc + y),  # Quadrant 2
        (xc - x, yc - y),  # Quadrant 3
        (xc + x, yc - y),  # Quadrant 4
    ])

def midpoint_ellipse(xc, yc, rx, ry):
    points = []
    
    # Region 1: Slope < -1
    x = 0
    y = ry
    
    # Initial decision parameters
    rx_sq = rx * rx
    ry_sq = ry * ry
    two_rx_sq = 2 * rx_sq
    two_ry_sq = 2 * ry_sq
    
    # Region 1 decision parameter
    p1 = ry_sq - (rx_sq * ry) + (0.25 * rx_sq)
    
    dx = two_ry_sq * x
    dy = two_rx_sq * y
    
    # Region 1: Continue while slope < -1
    while dx < dy:
        plot_ellipse_points(xc, yc, x, y, points)
        
        x += 1
        dx += two_ry_sq
        
        if p1 < 0:
            p1 += dx + ry_sq
        else:
            y -= 1
            dy -= two_rx_sq
            p1 += dx - dy + ry_sq
    
    # Region 2: Slope >= -1
    # Recalculate decision parameter for region 2
    p2 = ry_sq * (x + 0.5) * (x + 0.5) + rx_sq * (y - 1) * (y - 1) - rx_sq * ry_sq
    
    while y >= 0:
        plot_ellipse_points(xc, yc, x, y, points)
        
        y -= 1
        dy -= two_rx_sq
        
        if p2 > 0:
            p2 += rx_sq - dy
        else:
            x += 1
            dx += two_ry_sq
            p2 += dx - dy + rx_sq
    
    return points

def draw_points(points, color=(1.0, 1.0, 1.0)):
    glColor3f(*color)
    glBegin(GL_POINTS)
    for x, y in points:
        glVertex2f(x, y)
    glEnd()

def draw_axes(xc, yc, rx, ry):
    glColor3f(0.4, 0.4, 0.4)
    glLineWidth(1.0)
    
    glBegin(GL_LINES)
    # Major axis (horizontal)
    glVertex2f(xc - rx - 20, yc)
    glVertex2f(xc + rx + 20, yc)
    
    # Minor axis (vertical)
    glVertex2f(xc, yc - ry - 20)
    glVertex2f(xc, yc + ry + 20)
    glEnd()
    
    # Draw center point
    glColor3f(1.0, 1.0, 0.0)
    glPointSize(6.0)
    glBegin(GL_POINTS)
    glVertex2f(xc, yc)
    glEnd()

def draw_grid(width, height, spacing=50):
    glColor3f(0.15, 0.15, 0.15)
    glLineWidth(1.0)
    
    glBegin(GL_LINES)
    # Vertical lines
    for x in range(0, width, spacing):
        glVertex2f(x, 0)
        glVertex2f(x, height)
    
    # Horizontal lines
    for y in range(0, height, spacing):
        glVertex2f(0, y)
        glVertex2f(width, y)
    glEnd()

def draw_bounding_box(xc, yc, rx, ry):
    glColor3f(0.3, 0.3, 0.5)
    glLineWidth(1.0)
    
    glBegin(GL_LINE_LOOP)
    glVertex2f(xc - rx, yc - ry)
    glVertex2f(xc + rx, yc - ry)
    glVertex2f(xc + rx, yc + ry)
    glVertex2f(xc - rx, yc + ry)
    glEnd()

def main():
    if not glfw.init():
        return
    
    width, height = 1000, 800
    window = glfw.create_window(width, height, "Mid-Point Ellipse Drawing Algorithm", None, None)
    
    if not window:
        glfw.terminate()
        return
    
    glfw.make_context_current(window)
    
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, height, 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_POINT_SMOOTH)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
    
    glPointSize(2.0)
    
    ellipses = [
        # (center_x, center_y, radius_x, radius_y, color, name)
        (250, 200, 150, 100, (1.0, 0.3, 0.3), "Horizontal Ellipse"),
        (650, 200, 100, 150, (0.3, 1.0, 0.3), "Vertical Ellipse"),
        (250, 550, 180, 120, (0.3, 0.5, 1.0), "Wide Ellipse"),
        (650, 550, 120, 80, (1.0, 0.8, 0.2), "Narrow Ellipse"),
        (500, 400, 100, 100, (1.0, 0.4, 0.8), "Circle (rx=ry)"),
    ]
    
    all_ellipse_data = []
    for xc, yc, rx, ry, color, name in ellipses:
        points = midpoint_ellipse(xc, yc, rx, ry)
        all_ellipse_data.append({
            'points': points,
            'center': (xc, yc),
            'radii': (rx, ry),
            'color': color,
            'name': name
        })
    
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
        glClearColor(0.05, 0.05, 0.1, 1.0)
        
        draw_grid(width, height, spacing=50)
        
        for ellipse in all_ellipse_data:
            xc, yc = ellipse['center']
            rx, ry = ellipse['radii']
            
            draw_bounding_box(xc, yc, rx, ry)
            
            draw_axes(xc, yc, rx, ry)
            
            draw_points(ellipse['points'], ellipse['color'])
        
        glfw.swap_buffers(window)
        glfw.poll_events()
    
    glfw.terminate()

if __name__ == "__main__":
    main()
