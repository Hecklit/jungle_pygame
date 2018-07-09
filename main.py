#!/usr/bin/env python
"""
This is going to be a virtual world
"""

#Import Modules
import os, pygame
from pygame.locals import *
from pygame.compat import geterror
from utils import load_sound
from classes import Tile, World, Camera, DataStore, Actor, Fighter
from constants import *
import numpy as np

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')

def init_world_tiles(w, h, size, data):
    tiles_per_width = int(np.ceil(w/size))
    tiles_per_height = int(np.ceil(h/size))
    return [[Tile((x*size, y*size), data) for x in range(tiles_per_width)] for y in range(tiles_per_height)]

def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
#Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Jungle')
    pygame.mouse.set_visible(0)

#Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((125, 125, 125))

#Put Text On The Background, Centered
    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("Jungle", 1, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width()/2)
        background.blit(text, textpos)

#Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

#Prepare Game Objects
    clock = pygame.time.Clock()
    # whiff_sound = load_sound('whiff.wav')
    # punch_sound = load_sound('punch.wav')
    data = DataStore()
    world = World(64, 64)
    camera = Camera([0.0, 0.0], WIDTH, HEIGHT, 3)
    buffered_world_sprites = pygame.sprite.LayeredUpdates(init_world_tiles(WIDTH*2, HEIGHT*2, TILE_SIZE, data))
    displayed_world_sprites = pygame.sprite.LayeredUpdates([])

    f_sprite = Actor([0,1], data)
    f = Fighter([3, 3], 1, 1)
    allsprites = pygame.sprite.LayeredUpdates([f_sprite])

#Main Loop
    going = True
    while going:
        clock.tick(60)

        #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
            elif event.type == MOUSEBUTTONDOWN:
                pass
            elif event.type == MOUSEBUTTONUP:
                pass
            # elif event.type == MOUSEBUTTONDOWN and event.button == 4:

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            camera.rw_pos -= np.array([0, 0.1])*(10.0/camera.zoom)
        if pressed[pygame.K_s]:
            camera.rw_pos += np.array([0, 0.1])*(10.0/camera.zoom)
        if pressed[pygame.K_a]:
            camera.rw_pos -= np.array([0.1, 0])*(10.0/camera.zoom)
        if pressed[pygame.K_d]:
            camera.rw_pos += np.array([0.1, 0])*(10.0/camera.zoom)
        if pressed[pygame.K_q]:
            camera.set_zoom(camera.zoom+0.1)
        if pressed[pygame.K_e]:
            camera.set_zoom(camera.zoom-0.1)
    
        # update world camera
        sx, sy = camera.rw_pos
        ex, ey = camera.rw_pos + camera.rw_dim
        buffered_world_sprites.add(displayed_world_sprites.sprites())
        displayed_world_sprites.empty()
        for rw_tile in world.get_flat_slice(sx, ex, sy, ey):
            camera_pos = camera.rw_to_camera(rw_tile[:2])
            sprite = buffered_world_sprites.get_sprite(0)
            sprite.rect.topleft = camera_pos
            sprite.set_tile(rw_tile[2])
            sprite.zoom(camera.zoom)
            buffered_world_sprites.remove(sprite)
            displayed_world_sprites.add(sprite)

        f_sprite.rect.topleft = camera.rw_to_camera(f.pos)
        f_sprite.zoom(camera.zoom)

        #Draw Everything
        screen.blit(background, (0, 0))
        displayed_world_sprites.draw(screen)
        allsprites.draw(screen)
        pygame.display.flip()

    pygame.quit()

#Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
