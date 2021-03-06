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
import almath
import motion

from naoqi import ALProxy


NAO_IP = "mistcalf.local"
# Setup animatedSpeech.
BODYLANGUAGEMODECONFIG = {"bodyLanguageMode" : "contextual"}

tts = None
animatedSpeech = None
motionProxy = None
postureProxy = None
memoryProxy = None


class NAOPongPaddle(Widget):
    score = NumericProperty(0)

    sound1 = SoundLoader.load('Sounds/bipReco1.wav')
    sound2 = SoundLoader.load('Sounds/bipReco2.wav')

    global memoryProxy
    
    def bounce_ball(self, ball):
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

    def startwbBalancer(self):
        """ Starts the whole body balancer.

        """
        # Configure Whole Body Balancer:
        # Enable whole body balancer.
        self.iswbBalancerEnabled = True
        motionProxy.wbEnable(self.iswbBalancerEnabled)
        # Legs are constrained fixed.
        # todo: might be more fun if NAO moved about when playing, maybe too slow. Investigate.
        stateName = "Fixed"
        supportLeg = "Legs"
        motionProxy.wbFootState(stateName, supportLeg)
        # Constraint Balance Motion.
        isEnable = True
        supportLeg = "Legs"
        motionProxy.wbEnableBalanceConstraint(isEnable, supportLeg)
        
        print "wbBalancerEnabled after start: ", self.iswbBalancerEnabled

        

    def stopwbBalancer(self):
        """ Stop the whole body balancer.

        """
        # Deactivate whole body
        self.iswbBalancerEnabled = False
        motionProxy.wbEnable(self.iswbBalancerEnabled)

        print "wbBalancerEnabled after stop: ", self.iswbBalancerEnabled

    def getCurrentTransform(self):
        """ Gets the current position transform for left and right arms.

        """
        # Go to known position. Stand up.
        postureProxy.goToPosture("StandInit", 0.5)

        # Get the robot position transforms in a known position.
        arm = "LArm"
        frame = motion.FRAME_WORLD
        useSensorValues = False
        self.currentTfLeft = motionProxy.getTransform(arm, frame, useSensorValues)

        arm = "RArm"
        self.currentTfRight = motionProxy.getTransform(arm, frame, useSensorValues)

        print "Got new body position transform."



    def move_NAO(self, ball, court_y):
        """ NAO moves to try and meet the ball in y plane.

        """

        print "isBallInPlay, move_NAO: ", memoryProxy.getData("isBallInPlay")
        # print "ball.x {} ball.y {} bounce_ball: ".format(ball.x, ball.y)
        
        if memoryProxy.getData("isBallInPlay"):
            if not self.iswbBalancerEnabled:
                self.startwbBalancer()
                
                print "Started wbBalancer"

            
            # useSensorValues = False

            # Decide which arm to hit ball with. If ball on left of field use left arm, etc.
            # todo: only do a swing once when ball close enough using ball.x or ball velocity
            # todo: if ball on far side of court then do a waiting dance.            
            if ball.y < court_y / 2:
                # print "left"
                effectorList = ["LArm", "RArm"]
                armHitter = "LArm"
                armBalancer = "RArm"
                yAxisDirection = 1
                # self.currentTf = list(self.currentTfLeft)
            else:
                # print "right"
                effectorList = ["RArm", "LArm"]
                armHitter = "RArm"
                armBalancer = "LArm"
                yAxisDirection = -1
                # self.currentTf = list(self.currentTfRight)

            frame = motion.FRAME_WORLD
            useSensorValues = False
            pathArmHitter = []
            pathArmBalancer = []

            currentTf = motionProxy.getTransform(armHitter, frame, useSensorValues)

            # 1 - Hitting arm ready out front
            target1Tf = almath.Transform(currentTf)
            target1Tf.r1_c4 += 0.05 # x
            target1Tf.r2_c4 += 0.00 * yAxisDirection # y
            target1Tf.r3_c4 += 0.00 # z

            # 2 - Hitting arm back
            target2Tf = almath.Transform(currentTf)
            target2Tf.r1_c4 += 0.00
            target2Tf.r2_c4 += 0.15 * yAxisDirection
            target2Tf.r3_c4 += 0.15

            # 3 - Hitting arm to ball using ball.y
            target3Tf = almath.Transform(currentTf)
            target3Tf.r1_c4 += 0.05
            target3Tf.r2_c4 += 0.00 * yAxisDirection
            target3Tf.r3_c4 += 0.10

            pathArmHitter.append(list(target1Tf.toVector()))
            pathArmHitter.append(list(target2Tf.toVector()))
            pathArmHitter.append(list(target3Tf.toVector()))

            currentTf = motionProxy.getTransform(armBalancer, frame, useSensorValues)

            # 1 - Balancing arm ready out front
            target1Tf = almath.Transform(currentTf)
            target1Tf.r1_c4 += 0.05
            target1Tf.r2_c4 += 0.00 * yAxisDirection
            target1Tf.r3_c4 += 0.00

            # 2 - Balancing arm back
            target2Tf = almath.Transform(currentTf)
            target2Tf.r1_c4 += 0.00
            target2Tf.r2_c4 += 0.00 * yAxisDirection
            target2Tf.r3_c4 += 0.00

            # 3 - Balancing arm return to front
            target3Tf = almath.Transform(currentTf)
            target3Tf.r1_c4 += 0.05
            target3Tf.r2_c4 += 0.00 * yAxisDirection
            target3Tf.r3_c4 += 0.00

            pathArmBalancer.append(list(target1Tf.toVector()))
            pathArmBalancer.append(list(target2Tf.toVector()))
            pathArmBalancer.append(list(target3Tf.toVector()))

            pathList = [pathArmHitter, pathArmBalancer]

            axisMaskList = [almath.AXIS_MASK_VEL, # For hitting arm.
                            almath.AXIS_MASK_VEL] # For balancing arm.

            coef = 1.5
            timesList = [[coef * (i + 1) for i in range(len(pathArmHitter))], 
                        [coef * (i + 1) for i in range(len(pathArmBalancer))]]

            # And move!
            # try:
            #     id = motionProxy.post.transformInterpolations(effectorList, frame, pathList, axisMaskList, timesList)
            #     motionProxy.wait(id, 0)
            # except:
            #     pass

            # todo: move
            # print "moving ..... ball.y: {} ball.isBallInPlay: {}".format(ball.y, ball.isBallInPlay)

        else:
            self.stopwbBalancer()
            print "Stopped wbBalancer"
        
            
            

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

    global memoryProxy
        
    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = Vector(4, 0).rotate(randint(0, 360))
        memoryProxy.insertData("isBallInPlay", True)
        print "isBallInPlay, serve: ", memoryProxy.getData("isBallInPlay")
        print "SERVED!"
    
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
            memoryProxy.insertData("isBallInPlay", False)
            print "isBallInPlay, update: ", memoryProxy.getData("isBallInPlay")
            
            id = animatedSpeech.post.say("I win!", BODYLANGUAGEMODECONFIG)
            animatedSpeech.wait(id, 0)
            self.playerNAO.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.x > self.width:
            memoryProxy.insertData("isBallInPlay", False)
            print "isBallInPlay, update: ", memoryProxy.getData("isBallInPlay")
            
            id = animatedSpeech.post.say("Ouch", BODYLANGUAGEMODECONFIG)
            animatedSpeech.wait(id, 0)
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))
            
    def nao_update(self, dt):
        """ Update method for NAO to allow seperate control of NAO from game.

        """
        # todo: start NAO moving to current ball.y position, use post
        self.playerNAO.move_NAO(self.ball, self.height)

        # print "ball.x: {}, height: {}, ball.y: {}, width: {}".format(self.ball.x, self.height, self.ball.y, self.width)
            
    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.playerNAO.center_y = touch.y
        
            
