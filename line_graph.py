import glfw
from OpenGL.GL import *

def bresenham_line(x1, y1, x2, y2):
    points = []
    
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    
    x_step = 1 if x2 > x1 else -1
    y_step = 1 if y2 > y1 else -1
    
    x, y = x1, y1
    
    if dx > dy:
        p = 2 * dy - dx
        for _ in range(dx + 1):
            points.append((x, y))
            if p >= 0:
                y += y_step
                p += 2 * (dy - dx)
            else:
                p += 2 * dy
            x += x_step
    else:
        p = 2 * dx - dy
        for _ in range(dy + 1):
            points.append((x, y))
            if p >= 0:
                x += x_step
                p += 2 * (dx - dy)
            else:
                p += 2 * dx
            y += y_step
    
    return points

def dda_line(x1, y1, x2, y2):
    points = []
    
    dx = x2 - x1
    dy = y2 - y1
    
    steps = max(abs(dx), abs(dy))
    
    if steps == 0:
        return [(x1, y1)]
    
    x_inc = dx / steps
    y_inc = dy / steps
    
    x, y = x1, y1
    
    for _ in range(int(steps) + 1):
        points.append((round(x), round(y)))
        x += x_inc
        y += y_inc
    
    return points

def normalize_data(data, width, height, margin=50):
    """
    Normalize data to fit within the window dimensions.
    
    Parameters:
    data: List of (x, y) tuples representing the dataset
    width, height: Window dimensions
    margin: Margin from window edges
    
    Returns: Normalized data points as pixel coordinates
    """
    if not data:
        return []
    
    # Find min and max values
    x_values = [point[0] for point in data]
    y_values = [point[1] for point in data]
    
    x_min, x_max = min(x_values), max(x_values)
    y_min, y_max = min(y_values), max(y_values)
    
    # Avoid division by zero
    x_range = x_max - x_min if x_max != x_min else 1
    y_range = y_max - y_min if y_max != y_min else 1
    
    # Available drawing area
    draw_width = width - 2 * margin
    draw_height = height - 2 * margin
    
    # Normalize to pixel coordinates
    normalized = []
    for x, y in data:
        # Map x from [x_min, x_max] to [margin, width-margin]
        pixel_x = margin + ((x - x_min) / x_range) * draw_width
        # Map y from [y_min, y_max] to [height-margin, margin] (inverted for screen coords)
        pixel_y = height - margin - ((y - y_min) / y_range) * draw_height
        normalized.append((int(pixel_x), int(pixel_y)))
    
    return normalized, (x_min, x_max, y_min, y_max)

def generate_graph_lines(data_points, algorithm='bresenham'):
    all_points = []
    
    line_func = bresenham_line if algorithm == 'bresenham' else dda_line
    
    for i in range(len(data_points) - 1):
        x1, y1 = data_points[i]
        x2, y2 = data_points[i + 1]
        
        line_points = line_func(x1, y1, x2, y2)
        all_points.extend(line_points)
    
    return all_points

def draw_points(points, color=(1.0, 1.0, 1.0)):
    glColor3f(*color)
    glBegin(GL_POINTS)
    for x, y in points:
        glVertex2f(x, y)
    glEnd()

def draw_axes(width, height, margin=50):
    glColor3f(0.5, 0.5, 0.5)
    glLineWidth(1.0)
    
    glBegin(GL_LINES)
    # X-axis
    glVertex2f(margin, height - margin)
    glVertex2f(width - margin, height - margin)
    
    # Y-axis
    glVertex2f(margin, margin)
    glVertex2f(margin, height - margin)
    glEnd()

def draw_data_points_markers(points, color=(1.0, 0.0, 0.0)):
    glColor3f(*color)
    glPointSize(8.0)
    glBegin(GL_POINTS)
    for x, y in points:
        glVertex2f(x, y)
    glEnd()

def draw_grid(width, height, margin, divisions=10):
    glColor3f(0.2, 0.2, 0.2)
    glLineWidth(1.0)
    
    draw_width = width - 2 * margin
    draw_height = height - 2 * margin
    
    glBegin(GL_LINES)
    # Vertical grid lines
    for i in range(divisions + 1):
        x = margin + (draw_width / divisions) * i
        glVertex2f(x, margin)
        glVertex2f(x, height - margin)
    
    # Horizontal grid lines
    for i in range(divisions + 1):
        y = margin + (draw_height / divisions) * i
        glVertex2f(margin, y)
        glVertex2f(width - margin, y)
    glEnd()

def main():
    if not glfw.init():
        return
    
    width, height = 1000, 700
    window = glfw.create_window(width, height, "Line Graph - DDA/Bresenham Algorithm", None, None)
    
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
    
    # Sample datasets to visualize
    datasets = [
        {
            'name': 'Sales Data (Bresenham)',
            'data': [(1, 20), (2, 35), (3, 30), (4, 50), (5, 45), (6, 60), (7, 55), (8, 70), (9, 75), (10, 85)],
            'algorithm': 'bresenham',
            'color': (0.2, 0.8, 1.0)
        },
        {
            'name': 'Temperature Data (DDA)',
            'data': [(1, 15), (2, 18), (3, 22), (4, 25), (5, 28), (6, 32), (7, 30), (8, 27), (9, 23), (10, 20)],
            'algorithm': 'dda',
            'color': (1.0, 0.5, 0.2)
        }
    ]
    
    # 0 -> sales data (DDA), 1 -> temperature data (Bresenham)
    current_dataset = 1
    dataset = datasets[current_dataset]
    
    margin = 80
    
    # Normalize data to window coordinates
    normalized_points, bounds = normalize_data(dataset['data'], width, height, margin)
    
    # Generate line graph using specified algorithm
    graph_points = generate_graph_lines(normalized_points, dataset['algorithm'])
    
    for i, (x, y) in enumerate(dataset['data'], 1):
        print(f"  Point {i}: ({x}, {y})")
    
    glPointSize(2.0)
    
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
        glClearColor(0.05, 0.05, 0.1, 1.0)
        
        draw_grid(width, height, margin, divisions=10)
        
        draw_axes(width, height, margin)
        
        draw_points(graph_points, dataset['color'])
        
        draw_data_points_markers(normalized_points, (1.0, 0.0, 0.0))
        
        glfw.swap_buffers(window)
        glfw.poll_events()
    
    glfw.terminate()

if __name__ == "__main__":
    main()
