from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
from naoqi import ALProxy

NAO_IP = "mistcalf.local"

tts = None

class PongBall(Widget):
    # Velocity of the ball on the x and y axis.
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    
    # Referencelist property so we can use ball.velocity as
    # shorthand, just like e.g. w.pos for w.x and w.y
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    
    # ''move'' function will move the ball one step. This
    # will be called in equal intervals to animate the ball.
    
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class PongGame(Widget):
    ball = ObjectProperty(None)
    
    global tts
    tts = ALProxy("ALTextToSpeech", NAO_IP, 9559)
    
    def serve_ball(self):
        self.ball.center = self.center
        self.ball.velocity = Vector(4, 0).rotate(randint(0, 360))
    
    def update(self, dt):
        # Call ball.move and other stuff.
        self.ball.move()
        
        # Bounce off top and bottom.
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1
            tts.say("Ow!")
            
        # Bounce off left and right.
        if (self.ball.x < 0) or (self.ball.right > self.width):
            self.ball.velocity_x *= -1
            tts.say("Ouch!")

class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game
    
def main():
    
    PongApp().run()    

if __name__ == "__main__":
    main()