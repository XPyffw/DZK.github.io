import pygame

# 初始化Pygame
pygame.init()

# 游戏窗口尺寸
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 600

# 颜色定义（RGB）
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# 创建游戏窗口和游戏区域
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
play_area = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT - 100)

# 设置窗口标题
pygame.display.set_caption("Brick Breaker")

# 定义游戏变量
ball_x = 240
ball_y = 300
ball_dx = 3
ball_dy = -3
paddle_x = 200
paddle_y = 550
paddle_dx = 0
block_width = 60
block_height = 20
block_list = []
for row in range(5):
    for column in range(8):
        block_list.append(
            pygame.Rect(column * (block_width + 4) + 6, row * (block_height + 4) + 50, block_width, block_height))


# 定义游戏函数
def update_ball():
    global ball_x, ball_y, ball_dx, ball_dy, paddle_x, paddle_y

    # 更新球的位置
    ball_x += ball_dx
    ball_y += ball_dy

    # 检测球是否撞到左右边界
    if ball_x < 0 or ball_x > SCREEN_WIDTH:
        ball_dx *= -1

    # 检测球是否撞到顶部
    if ball_y < 0:
        ball_dy *= -1

    # 检测球是否撞到挡板
    if ball_y > paddle_y and (paddle_x - 10) <= ball_x <= (paddle_x + 70):
        ball_dy *= -1

    # 检测球是否撞到砖块
    for block in block_list:
        if ball_y < block.y + block_height and block.x <= ball_x <= block.x + block_width:
            block_list.remove(block)
            ball_dy *= -1

    # 检测游戏结束
    if ball_y > SCREEN_HEIGHT:
        return False

    return True


def update_paddle():
    global paddle_x, paddle_dx

    # 更新挡板的位置
    paddle_x += paddle_dx

    # 检测挡板是否撞到边界
    if paddle_x < 0:
        paddle_x = 0
    elif paddle_x > SCREEN_WIDTH - 80:
        paddle_x = SCREEN_WIDTH - 80


def draw_objects():
    # 绘制游戏区域
    pygame.draw.rect(screen, BLUE, play_area)

    # 绘制球和挡板
    pygame.draw.circle(screen, RED, (ball_x, ball_y), 10)
    pygame.draw.rect(screen, GREEN, (paddle_x, paddle_y, 80, 10))

    # 绘制砖块
    for block in block_list:
        pygame.draw.rect(screen, WHITE, block)


# 游戏循环
clock = pygame.time.Clock()
running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                paddle_dx = -5
            elif event.key == pygame.K_RIGHT:
                paddle_dx = 5
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                paddle_dx = 0

    # 更新游戏状态
    update_paddle()
    if not update_ball():
        running = False

    # 绘制游戏对象
    screen.fill(BLACK)
    draw_objects()

    # 更新屏幕显示
    pygame.display.flip()

    # 控制游戏速度
    clock.tick(60)

# 退出Pygame
pygame.quit()
