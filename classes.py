import os, pygame
from pygame.locals import *
from pygame.compat import geterror
from utils import load_image
import numpy as np
from constants import *

#classes for our game objects
class DataStore:
    def __init__(self):
        self.tile_imgs = [load_image(img_n, None) for img_n in IMG_NAMES]

class Tile(pygame.sprite.Sprite):
    """moves a monkey critter across the screen. it can spin the
       monkey when it is punched."""
    def __init__(self, pos, data):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.data = data.tile_imgs
        self.image, self.rect = data.tile_imgs[0]
        self.originals = self.image.copy();
        self.rect.topleft = pos
        self.tt = 0

    def zoom(self, zoom):
        _, orig_rect = self.data[self.tt]
        self.image = pygame.transform.scale(self.data[self.tt][0], (int(orig_rect.width*zoom), int(orig_rect.height*zoom)))
        pos = self.rect.topleft
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def set_tile(self, tt):
        self.tt = int(tt)
            
class Camera:
    """Manages the visible part of the world"""
    def __init__(self, rw_pos, w, h, zoom):
        self.rw_pos = np.array(rw_pos)-1
        rw_w = int(np.ceil(w/(TILE_SIZE*zoom)))
        rw_h = int(np.ceil(h/(TILE_SIZE*zoom)))
        self.rw_dim = np.array([rw_w, rw_h])+2
        print(self.rw_dim)
        self.w = w
        self.h = h
        self.zoom = zoom

    def set_zoom(self, zoom):
        if zoom < 0.6:
            return
        rw_w = int(np.ceil(self.w/(TILE_SIZE*zoom)))
        rw_h = int(np.ceil(self.h/(TILE_SIZE*zoom)))
        self.rw_dim = np.array([rw_w, rw_h])+2
        self.zoom = zoom;

    def rw_to_camera(self, p):
        p = np.array(p)
        return (p - self.rw_pos) * (TILE_SIZE-0.9) * self.zoom

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
        sx, ex, sy, ey = int(np.max([sx, 0])), int(ex), int(np.max([sy, 0])), int(ey)
        return self.tiles[sx:ex, sy:ey].reshape((-1, 3))
        

