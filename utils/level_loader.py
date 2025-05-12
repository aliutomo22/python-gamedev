from objects.block import Block
# from objects.enemy import Enemy    # Kalau sudah dibuat
# from objects.door import Door      # dst...
from objects.checkpoint import Checkpoint


BLOCK_SIZE = 96

def load_level(level_map):
    objects = []
    for y, row in enumerate(level_map):
        x = 0
        while x < len(row):
            cell = row[x:x+2] if x+1 < len(row) and row[x:x+2] in {"ET", "DJ"} else row[x]
            world_x = x * BLOCK_SIZE
            world_y = y * BLOCK_SIZE

            if cell == "X":
                objects.append(Block(world_x, world_y, BLOCK_SIZE))
            elif cell == "E":
                # objects.append(Enemy(...))
                pass
            elif cell == "ET":
                # objects.append(GunTurret(...))
                pass
                x += 1
            elif cell == "DJ":
                # objects.append(DoubleJumpPowerUp(...))
                pass
                x += 1
            elif cell == "K":
                # objects.append(Key(...))
                pass
            elif cell == "D":
                # objects.append(Door(...))
                pass
            elif cell == "C":
                checkpoint = Checkpoint(world_x, world_y)
                objects.append(checkpoint)

            x += 1
    return objects