import glfw
from OpenGL.GL import *
import math

def draw_filled_circle_sector(cx, cy, radius, start_angle, end_angle, color, segments=100):
    glColor3f(*color)
    glBegin(GL_TRIANGLE_FAN)
    
    glVertex2f(cx, cy)
    
    # Calculate number of segments for this sector
    angle_range = end_angle - start_angle
    sector_segments = max(int(segments * (angle_range / (2 * math.pi))), 2)
    
    # Draw vertices along the arc
    for i in range(sector_segments + 1):
        angle = start_angle + (angle_range * i / sector_segments)
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        glVertex2f(x, y)
    
    glEnd()

def draw_circle_outline(cx, cy, radius, color=(1.0, 1.0, 1.0), segments=100):
    glColor3f(*color)
    glLineWidth(2.0)
    glBegin(GL_LINE_LOOP)
    
    for i in range(segments):
        angle = 2.0 * math.pi * i / segments
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        glVertex2f(x, y)
    
    glEnd()

def draw_sector_outline(cx, cy, radius, start_angle, end_angle, color=(1.0, 1.0, 1.0), segments=100):
    glColor3f(*color)
    glLineWidth(2.0)
    
    # Draw the arc
    glBegin(GL_LINE_STRIP)
    angle_range = end_angle - start_angle
    sector_segments = max(int(segments * (angle_range / (2 * math.pi))), 2)
    
    for i in range(sector_segments + 1):
        angle = start_angle + (angle_range * i / sector_segments)
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        glVertex2f(x, y)
    
    glEnd()
    
    # Draw radial lines
    glBegin(GL_LINES)
    # Start radius
    glVertex2f(cx, cy)
    glVertex2f(cx + radius * math.cos(start_angle), cy + radius * math.sin(start_angle))
    # End radius
    glVertex2f(cx, cy)
    glVertex2f(cx + radius * math.cos(end_angle), cy + radius * math.sin(end_angle))
    glEnd()

def create_pie_chart(data, labels, colors, cx, cy, radius):
    total = sum(data)
    sectors = []
    
    current_angle = -math.pi / 2  # Start at top (12 o'clock position)
    
    for i, (value, label, color) in enumerate(zip(data, labels, colors)):
        percentage = (value / total) * 100
        angle_size = (value / total) * 2 * math.pi
        
        sector_info = {
            'value': value,
            'percentage': percentage,
            'label': label,
            'color': color,
            'start_angle': current_angle,
            'end_angle': current_angle + angle_size,
            'mid_angle': current_angle + angle_size / 2
        }
        
        sectors.append(sector_info)
        current_angle += angle_size
    
    return sectors

def draw_pie_chart(sectors, cx, cy, radius):
    for sector in sectors:
        draw_filled_circle_sector(
            cx, cy, radius,
            sector['start_angle'],
            sector['end_angle'],
            sector['color']
        )
        
        # Draw outline for each sector
        draw_sector_outline(
            cx, cy, radius,
            sector['start_angle'],
            sector['end_angle'],
            (0.2, 0.2, 0.2)
        )

def draw_legend(sectors, x, y, box_size=20, spacing=30):
    for i, sector in enumerate(sectors):
        y_pos = y + i * spacing
        
        # Draw colored box
        glColor3f(*sector['color'])
        glBegin(GL_QUADS)
        glVertex2f(x, y_pos)
        glVertex2f(x + box_size, y_pos)
        glVertex2f(x + box_size, y_pos + box_size)
        glVertex2f(x, y_pos + box_size)
        glEnd()
        
        # Draw box outline
        glColor3f(1.0, 1.0, 1.0)
        glLineWidth(1.0)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x, y_pos)
        glVertex2f(x + box_size, y_pos)
        glVertex2f(x + box_size, y_pos + box_size)
        glVertex2f(x, y_pos + box_size)
        glEnd()

def draw_labels_on_chart(sectors, cx, cy, radius):
    for sector in sectors:
        # Calculate position for label
        label_radius = radius * 0.6
        mid_angle = sector['mid_angle']
        
        label_x = cx + label_radius * math.cos(mid_angle)
        label_y = cy + label_radius * math.sin(mid_angle)
        
        # Draw a small circle at label position to show percentage location
        glColor3f(1.0, 1.0, 1.0)
        glPointSize(8.0)
        glBegin(GL_POINTS)
        glVertex2f(label_x, label_y)
        glEnd()

def main():
    if not glfw.init():
        return
    
    width, height = 1000, 700
    window = glfw.create_window(width, height, "Pie Chart - OpenGL Implementation", None, None)
    
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
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    
    data = [30, 45, 15, 60, 25]
    labels = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
    colors = [
        (1.0, 0.2, 0.2),   # Red
        (0.2, 0.8, 0.2),   # Green
        (0.2, 0.4, 1.0),   # Blue
        (1.0, 0.8, 0.2),   # Yellow
        (1.0, 0.4, 0.8),   # Pink
    ]
    
    center_x = width // 2 - 100
    center_y = height // 2
    radius = 200
    
    sectors = create_pie_chart(data, labels, colors, center_x, center_y, radius)
    
    print("Pie Chart Data:")
    print("-" * 60)
    total = sum(data)
    for sector in sectors:
        print(f"{sector['label']:12s}: {sector['value']:6.1f} ({sector['percentage']:5.1f}%)")
    print("-" * 60)
    print(f"{'Total':12s}: {total:6.1f} (100.0%)")
    print("\nColors:")
    for sector in sectors:
        print(f"{sector['label']:12s}: RGB{sector['color']}")
    
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
        glClearColor(0.1, 0.1, 0.15, 1.0)
        
        draw_pie_chart(sectors, center_x, center_y, radius)
        
        draw_labels_on_chart(sectors, center_x, center_y, radius)
        
        draw_legend(sectors, width - 250, 100)
        
        glColor3f(0.7, 0.7, 0.7)
        glLineWidth(2.0)
        glBegin(GL_LINES)
        glVertex2f(width // 2 - 100, 30)
        glVertex2f(width // 2 + 100, 30)
        glEnd()
        
        glfw.swap_buffers(window)
        glfw.poll_events()
    
    glfw.terminate()

if __name__ == "__main__":
    main()
