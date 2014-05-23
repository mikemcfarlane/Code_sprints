from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.button import Button

from random import randint
from time import sleep

from naoqi import ALProxy


NAO_IP = "mistcalf.local"
# Setup animatedSpeech.
BODYLANGUAGEMODECONFIG = {"bodyLanguageMode" : "contextual"}

tts = None
animatedSpeech = None
robotMotion = None

class NAOPongPaddle(Widget):
    score = NumericProperty(0)

    sound1 = SoundLoader.load('Sounds/bipReco1.wav')
    sound2 = SoundLoader.load('Sounds/bipReco2.wav')
    
    def bounce_ball(self, ball):
        # print "ball:", self.player_id
        
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset
            if self.player_id == "player1":
                self.sound1.play()
            elif self.player_id == "playerNAO":
                self.sound2.play()
            
            

class NAOPongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
        

class NAOPongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    playerNAO = ObjectProperty(None)

    global tts
    
    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = Vector(4, 0).rotate(randint(0, 360))
    
    def update(self, dt):
        # Call ball.move and other stuff.
        self.ball.move()
        
        # todo: update self.playerNAO.center_y based on NAOs current position
  
        # Bounce of paddles.
        self.player1.bounce_ball(self.ball)
        self.playerNAO.bounce_ball(self.ball)
        
        # Bounce off top or bottom.
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1
            
        # Went off to side to score point.
        if self.ball.x < self.x:
            id = animatedSpeech.post.say("I win!", BODYLANGUAGEMODECONFIG)
            animatedSpeech.wait(id, 0)
            self.playerNAO.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.x > self.width:
            id = animatedSpeech.post.say("Ouch", BODYLANGUAGEMODECONFIG)
            animatedSpeech.wait(id, 0)
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))
            
        # todo: start NAO moving to current ball.y position, use post

        #print "ball.x: {}, x: {}, ball.y: {}, y: {}".format(self.ball.x, self.x, self.ball.y, self.y)
            
    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.playerNAO.center_y = touch.y
        
            
class NAOPongApp(App):
    def build(self):

        game = NAOPongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        
        restartButton = Button(text = 'Restart!', center_x = game.width * 7, background_color = (1, 1, 1, 0.5))
        
        game.add_widget(restartButton)

        def restart_game(obj):
            print "restart"
            game.player1.score = 0
            game.playerNAO.score = 0
            game.serve_ball()

        restartButton.bind(on_release = restart_game)
        
        return game


def NAO_setup():
    """ Setup NAO inc proxies.

    """
    # Define globals for holding proxies.
    global tts
    global animatedSpeech
    global robotMotion

    # Setup proxies.
    try:
        tts = ALProxy("ALTextToSpeech", NAO_IP, 9559)
    except Exception, e:
        print "Could not setup tts, error: ", e
    try:
        animatedSpeech = ALProxy("ALAnimatedSpeech", NAO_IP, 9559)
    except Exception, e:
        print "Could not setup animatedSpeech, error: ", e
    try:
        robotMotion = ALProxy("ALMotion", NAO_IP, 9559)
    except Exception, e:
        print "Could not setup robotMotion, error: ", e

    # Wake NAO up.
    robotMotion.wakeUp()

def NAO_instructions():
    """ Provides game instructions.

    """
    global animatedSpeech

    id = animatedSpeech.post.say("We are going to play ping pong. I play on the right, you play on the left.", BODYLANGUAGEMODECONFIG)
    animatedSpeech.wait(id, 0)
    sleep(1.0)

def main():
    NAO_setup()
    # NAO_instructions()
    NAOPongApp().run()
    
if __name__ == "__main__":
    main()