import pygame

WIN = pygame.display.set_mode((800, 600))
from config import WIDTH, HEIGHT, FPS
from utils.background import get_background
from utils.collisions import handle_move
from utils.sprites import get_block
from player import Player
from objects.block import Block
from objects.fire import Fire
from levels.level1 import level_map
from utils.level_loader import load_level
from objects.checkpoint import Checkpoint

pygame.init()
pygame.display.set_caption("Platformer")
window = pygame.display.set_mode((WIDTH, HEIGHT))


def draw(window, background, bg_image, player, objects, offset_x, offset_y):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x, offset_y)

    player.draw(window, offset_x, offset_y)
    pygame.display.update()


def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Green.png")

    block_size = 96
    LEVEL_WIDTH = 30 * block_size
    LEVEL_HEIGHT = 10 * block_size

    player = Player(480, 384, 50, 50)
    spawn_point = player.rect.topleft

    fire = Fire(100, HEIGHT - block_size - 64, 16, 32)
    fire.on()

    floor = [Block(i * block_size, HEIGHT - block_size, block_size)
             for i in range(-WIDTH // block_size, WIDTH * 2 // block_size)]

    objects = load_level(level_map)
    checkpoints = [obj for obj in objects if isinstance(obj, Checkpoint)]
    spawn_point = player.rect.topleft  # posisi awal

    # SETUP CHECKPOINT
    checkpoints = pygame.sprite.Group()
    checkpoint1 = Checkpoint(700, HEIGHT - block_size * 2)
    checkpoint2 = Checkpoint(1500, HEIGHT - block_size * 2)
    checkpoints.add(checkpoint1, checkpoint2)

    offset_x = 0
    offset_y = 0

    scroll_area_width = 200
    scroll_area_height = 150
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and player.jump_count < 2:
                    player.jump()

        player.loop(FPS)
        fire.loop()
        handle_move(player, objects, spawn_point)

        # CEK COLLISION DENGAN CHECKPOINT
        # Cek checkpoint
        for checkpoint in checkpoints:
            if pygame.sprite.collide_mask(player, checkpoint) and not checkpoint.activated:
                checkpoint.activate()
                spawn_point = (checkpoint.rect.centerx - player.rect.width // 2, checkpoint.rect.top - player.rect.height)

        # Cek jatuh
        if player.rect.top > LEVEL_HEIGHT:
            player.make_hit()
            player.rect.topleft = spawn_point
            player.x_vel = 0
            player.y_vel = 0

            offset_x = player.rect.centerx - WIDTH // 2
            offset_y = player.rect.centery - HEIGHT // 2
            offset_x = max(0, min(offset_x, LEVEL_WIDTH - WIDTH))
            offset_y = max(0, min(offset_y, LEVEL_HEIGHT - HEIGHT))

        draw(window, background, bg_image, player, objects, offset_x, offset_y)

        # DRAW CHECKPOINT
        for checkpoint in checkpoints:
            checkpoint.draw(window, offset_x, offset_y)

        # SCROLLING
        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
            (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

        if ((player.rect.bottom - offset_y >= HEIGHT - scroll_area_height) and player.y_vel > 0) or (
            (player.rect.top - offset_y <= scroll_area_height) and player.y_vel < 0):
            offset_y += player.y_vel

    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)
