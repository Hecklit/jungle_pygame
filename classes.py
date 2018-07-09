import os, pygame
from pygame.locals import *
from pygame.compat import geterror
from utils import load_image
import numpy as np
from constants import *

#classes for our game objects
class Fist(pygame.sprite.Sprite):
    """moves a clenched fist on the screen, following the mouse"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image('walker.png', -1)
        self.punching = 0

    def update(self):
        "move the fist based on the mouse position"
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos
        if self.punching:
            self.rect.move_ip(5, 10)

    def punch(self, target):
        "returns true if the fist collides with the target"
        if not self.punching:
            self.punching = 1
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)

    def unpunch(self):
        "called to pull the fist back"
        self.punching = 0

class DataStore:
    def __init__(self):
        self.tile_imgs = [load_image(img_n, None) for img_n in IMG_NAMES]


class Tile(pygame.sprite.Sprite):
    """moves a monkey critter across the screen. it can spin the
       monkey when it is punched."""
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = load_image('stone.bmp', None)
        self.originals = self.image.copy();
        # screen = pygame.display.get_surface()
        # self.area = screen.get_rect()
        self.rect.topleft = pos

    def zoom(self, zoom):
        orig_rect = self.original.get_rect()
        self.image = pygame.transform.scale(self.original, (int(orig_rect.width*zoom), int(orig_rect.height*zoom)))
        pos = self.rect.topleft
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def set_tile(self, tt):
        if tt == 0:
            self.image, _ = load_image('sky.bmp', None)
        else:
            self.image, _ = load_image('stone.bmp', None)
            
class Camera:
    """Manages the visible part of the world"""
    def __init__(self, rw_pos, rw_w, rw_h, w, h, zoom):
        self.rw_pos = np.array(rw_pos)
        self.rw_dim = np.array([rw_w, rw_h])
        self.w = w
        self.h = h
        self.zoom = zoom

    def rw_to_camera(self, p):
        p = np.array(p)
        return (p + self.rw_pos) * TILE_SIZE * self.zoom

class World:
    """Main data structure to keep all infos about static world data
    it is not responsible to display the world just keep all the data about it"""
    def __init__(self, w, h):
        self.tiles = np.zeros((w, h, 3))
        x_ind, y_ind = np.indices(self.tiles.shape[:2])
        self.tiles[:, :, 0] = x_ind
        self.tiles[:, :, 1] = y_ind
        self.tiles[:, :, 2] = np.random.choice(2, size=self.tiles.shape[:2])

    def get_flat_slice(self, sx, ex, sy, ey):
        return self.tiles[sx:ex, sy:ey].reshape((-1, 3))
        

