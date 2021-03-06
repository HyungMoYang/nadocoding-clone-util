
import pygame
import os

# 기본 초기화 (반드시 해야 하는 것들)
pygame.init()  # pygame 초기화 (반드시 필요)

# 화면 크기 설정
screen_width = 640  # 가로 크기
screen_height = 480  # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정 - 윈도우 타이틀
pygame.display.set_caption("Nado Pang")  # 게임 타이틀

# FPS
clock = pygame.time.Clock()

##################################################################################

# 1. 사용자 게임 초기화(배경 화면, 게임 이미지, 좌표, 폰트, 등)

current_path = os.path.dirname(__file__)  # 현재 파일의 위치 반환

# 현재 위치+images파일: images 폴더위치 반환
image_path = os.path.join(current_path, "images")

### 배경 ###
# 배경 만들기
background = pygame.image.load(os.path.join(image_path, "background.png"))

### 스테이지 ###
# 스테이지 만들기
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]  # 스테이지 위에 캐릭터를 두기 위해서

### 캐릭터 ###
# 캐릭터 만들기
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = screen_width / 2 - character_width / 2
character_y_pos = screen_height - character_height - stage_height  # 스테이지 위

# 캐릭터 이동 방향
character_to_x = 0

# 캐릭터 이동속도
character_speed = 5

### 무기 ###
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# 무기는 한 번에 여러 발 발사 가능
weapons = []

# 무기 이동속도
weapon_speed = 10

running = True
while running:
    dt = clock.tick(60)

    # 2. 이벤트 처리(키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:  # space를 눌렀을 때, 공격
                weapon_x_pos = character_x_pos + \
                    (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])  # 무기를 여러번 쏘기 위해서

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    # 3. 게임 캐릭터 위치 정의
    character_x_pos += character_to_x

    # 경계 값 처리
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # 무기의 위치 조정 - 위에서 weapon을 image의 변수로 이미 사용함 - w사용
    for w in weapons:
        w[1] = w[1] - weapon_speed  # weapons 배열의 발사된 무기의 y좌표 값을 변경
    # weapons = [[w[0], w[1] - weapon_speed] for w in weapons] # 한 줄 for

    # 천장에 닿은 무기 없애기
    for index, w in enumerate(weapons):
        if w[1] < 0:
            del weapons[index]
    # weapons = [[w[0], w[1]] for w in weapons if w[1] > 0] # 한 줄 for

    # 4. 충돌 처리

    # 5. 화면에 그리기
    screen.blit(background, (0, 0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))

    pygame.display.update()  # 게임화면을 다시 그리기 - pygame에선 배경을 계속 업데이트 해주어야함

# pygame 종료
pygame.quit()
