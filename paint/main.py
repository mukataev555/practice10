import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    canvas = pygame.Surface((640, 480))
    canvas.fill((0, 0, 0))
    
    clock = pygame.time.Clock()
    
    radius = 15
    mode = 'red' # Текущий цвет/инструмент
    drawing = False
    last_pos = None 
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            if event.type == pygame.KEYDOWN:
                # Можно поменять цвет, КРАСНЫЙ, СИНИЙ, ЗЕЛЕНЫЙ
                if event.key == pygame.K_r: mode = 'red'
                elif event.key == pygame.K_g: mode = 'green'
                elif event.key == pygame.K_b: mode = 'blue'
                elif event.key == pygame.K_t: mode = 'white'
                #Ластик просто рисует черным
                elif event.key == pygame.K_e: mode = 'eraser'
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    drawing = True
                    pos = event.pos
                    draw_shape(canvas, mode, pos, radius)
                
                elif event.button == 3: 
                    radius = max(1, radius - 1)
                elif event.button == 2: 
                    radius = min(100, radius + 1)

            if event.type == pygame.MOUSEBUTTONUP:
                drawing = False
                last_pos = None

            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    mouse_pos = event.pos
                    if last_pos:
                        # Рисуем плавную линию между кадрами
                        drawLine(canvas, last_pos, mouse_pos, radius, mode)
                    last_pos = mouse_pos
        
        screen.blit(canvas, (0, 0))

        mouse_p = pygame.mouse.get_pos()
        preview_color = get_color(mode)
        pygame.draw.circle(screen, preview_color, mouse_p, radius, 1)
        
        pygame.display.flip()
        clock.tick(60)

def get_color(mode):
    if mode == 'red': 
        return (255, 0, 0)
    if mode == 'green': 
        return (0, 255, 0)
    if mode == 'blue': 
        return (0, 0, 255)
    if mode == 'eraser': 
        return (0, 0, 0) # Ластик совпадает с фоном
    return (255, 255, 255)

def draw_shape(surface, mode, pos, radius):
    color = get_color(mode)
    # если зажат Shift, рисуем квадрат, иначе круг
    if pygame.key.get_pressed()[pygame.K_LSHIFT]:
        #Нарисует квадрат, если зажать SHIFT
        pygame.draw.rect(surface, color, (pos[0]-radius, pos[1]-radius, radius*2, radius*2))
    else:
        # Нарисует КРУГ
        pygame.draw.circle(surface, color, pos, radius)

def drawLine(surface, start, end, width, mode):
    color = get_color(mode)
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int(start[0] + float(i) / distance * dx)
        y = int(start[1] + float(i) / distance * dy)
        pygame.draw.circle(surface, color, (x, y), width)

main()