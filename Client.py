"""
Platformer Game
"""
import socket
import select
import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"
IP = '127.0.0.1'
PORT = 1729

# Constants used to scale our sprites from their original size

CHARACTER_SCALING = 0.5
CHARACTER2_SCALING = 1.0
TILE_SCALING = 0.5
Jump = 10
GRAVITY = 1
Player2Speed = 5

class MyGame(arcade.Window):
    resetnum = (2,"",0,0,False,False,0,0,False,False,5,5,15,15,0,0,0,0,0,0,True)
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
    resetchr = [aftrhit,savemsg,Direc,Direc2,UseD,UseD2,CD,CD2,Fjump,Fjump2,Xspeed,Xspeed2,Pspeed,Pspeed2,Btime,Btime2,Djump,Djump2,SaveX,SaveX2,hitpic]
    """
    Main application class.
    """
    def __init__(self, my_socket,inputs,charact):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # These are 'lists' that keep track of our sprites. Each sprite should
        self.my_socket = my_socket
        self.charact = charact
        self.inputs = inputs
        # go into a list.
        self.scene = None
        self.scene2 = None

        # Separate variable that holds the player sprite

        self.player_sprite = None
        self.physics_engine = None

        self.player_sprite2 = None
        self.physics_engine2 = None
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        self.left_pressed = False
        self.right_pressed = False


        self.left_pressed2 = False
        self.right_pressed2 = False


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
        if(self.charact == "1"):
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

        else:
            image_source = r"Picture1.PNG"
            self.player_sprite2 = arcade.Sprite(image_source, CHARACTER_SCALING)
            self.player_sprite2.center_x = 100
            self.player_sprite2.bottom = 264
            self.scene.add_sprite("Player", self.player_sprite2)

            image_source = r"Picture2.PNG"
            self.player_sprite = arcade.Sprite(image_source, CHARACTER2_SCALING)
            self.player_sprite.center_x = 900
            self.player_sprite.bottom = 264
            self.scene.add_sprite("Player", self.player_sprite)

        self.RESET()
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

    def key(self):
        pass
        #player one

    def update_player_speed(self,player):

        # Calculate speed based on the keys pressed
        player.change_x = 0

        if(player == self.player_sprite):
            if self.left_pressed and not self.right_pressed:
                player.change_x = -self.Xspeed
            elif self.right_pressed and not self.left_pressed:
                player.change_x = self.Xspeed
        else:
            if self.left_pressed2 and not self.right_pressed2:
                player.change_x = -self.Xspeed2
            elif self.right_pressed2 and not self.left_pressed2:
                player.change_x = self.Xspeed2

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
                self.left_pressed = True
                self.update_player_speed(self.player_sprite)
            elif key == arcade.key.D:
                savekey='D'
                self.Direc = self.Xspeed
                self.right_pressed = True
                self.update_player_speed(self.player_sprite)
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
        for x in ALLBUTTONS:
            if(savekey==x):
                print("i sent key press " + savekey)
                self.my_socket.send(savekey.encode())

        print("dik")
        #self.savems= self.my_socket.recv(1024).decode()
        #key = self.savems




        # player two
    def on_key_press2(self, key):
        if key == 'W':
            if self.Djump2 < 2:
                self.player_sprite2.change_y = self.Pspeed2
                self.Djump2 += 1
                self.Fjump2 = True
        if self.UseD2 == False:
            if key == 'A':
                self.Direc2 = -self.Xspeed2
                self.left_pressed2 = True
                self.update_player_speed(self.player_sprite2)
            elif key == 'D':
                self.Direc2 = self.Xspeed2
                self.right_pressed2 = True
                self.update_player_speed(self.player_sprite2)
        if key == 'R':
            if self.physics_engine2.can_jump():
                self.player_sprite2.change_y = 25
                self.Btime2 = 1
                self.SaveX2 = self.player_sprite2.center_x
        if key == 'F':
            self.Dash2()
        if key == 'P':
            self.setup()
        if key == 'C':
            self.hitpic = True
            self.attack(self.player_sprite2, self.player_sprite,self.Direc2,self.scene)


    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        ALLBUTTONS = {"2A","2D"}
        savekey=''
        if key == arcade.key.A:
            savekey='2A'
            self.left_pressed = False
            self.update_player_speed(self.player_sprite)
        elif key == arcade.key.D:
            savekey='2D'
            self.right_pressed = False
            self.update_player_speed(self.player_sprite)
        for x in ALLBUTTONS:
            if (savekey == x):
                print("i sent key release " + savekey)
                self.my_socket.send(savekey.encode())


    def on_key_release2(self, key):
        """Called when the user releases a key."""
        if key == '2A':
            self.left_pressed2 = False
            self.update_player_speed(self.player_sprite2)
        elif key == '2D':
            self.right_pressed2 = False
            self.update_player_speed(self.player_sprite2)



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
            #if self.hitpic == False:
           #     Hit.kill()
        else:
            Hit.right = player1.left
            Hit.top = player1.top
            scene.add_sprite("Walls", Hit)
            if (arcade.check_for_collision(Hit, player2)):
                player2.center_x = player2.center_x - 20
            #if self.hitpic == False:
        Hit.kill()
        self.hitpic = False

    def CheckEnd(self):
        if self.player_sprite.top < 0 or self.player_sprite2.top<0:
            self.setup()

    def RESET(self):
        i=0
        while i < len(self.resetchr):
            self.resetchr[i] = self.resetnum[i]
            i+=1
        self.left_pressed = False
        self.right_pressed = False
        self.left_pressed2 = False
        self.right_pressed2 = False

    def checkmul(self):
        inputs = self.inputs
        readable, _, _ = select.select(inputs, [], [], 0.00000001)
        # print(readable)
        for sock in readable:
            #  print(sock)
            # Incoming data on existing connection
            data = sock.recv(1024)
            key = data.decode()
            i=0
            while i < len(key):
                if key[i]!="2":
                    save = key[i]
                    i += 1
                else:
                    save = key[i]+key[i+1]
                    i += 2
                print("recevied " + save)
                if save == "2A":
                    self.on_key_release2(save)
                if save == "2D":
                    self.on_key_release2(save)
                else:
                    self.on_key_press2(save)
   # def attack2(self):
    def on_update(self, delta_time):
        """Movement and game logic"""
        # player two
        self.checkmul()

        # print(readable)

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

#        if self.hitpic == False:
#            self.attack(self.player_sprite2, self.player_sprite,self.Direc2)

        self.CheckEnd()

        self.physics_engine.update()
        self.physics_engine2.update()

        #loc = self.player_sprite.center_x
        #client = self.my_socket
        #client.send(str(loc).encode())
        #print(client.recv(1024).decode())

def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.bind(('0.0.0.0', 0))
    my_socket.connect((IP, PORT))
    inputs = [my_socket]
    charact = my_socket.recv(1024).decode()
    """Main function"""
    window = MyGame(my_socket,inputs,charact)
    window.setup()

    arcade.run()
    my_socket.close()

if __name__ == "__main__":
    main()