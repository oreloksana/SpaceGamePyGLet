from random import randint

import pyglet
from pyglet.window import key, FPSDisplay
from pyglet.sprite import Sprite
from GameObjects import GameObject, preload_image


class GameWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_location(400, 100)
        self.frame_rate = 1/60.0
        self.fps_display = FPSDisplay(self)
        self.fps_display.label.font_size = 40

        self.main_batch = pyglet.graphics.Batch()

        enemy_ship = pyglet.image.load("res/sprites/enemyShip_Sh01.png")
        enemy_ship_seq = pyglet.image.ImageGrid(enemy_ship, 1, 15, item_width=100, item_height=100)
        enemy_ship_animation =pyglet.image.Animation.from_image_sequence(enemy_ship_seq[0:], 0.1, loop=True)
        self.enemy_sprite = pyglet.sprite.Sprite(enemy_ship_animation, x=400, y=400, batch=self.main_batch)

        explosion = pyglet.image.load("res/sprites/explosion.png")
        explosion_seq = pyglet.image.ImageGrid(explosion, 4, 5, item_width=96, item_height=96)
        explosion_animation = pyglet.image.Animation.from_image_sequence(explosion_seq[0:], 0.1, loop=True)
        self.explosion_sprite = pyglet.sprite.Sprite(explosion_animation, x=700, y=400, batch=self.main_batch)

        enemy = pyglet.image.load('res/sprites/alien.png')
        self.enemy_list = []
        for i in range(5):
            self.enemy_list.append(pyglet.sprite.Sprite(enemy, x=randint(200, 800), y=randint(500, 800), batch=self.main_batch))

        text = pyglet.text.Label("testing text", x=500, y=450, batch=self.main_batch)
        text.italic=True
        text.bold = True
        text.font_size = 20

        self.right = False
        self.left = False
        self.player_speed = 300
        self.fire = False
        self.player_fire_rate = 0

        player_spr = Sprite(preload_image('plane.png'))

        self.player = GameObject(450, 100, player_spr)

        self.player_laser = preload_image('laser.png')
        self.player_laser_list = []


        self.space_list = []
        self.space_img = preload_image('images.jpg')
        for i in range(3):
            self.space_list.append(GameObject(0, i*1300, Sprite(self.space_img)))


    def on_key_press(self, symbol, modifiers):
        if symbol == key.RIGHT:
            self.right = True
        if symbol == key.LEFT:
            self.left = True
        if symbol == key.SPACE:
            self.fire = True
        if symbol == key.ESCAPE:
            pyglet.app.exit()



    def on_key_release(self, symbol, modifiers):
        if symbol == key.RIGHT:
            self.right = False
        if symbol == key.LEFT:
            self.left = False
        if symbol == key.SPACE:
            self.fire = False

    def on_draw(self):
        self.clear()
        for space in self.space_list:
            space.draw()
        self.player.draw()
        for lsr in self.player_laser_list:
            lsr.draw()
        self.main_batch.draw()

        self.fps_display.draw()


    def update_player(self, dt):
        self.player.update()
        if self.right and self.player.posx < 950 - self.player.width:
            self.player.posx += self.player_speed * dt
        if self.left and self.player.posx > 50:
            self.player.posx -= self.player_speed * dt


    def update_player_laser(self,dt):
        for lsr in self.player_laser_list:
            lsr.update()
            lsr.posy += 400 * dt
            if lsr.posy > 950:
                self.player_laser_list.remove(lsr)


    def player_fire(self, dt):
        self.player_fire_rate -= dt
        if self.player_fire_rate <= 0:
            self.player_laser_list.append(GameObject(self.player.posx + 39, self.player.posy + 85, Sprite(self.player_laser)))
            self.player_fire_rate += 0.2


    def update_space(self, dt):
        for space in self.space_list:
            space.update()
            space.posy -= 50 * dt
            if space.posy <= -1500:
                self.space_list.remove(space)
                self.space_list.append(GameObject(0, 1500, Sprite(self.space_img)))



    def update(self, dt):
        self.update_player(dt)
        if self.fire:
            self.player_fire(dt)
        self.update_player_laser(dt)
        self.update_space(dt)


if __name__ == "__main__":
    window = GameWindow(1000, 900, "Space Invaders", resizable=False)
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()