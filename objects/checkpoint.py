import pygame
from objects.basis import Object
from utils.sprites import load_sprite_sheets

class Checkpoint(Object):
    SPRITES = {
        "checkpoint": [
            pygame.image.load("assets/Items/Checkpoints/Checkpoint/Checkpoint (Flag Idle)(64x64).png").convert_alpha(),
            pygame.image.load("assets/Items/Checkpoints/Checkpoint/Checkpoint (Flag Idle)(64x64).png").convert_alpha()
        ]
    }

    def __init__(self, x, y):
        width, height = Checkpoint.SPRITES["checkpoint"][0].get_size()
        super().__init__(x, y, width, height, name="checkpoint")
        self.image = self.SPRITES["checkpoint"][0]
        self.activated = False

    def activate(self):
        self.activated = True
        # Ganti sprite saat aktif? Tambahkan di sini