class NAOPongApp(App):
    def build(self):

        nao_update_dt = 1.0/60.0

        game = NAOPongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        Clock.schedule_interval(game.nao_update, nao_update_dt)
        
        # restart button
        restartButton = Button(text = 'Restart!', center_x = game.width * 7, background_color = (1, 1, 1, 0.5))
        
        game.add_widget(restartButton)

        def restart_game(obj):
            print "restart"
            game.player1.score = 0
            game.playerNAO.score = 0
            game.serve_ball()

        restartButton.bind(on_release = restart_game)

        # stop game button
        stopButton = Button(text = 'Stop!', center_x = game.width * 2, background_color = (1, 1, 1, 0.5))
        game.add_widget(stopButton)

        def stop_game(obj):
            print "stop"
            try:
                NAOPongApp().stop()
            except Exception, e:
                print "Stopping error: ", e
            sleep(0.5)
            memoryProxy.insertData("isBallInPlay", False)
            game.playerNAO.stopwbBalancer()
            id = animatedSpeech.post.say("Bye bye", BODYLANGUAGEMODECONFIG)
            animatedSpeech.wait(id, 0)
            

        stopButton.bind(on_release = stop_game)
        
        return game


def NAO_setup():
    """ Setup NAO inc proxies.

    """
    # Define globals for holding proxies.
    global tts
    global animatedSpeech
    global motionProxy
    global postureProxy
    global memoryProxy

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
        motionProxy = ALProxy("ALMotion", NAO_IP, 9559)
    except Exception, e:
        print "Could not setup motionProxy, error: ", e
    try:
        postureProxy = ALProxy("ALRobotPosture", NAO_IP, 9559)
    except Exception, e:
        print "Could not setup postureProxy, error: ", e
    try:
        memoryProxy = ALProxy("ALMemory", NAO_IP, 9559)
    except Exception, e:
        print "Could not setup memoryProxy, error: ", e

    # Wake NAO up.
    motionProxy.wakeUp()

    # Stand up.
    postureProxy.goToPosture("StandInit", 0.5)

    # Default state for isBallInPlay
    memoryProxy.insertData("isBallInPlay", False)


     

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