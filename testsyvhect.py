"""
Platformer Game
"""


import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"


# Constants used to scale our sprites from their original size

CHARACTER_SCALING = 0.5
CHARACTER2_SCALING = 1.0
TILE_SCALING = 0.5
Jump = 10
GRAVITY = 1
Player2Speed = 5

class MyGame(arcade.Window):
    aftrhit = 2
    savemsg = ""
    Direc = 0
    Direc2 = 0
    UseD =False
    UseD2 = False
    CD = 0
    CD2 = 0
    Fjump = False
    Fjump2 = False
    Xspeed = 5
    Xspeed2 = 5
    Pspeed = 15
    Pspeed2 = 15
    Btime = 0
    Btime2 = 0
    Djump = 0
    Djump2 = 0
    SaveX = 0
    SaveX2 = 0
    hitpic = True
    """
    Main application class.
    """
    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # These are 'lists' that keep track of our sprites. Each sprite should

        # go into a list.
        self.scene = None
        self.scene2 = None

        # Separate variable that holds the player sprite
        self.player_sprite = None
        self.physics_engine = None

        self.player_sprite2 = None
        self.physics_engine2 = None

        self.background  =  arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
        if self.background is None:
            print("Error loading background image!")

        self.additional_picture = arcade.load_texture("Hit.png")
        if self.additional_picture is None:
            print("Error loading additional picture!")

    def setup(self):

        """Set up the game here. Call this function to restart the game."""

        self.scene = arcade.Scene()
        self.scene2 = arcade.Scene()
        # Create the Sprite lists
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)

        self.scene2.add_sprite_list("Player")
        self.scene2.add_sprite_list("Walls", use_spatial_hash=True)


        # Set up the player, specifically placing it at these coordinates.

        image_source = r"Picture1.PNG"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 100
        self.player_sprite.bottom = 264
        self.scene.add_sprite("Player", self.player_sprite)

        image_source = r"Picture2.PNG"
        self.player_sprite2 = arcade.Sprite(image_source, CHARACTER2_SCALING)
        self.player_sprite2.center_x = 900
        self.player_sprite2.bottom = 264
        self.scene.add_sprite("Player", self.player_sprite2)
        # Create the ground

        # This shows using a loop to place multiple sprites horizontally

        for x in range(100, 901, 50):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
            wall.center_x = x
            wall.bottom = 200
            self.scene.add_sprite("Walls", wall)
            self.scene2.add_sprite("Walls", wall)
        # Put some crates on the ground

        # This shows using a coordinate list to place sprites
        coordinate_list = [[100, 400],[600, 300], [700, 300]]
        for coordinate in coordinate_list:
            # Add a crate on the ground
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", TILE_SCALING)
            wall.position = coordinate
            self.scene.add_sprite("Walls", wall)
            self.scene2.add_sprite("Walls", wall)
            # Create the 'physics engine'
            self.physics_engine = arcade.PhysicsEnginePlatformer(
                self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["Walls"])

            self.physics_engine2 = arcade.PhysicsEnginePlatformer(
                self.player_sprite2, gravity_constant=GRAVITY, walls=self.scene2["Walls"])


    def on_draw(self):
        """Render the screen."""
        # Clear the screen to the background color
        self.clear()
        # Draw our sprites
        self.scene.draw()
        self.scene2.draw()
        arcade.start_render()

        # Draw the background image
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT,
                                      self.background)

        # Draw the additional picture on top of the background
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 200, 200, self.additional_picture)

    def key(self):
        pass
        #player one
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        ALLBUTTONS = {"W", "A", "D", "S", "F", "R", "P", "C"}
        savekey = ''
        if key == arcade.key.W:
            savekey = 'W'
            if self.Djump<2:
                self.player_sprite.change_y=self.Pspeed
                self.Djump+=1
                self.Fjump = True
        if self.UseD==False:
            if key == arcade.key.A:
                savekey='A'
                self.Direc = -self.Xspeed
                self.player_sprite.change_x = -self.Xspeed
            elif key == arcade.key.D:
                savekey='D'
                self.Direc = self.Xspeed
                self.player_sprite.change_x = self.Xspeed
        if key == arcade.key.R:
            savekey='R'
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = 25
                self.Btime = 1
                self.SaveX = self.player_sprite.center_x
        if key == arcade.key.F:
            savekey='F'
            self.Dash()
        if key == arcade.key.P:
            savekey='P'
            self.setup()
        if key == arcade.key.C:
            savekey='C'
            self.hitpic = True
            self.attack(self.player_sprite, self.player_sprite2,self.Direc,self.scene2)

        #self.savems= self.my_socket.recv(1024).decode()
        #key = self.savems


        #player two

        if key == arcade.key.UP:
            if self.Djump2 < 2:
                self.player_sprite2.change_y = self.Pspeed2
                self.Djump2 += 1
                self.Fjump2 = True
        if self.UseD2 == False:
            if key == arcade.key.LEFT:
                self.Direc2 = -self.Xspeed2
                self.player_sprite2.change_x = -self.Xspeed2
            elif key == arcade.key.RIGHT:
                self.Direc2 = self.Xspeed2
                self.player_sprite2.change_x = self.Xspeed2
        if key == arcade.key.L:
            if self.physics_engine2.can_jump():
                self.player_sprite2.change_y = 25
                self.Btime2 = 1
                self.SaveX2 = self.player_sprite2.center_x
        if key == arcade.key.K:
            self.Dash2()
        if key == arcade.key.P:
            self.setup()
        if key == arcade.key.J:
            self.hitpic = True
            self.attack(self.player_sprite2, self.player_sprite,self.Direc2,self.scene)

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        if key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.D:
            self.player_sprite.change_x = 0

        if key == arcade.key.LEFT:
            self.player_sprite2.change_x = 0
        elif key == arcade.key.RIGHT:
            self.player_sprite2.change_x = 0

    def block1(self):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
            wall.center_x= self.SaveX
            wall.top = self.player_sprite.bottom
            self.scene.add_sprite("Walls", wall)
            self.scene2.add_sprite("Walls", wall)
            #wall.kill()

    def block2(self):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
            wall.center_x= self.SaveX2
            wall.top = self.player_sprite2.bottom
            self.scene.add_sprite("Walls", wall)
            self.scene2.add_sprite("Walls", wall)

    def Dash(self):
        self.UseD = True
        self.CD = 3
        self.player_sprite.change_x = self.Direc*10

    def Dash2(self):
        self.UseD2 = True
        self.CD2 = 3
        self.player_sprite2.change_x = self.Direc2*10

    def attack(self,player1,player2,Direc,scene):
        Hit = arcade.Sprite("HIT.png", 0.5)
        if Direc > 0:
            Hit.left = player1.right
            Hit.top = player1.top
            scene.add_sprite("Walls", Hit)
            if (arcade.check_for_collision(Hit,player2)):
                player2.center_x = player2.center_x + 20
            if self.hitpic == False:
                Hit.kill()
        else:
            Hit.right = player1.left
            Hit.top = player1.top
            scene.add_sprite("Walls", Hit)
            if (arcade.check_for_collision(Hit, player2)):
                player2.center_x = player2.center_x - 20
            if self.hitpic == False:
                Hit.kill()
        self.hitpic = False

    def CheckEnd(self):
        if self.player_sprite.top < 0 or self.player_sprite2.top<0:
            self.setup()
   # def attack2(self):
    def on_update(self, delta_time):
        """Movement and game logic"""
        if self.Btime>0:
            self.block1()
            self.Btime-=0.1

        if self.physics_engine.can_jump():
            if self.Fjump==True:
                self.Djump = 1
                self.Fjump =False
            else:
                self.Djump=0

        if self.UseD== True:
            if self.CD>0:
                self.CD-=1
            else:
                self.UseD=False
                self.player_sprite.change_x = 0

        #player two
        if self.Btime2>0:
            self.block2()
            self.Btime2-=0.1

        if self.physics_engine2.can_jump():
            if self.Fjump2==True:
                self.Djump2 = 1
                self.Fjump2 =False
            else:
                self.Djump2=0

        if self.UseD2== True:
            if self.CD2>0:
                self.CD2-=1
            else:
                self.UseD2=False
                self.player_sprite2.change_x = 0
        # Move the player with the physics engine

       # if self.hitpic == False:
        #    self.attack(self.player_sprite2, self.player_sprite,self.Direc2)

        self.CheckEnd()

        self.physics_engine.update()
        self.physics_engine2.update()


        #print(client.recv(1024).decode())

def main():
    """Main function"""
    window = MyGame()
    window.setup()

    arcade.run()

if __name__ == "__main__":
    main()