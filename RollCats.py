#!/usr/bin/python

#==================================================================

#                             RollCats activity

#==================================================================
global lvl

import pygame
from pygame.locals import *
from pygame.color import *
import box2d
from math import *
import random
from level_specs_test import *
#import level_specs_test

global SCENERY
global ROLLCAT_WHEEL
global ROLLCAT_BODY
global ROLLCAT_WIN_SENSOR
global BRIDGE
global BRIDGE_SWITCH
global LAUNCHER
(SCENERY, ROLLCAT_WHEEL, ROLLCAT_BODY, ROLLCAT_JUMP_SENSOR, ROLLCAT_WIN_SENSOR, BRIDGE, BRIDGE_SWITCH, LAUNCHER) = (0,1,2,3,4,5,6,7)

global BG_COLOR
BG_COLOR = (80, 80, 255)

global winSoundFile
winSoundFile = 'win.wav'
global loseSoundFile
loseSoundFile = 'lose.wav'
global hissSoundFile
hissSoundFile = 'hiss.wav'
global drawbridgeSoundFile
drawbridgeSoundFile = 'drawbridge.wav'

global currentLevel
currentLevel = 0

class X2OGame: 
    contactList = []
    waitTime = 70
    loseHeight = -40

    def __init__(self, screen):
        X2OGame.game = self
        self.pixelsPerMeter = 20
        
        self.screen = screen
        # get everything set up
        self.clock = pygame.time.Clock()
        #self.font = pygame.font.Font(None, 24) # font object
        #self.canvas = olpcgames.ACTIVITY.canvas
        #self.joystickobject = None
        self.debug = True
        self.init()
        global currentLevel
        currentLevel = 0
        loadLevel(currentLevel)
        
#        X2OGame.game.humSound.play(-1)
    
    def init(self):
        self.initializeWorld()
        self.screen.fill(BG_COLOR)
        
        self.updateList = []
        pygame.display.flip()
        
        self.leftLPress = False
        self.leftRPress = False
        self.leftJump = False
        self.rightLPress = False
        self.rightRPress = False
        self.rightJump = False
        
        self.winSound = loadSound(winSoundFile)
        self.loseSound = loadSound(loseSoundFile)
        self.hissSound = loadSound(hissSoundFile)
        self.drawbridgeSound = loadSound(drawbridgeSoundFile)
#        self.startupSound = loadSound('startup.wav')
#        self.humSound = loadSound('hum.wav')
#        self.accelSound = loadSound('accel2.wav')
        self.meowSound = loadSound('meow.wav')
        
        
        # create the name --> instance map for components

    def worldToScreen(self, worldX, worldY):
        return (worldX * self.pixelsPerMeter, - worldY * self.pixelsPerMeter)

    def screenToWorld(self, screenX, screenY):
        return (screenX / self.pixelsPerMeter, - screenY / self.pixelsPerMeter)
        
    def initializeWorld(self):
        global contactList
        contactList = []
        worldAABB = box2d.b2AABB()
        worldAABB.lowerBound.Set(- 100, - 100)
        worldAABB.upperBound.Set(100, 100)
        gravity = box2d.b2Vec2(0, - 10)
        doSleep = True
        self.world = box2d.b2World(worldAABB, gravity, doSleep)
        self.levelSwitchCountingDown = False
        self.levelSwitchCounter = 0

        # make sun
        BodySprite(self.world.GetGroundBody(), 'Rollcats_Sun.png', 20, 20, -10, -10, self.worldToScreen, self.screenToWorld)

        self.contactListener = myContactListener()
        self.world.SetContactListener(self.contactListener)
#        createScenery(self,self.world)
#        switch = BridgeAndSwitch((30,-25), (35,-26), False)
#        self.updateList.append(switch)

    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    self.running = False
                if (event.type == KEYDOWN and (event.key == K_a or event.key == K_KP4)):
                    self.leftLPress = True
                if (event.type == KEYUP and (event.key == K_a or event.key == K_KP4)):
                    self.leftLPress = False
                if (event.type == KEYDOWN and (event.key == K_d or event.key == K_KP6)):
                    self.leftRPress = True
                if (event.type == KEYUP and (event.key == K_d or event.key == K_KP6)):
                    self.leftRPress = False
                if (event.type == KEYDOWN and (event.key == K_w or event.key == K_KP8)):
                    self.leftJump = True
                if (event.type == KEYUP and (event.key == K_w or event.key == K_KP8)):
                    self.leftJump = False
                if (event.type == KEYDOWN and (event.key == K_LEFT or event.key == K_KP7)):
                    self.rightLPress = True
                if (event.type == KEYUP and (event.key == K_LEFT or event.key == K_KP7)):
                    self.rightLPress = False
                if (event.type == KEYDOWN and (event.key == K_RIGHT or event.key == K_KP1)):
                    self.rightRPress = True
                if (event.type == KEYUP and (event.key == K_RIGHT or event.key == K_KP1)):
                    self.rightRPress = False
                if (event.type == KEYDOWN and (event.key == K_UP or event.key == K_KP9)):
                    self.rightJump = True
                if (event.type == KEYUP and (event.key == K_UP or event.key == K_KP9)):
                    self.rightJump = False                
                #self.currentTool.handleEvents(event)
            # Clear Display
            #self.screen.fill((0,0,0)) #255 for white
            
            if self.levelSwitchCountingDown:
                self.levelSwitchCounter -= 1
                if self.levelSwitchCounter == 0:
                    self.levelSwitchCountingDown = 0
                    loadLevel(currentLevel)
            
            X2OGame.contactList = []
            self.world.Step(1.0/60,10)
            for updatable in self.updateList:
                updatable.update()
            self.leftCat.update(self.leftLPress, self.leftRPress, self.leftJump)
            self.rightCat.update(self.rightLPress, self.rightRPress, self.rightJump)            
            self.winCheck()

            X2OGame.contactList = []
            self.world.Step(1.0/60,10)
            for updatable in self.updateList:
                updatable.update()
            self.leftCat.update(self.leftLPress, self.leftRPress, self.leftJump)
            self.rightCat.update(self.rightLPress, self.rightRPress, self.rightJump)
            self.winCheck()
            
            X2OGame.contactList = []
            self.world.Step(1.0/60,10)
            for updatable in self.updateList:
                updatable.update()
            self.leftCat.update(self.leftLPress, self.leftRPress, self.leftJump)
            self.rightCat.update(self.rightLPress, self.rightRPress, self.rightJump)
            self.winCheck()
            
            self.loseCheck()
            
            #Print all the text on the screen
            #text = self.font.render("Current Tool: "+self.currentTool.name, True, (0,0,0))
            #textpos = text.get_rect(left=700,top=7)
            #self.screen.blit(text,textpos)  
            
            for char in BodySprite.bodySpriteList:
                char.update()
            for char in BodySprite.bodySpriteList:
                self.screen.blit(char.blank, char.old)
            for char in BodySprite.bodySpriteList:
                self.screen.blit(char.image, char.rect)
            #for char in BodySprite.bodySpriteList:
            displayList = []
            for char in BodySprite.bodySpriteList:
                displayList.append(char.rect)
                displayList.append(char.old)#[char.old, char.rect])    
            pygame.display.update(displayList)#[char.old, char.rect])
       
            # Flip Display
            #pygame.display.flip()  
            
            # Try to stay at 30 FPS
            self.clock.tick(24) # originally 50
#            print self.clock.get_fps()
    
    def restartLevel(self):
        loadLevel(currentLevel)
    
    def winCheck(self):
        if self.levelSwitchCountingDown:
            return
        for pair in X2OGame.contactList:
            shape1 = pair[0]
            shape2 = pair[1]
            if (shape1.GetUserData() == ROLLCAT_WIN_SENSOR and shape2.GetUserData() == ROLLCAT_WIN_SENSOR):
                self.winSound.play()
                self.startLevelSwitch()
                
    def loseCheck(self):
        if self.levelSwitchCountingDown:
            return
        if self.leftCat.torso.GetWorldCenter().y < X2OGame.loseHeight or self.rightCat.torso.GetWorldCenter().y < X2OGame.loseHeight:
            self.loseSound.play()
            self.restartLevel()
            
                
    def startLevelSwitch(self):
        if self.levelSwitchCountingDown:
            return
        global currentLevel
        currentLevel += 1
        if currentLevel > len(lvl._list)-1:
            currentLevel = 0
        self.levelSwitchCountingDown = True
        self.levelSwitchCounter = X2OGame.waitTime
        


class BodySprite(pygame.sprite.Sprite):
   blankColor = BG_COLOR
   bodySpriteList = []

   def __init__(self, body, imageName, imageWidthMeters, imageHeightMeters, imageOffsetXMeters, imageOffsetYMeters, worldToScreenFunction, screenToWorldFunction):

      pygame.sprite.Sprite.__init__(self)

      BodySprite.bodySpriteList.append(self)
      
      # Save a copy of the screen's rectangle
      self.screen = pygame.display.get_surface().get_rect()
      
      self.w2s = worldToScreenFunction
      self.s2w = screenToWorldFunction
      
      self.body = body
      
      newWidth = self.w2s(imageWidthMeters, imageHeightMeters)[0] - self.w2s(0, 0)[0]
      newHeight = self.w2s(imageWidthMeters, imageHeightMeters)[1] - self.w2s(0, 0)[1]
      
      self.offsetX = imageOffsetXMeters
      self.offsetY = imageOffsetYMeters
      
      if newWidth < 0:
          newWidth *= - 1
      if newHeight < 0:
          newHeight *= - 1

      # Create a variable to store the previous position of the sprite
      self.old = (0, 0, 0, 0)
      
      self.angle = 0

      self.originalImage = pygame.transform.scale(pygame.image.load(imageName).convert_alpha(), (newWidth, newHeight))
#      self.originalImage = self.originalImage.
#      self.originalImage.set_colorkey((0,0,0),pygame.RLEACCEL)
      self.image = pygame.transform.rotate(self.originalImage, self.angle)
      self.rect = self.image.get_rect()

      # Create a Surface the size of our character
      #bigSize = max(self.rect.width, self.rect.height)
      self.blank = pygame.Surface((self.rect.width * 2, self.rect.height * 2), 0, self.screen)
      self.blank.fill(BodySprite.blankColor)
      self.alreadyRendered = False
      # self.

   def update(self):

      if ((self.body.IsStatic() or self.body.IsSleeping()) and self.alreadyRendered):
          return
      
      self.alreadyRendered = True
      # Make a copy of the current rectangle for use in erasing
      self.old = self.rect
      
      
      angle = self.body.GetAngle()
      self.image = pygame.transform.rotate(self.originalImage, angle * 180 / 3.1415)
      
      # Move the rectangle by the specified amount
      self.rect = self.image.get_rect()
      
      cosAngle = cos(- angle)
      sinAngle = sin(- angle)
      
      vrotx = - (cosAngle * self.offsetX - sinAngle * self.offsetY)
      vroty = (sinAngle * self.offsetX + cosAngle * self.offsetY)

      (self.x, self.y) = self.w2s(self.body.GetXForm().position.x + vrotx, self.body.GetXForm().position.y + vroty)
      
      self.rect.center = (self.x, self.y)
      
def convertToFlipY( coord ):
    return ( coord[0], 800 - coord[1] )
       
class myContactListener(box2d.b2ContactListener):
    def __init__(self): super(myContactListener, self).__init__() 
    def Add(self, point):
        pass
    def Persist(self, point):
        #print point
        #if (point.shape1.GetBody().type == ROLLCAT_BODY or point.shape2.GetBody().type == ROLLCAT_BODY):
        X2OGame.contactList.append((point.shape1,point.shape2))
    def Remove(self, point):
        pass
    def Result(self, point):
        pass
        
def loadLevel(levelNumber):
    X2OGame.contactList = []
    BodySprite.bodySpriteList = []
    X2OGame.game.init()
    pic = 'Rollcats_Grass.png'
    vertexList = []
    heightField = lvl.return_height_fields(levelNumber)
    for i in range(0, len(heightField)):
        loc = X2OGame.game.screenToWorld(heightField[i][0], 800-heightField[i][1])
        vertexList.append(loc)
    createGround(X2OGame.game, X2OGame.game.world, vertexList, 0.6, 'Rollcats_Grass.png')
    scenery = lvl.return_scenery(levelNumber)
    cloudW = 15
    cloudH = 10
    for obj in scenery:
        cloudPic = obj['img_url']
        cloudLocScreen = obj['pos']
        cloudLoc = X2OGame.game.screenToWorld(cloudLocScreen[0], 800-cloudLocScreen[1])
        BodySprite(X2OGame.game.world.GetGroundBody(),cloudPic,cloudW, cloudH, -cloudLoc[0], cloudLoc[1],X2OGame.game.worldToScreen, X2OGame.game.screenToWorld)
        
    sunBubbleLoc = X2OGame.game.screenToWorld(587, 800-739)
    sunBubblePic = 'level'+repr(levelNumber+1)+'_hint.png'
    sunBubbleW = 20
    sunBubbleH = 7
    BodySprite(X2OGame.game.world.GetGroundBody(),sunBubblePic,sunBubbleW, sunBubbleH, -sunBubbleLoc[0], sunBubbleLoc[1],X2OGame.game.worldToScreen, X2OGame.game.screenToWorld)
        
    bridges = lvl.return_bridges(levelNumber)
    for obj in bridges:
        #bridgePic = obj[0]['img_url']
        bridgeLocRaw = obj[0]['pos']
        bridgeLoc = X2OGame.game.screenToWorld(bridgeLocRaw[0], 800-bridgeLocRaw[1])
        #switchPic
        switchLocRaw = obj[1]['pos']
        switchLoc = X2OGame.game.screenToWorld(switchLocRaw[0], 800-bridgeLocRaw[1])
        orientation = obj[0]['fallsLeft']
        X2OGame.game.updateList.append(BridgeAndSwitch(bridgeLoc, switchLoc, orientation))
    
    vertexList = [ X2OGame.game.screenToWorld(-10,0), X2OGame.game.screenToWorld(-10,800) ]
    createGround(X2OGame.game, X2OGame.game.world, vertexList, 0.3, 'Rollcats_Grass.png')
    vertexList = [ X2OGame.game.screenToWorld(1230,0), X2OGame.game.screenToWorld(1230,800) ]
    createGround(X2OGame.game, X2OGame.game.world, vertexList, 0.3, 'Rollcats_Grass.png')
    
    if currentLevel == 3:
        X2OGame.game.updateList.append(Launcher(X2OGame.game.screenToWorld(422,800-180),True))
    
    X2OGame.game.leftCat = RollCat(X2OGame.game,(5,-20),'Rollcats_bottom.png','Rollcats_top.png')
    X2OGame.game.rightCat = RollCat(X2OGame.game,(55,-20),'Rollcats_bottom_inverted.png','Rollcats_top_inverted.png')
    
#    X2OGame.game.startupSound.play()
    
def createScenery(game, world):
    pic = 'Rollcats_Grass.png'
    vertexList = []     #[ (0,-16), (5,-18), (10,-18), (16,-17), (20,-18), (25,-15) ]
    lastY = 600
    for i in range(0,10):
        lastY += random.uniform(-20,19)
        locScreen = ( i * 1200 / 10, lastY )
        loc = X2OGame.game.screenToWorld(locScreen[0], locScreen[1])
        vertexList.append( loc )
    createGround(game, world, vertexList, 0.6, pic)

def createGround(game, world, vertexList, thickness, pic):
    list = []
    for i in range(0, len(vertexList)-1):
        va = vertexList[i]
        vb = vertexList[i+1]
        dx = vb[0]-va[0]
        dy = vb[1]-va[1]
        angle = atan2(dy,dx)
        distSqr = dx*dx + dy*dy
        dist = sqrt(distSqr)
        bodyDef = box2d.b2BodyDef()
        bodyDef.position.Set((va[0]+vb[0])*.5, (va[1]+vb[1])*.5)
        body = world.CreateBody(bodyDef)

        shapeDef = box2d.b2PolygonDef()
        shapeDef.SetAsBox(dist*.5, thickness*.5)
        shape = body.CreateShape(shapeDef)
        shape.SetUserData(SCENERY)
        body.SetXForm(body.GetXForm().position,angle)
        BodySprite(body,pic,dist,thickness*3,0,0,game.worldToScreen, game.screenToWorld)
        body.SetUserData(SCENERY)
        list.append( body)
    return list
    
class Launcher:
    launcherLength = 10
    launcherThickness = 1.0
    launcherPicLoc = 'Drawbridge.png'
    
    launchThreshold = 1000
    launchImpulse = 400
    
    def __init__(self, hingeLoc, opensLeft):
        self.resetTimer = 0
        bodyDef = box2d.b2BodyDef()
        endX = hingeLoc[0] + Launcher.launcherLength
        if opensLeft:
            endX = hingeLoc[0] - Launcher.launcherLength
        bodyDef.position.Set( (hingeLoc[0]+endX) * .5, hingeLoc[1] )
        self.launcherBody = X2OGame.game.world.CreateBody(bodyDef)
        self.launcherBody.SetUserData(LAUNCHER)
        self.opensLeft = opensLeft
        
        shapeDef = box2d.b2PolygonDef()
        shapeDef.SetAsBox(Launcher.launcherLength*.5, Launcher.launcherThickness*.5)
        shapeDef.density = 1.0
        shape = self.launcherBody.CreateShape(shapeDef)
        self.launcherBody.SetMassFromShapes()
        shape.SetUserData(LAUNCHER)
        
        rjd = box2d.b2RevoluteJointDef()
        rjd.Initialize(self.launcherBody, X2OGame.game.world.GetGroundBody(), box2d.b2Vec2(hingeLoc[0],hingeLoc[1]))
        rjd.enableLimit = True
        rjd.lowerAngle = -3.1415 * .333
        rjd.upperAngle = 0
        
        if opensLeft:        
            rjd.lowerAngle = 0
            rjd.upperAngle = 3.1415 * .333

        
        self.hingeJoint = X2OGame.game.world.CreateJoint(rjd)
        
        BodySprite(self.launcherBody,Launcher.launcherPicLoc,Launcher.launcherLength,Launcher.launcherThickness,0,0,X2OGame.game.worldToScreen,X2OGame.game.screenToWorld)
        
    
    def update(self):
        if self.resetTimer > 0:
            self.resetTimer -= 1
            #print self.resetTimer
            return
        torque = -self.hingeJoint.GetReactionTorque()
#        print torque
        if self.opensLeft:
            torque *= -1
        if (torque > Launcher.launchThreshold):
            self.launcherBody.ApplyImpulse( box2d.b2Vec2(0.0, Launcher.launchImpulse), self.launcherBody.GetWorldCenter())
            self.resetTimer = 240
            X2OGame.game.hissSound.play()
            
            
            
class BridgeAndSwitch:
    bridgeLength = 15
    bridgeThickness = 1.0
    bridgePicLoc = 'Drawbridge.png'
    
    
    switchThickness = 0.4
    switchLength = 2.0
    switchPicLoc = 'Lever_lever.png'
    
    baseWidth = 2.0
    baseHeight = 1.0
    basePicLoc = 'Lever_base.png'
    
    switchThreshold = 50
    
    def __init__(self, bridgeLoc, switchLoc, fallsLeft):
        self.isSwitchHit = False
        # create bridge
        bodyDef = box2d.b2BodyDef()
        bodyDef.position.Set( bridgeLoc[0], bridgeLoc[1] + BridgeAndSwitch.bridgeLength * .5 )
        self.bridgeBody = X2OGame.game.world.CreateBody(bodyDef)
        self.bridgeBody.SetUserData(BRIDGE)
        self.fallsLeft = fallsLeft
        
        shapeDef = box2d.b2PolygonDef()
        shapeDef.SetAsBox(BridgeAndSwitch.bridgeThickness*.5, BridgeAndSwitch.bridgeLength*.5)
        shapeDef.density = 1.0
        shape = self.bridgeBody.CreateShape(shapeDef)
        self.bridgeBody.SetMassFromShapes()
        shape.SetUserData(BRIDGE)
        
        rjd = box2d.b2RevoluteJointDef()
        rjd.Initialize(self.bridgeBody, X2OGame.game.world.GetGroundBody(), box2d.b2Vec2(bridgeLoc[0],bridgeLoc[1]))
        rjd.enableLimit = True
        rjd.lowerAngle = -.05
        rjd.upperAngle = .05
        rjd.collideConnected = True
        
        self.bridgeJoint = X2OGame.game.world.CreateJoint(rjd)
        
        bodyDef2 = box2d.b2BodyDef()
        bodyDef2.position.Set( switchLoc[0], switchLoc[1] + BridgeAndSwitch.switchLength*.5 )
        self.switchBody = X2OGame.game.world.CreateBody(bodyDef2)
        self.switchBody.SetUserData(BRIDGE_SWITCH)
        
        shapeDef2 = box2d.b2PolygonDef()
        shapeDef2.SetAsBox(BridgeAndSwitch.switchThickness*.5, BridgeAndSwitch.switchLength*.5)
        shapeDef2.density = 5.0
        shape2 = self.switchBody.CreateShape(shapeDef2)
        self.switchBody.SetMassFromShapes()
        shape2.SetUserData(BRIDGE_SWITCH)
        
        rjd2 = box2d.b2RevoluteJointDef()
        rjd2.Initialize(self.switchBody, X2OGame.game.world.GetGroundBody(), box2d.b2Vec2(switchLoc[0],switchLoc[1]))
        rjd2.enableLimit = True
        rjd2.lowerAngle = -.02
        rjd2.upperAngle = .02
        rjd2.collideConnected = True
        
        self.switchJoint = X2OGame.game.world.CreateJoint(rjd2)
        BodySprite(self.bridgeBody,BridgeAndSwitch.bridgePicLoc,BridgeAndSwitch.bridgeThickness,BridgeAndSwitch.bridgeLength,0,0,X2OGame.game.worldToScreen,X2OGame.game.screenToWorld)
        BodySprite(self.switchBody,BridgeAndSwitch.switchPicLoc,BridgeAndSwitch.switchThickness,BridgeAndSwitch.switchLength,0,0,X2OGame.game.worldToScreen,X2OGame.game.screenToWorld)
        BodySprite(X2OGame.game.world.GetGroundBody(), BridgeAndSwitch.basePicLoc, BridgeAndSwitch.baseWidth, BridgeAndSwitch.baseHeight, -switchLoc[0], switchLoc[1],X2OGame.game.worldToScreen,X2OGame.game.screenToWorld)
        
        
    def update(self):
        if self.isSwitchHit:
            return
        force = self.switchJoint.GetReactionForce().Normalize()
        if (force > BridgeAndSwitch.switchThreshold):
            self.switchJoint.getAsType().SetLimits(-.4, .4)
            self.release()
        
    def release(self):
        self.isSwitchHit = True
        X2OGame.game.drawbridgeSound.play()
        if self.fallsLeft:
            self.bridgeJoint.getAsType().SetLimits(-3.1415 / 2, 0.1)
            self.bridgeBody.ApplyImpulse(box2d.b2Vec2(-10.0,0),self.bridgeBody.GetWorldCenter())
        else:
            self.bridgeJoint.getAsType().SetLimits(-0.1, 3.1415 / 2)
            self.bridgeBody.ApplyImpulse(box2d.b2Vec2(10.0,0),self.bridgeBody.GetWorldCenter())            
        
        
class RollCat:
    # Must touch ground, then not be pressing jump, then you're ready to jump
    NO_GROUND_TOUCH = 0
    NO_KEY_RELEASE = 1
    READY_TO_JUMP = 2
    
    initialJumpTimer = 5
    
    def __init__(self, game, location, bottomGraphicFile, topGraphicFile):
        self.jumpTimer = RollCat.initialJumpTimer
        self.game = game
        self.world = game.world
        self.cachedOnGround = False
        
        self.jumpState = RollCat.NO_GROUND_TOUCH
        
        bodyDef = box2d.b2BodyDef()
        bodyDef.position.Set(location[0], location[1]+1)
        #bodyDef.fixedRotation = True
        body = self.world.CreateBody(bodyDef)
        shapeDef = box2d.b2PolygonDef()
        shapeDef.SetAsBox(1, 1)
        shapeDef.density = 1
        shapeDef.restitution = 0.3
        shapeDef.friction = 1.0
        shape = body.CreateShape(shapeDef)
        shape.SetUserData(-1)
        body.SetMassFromShapes()
        self.torso = body
        self.torso.SetUserData(ROLLCAT_BODY)


        bodyDef3 = box2d.b2BodyDef()
        bodyDef3.position.Set(location[0],location[1])
        body3 = self.world.CreateBody(bodyDef3)

        shapeDef3 = box2d.b2CircleDef()
        shapeDef3.radius = 0.95
        shapeDef3.density = 1
        shapeDef3.restitution = 0.1
        shapeDef3.friction = 3.0
        shape3 = body3.CreateShape(shapeDef3)
        shape3.SetUserData(-1) #don't need
        body3.SetMassFromShapes()
        self.wheel = body3
        self.wheel.SetUserData(ROLLCAT_WHEEL)
        
        sensorDef = box2d.b2CircleDef()
        sensorDef.radius = 0.9
        sensorDef.isSensor = True
        sensorDef.localPosition = box2d.b2Vec2(0,-1.1)
        sensorShape = self.torso.CreateShape(sensorDef)
        sensorShape.SetUserData(ROLLCAT_JUMP_SENSOR)
        
        sensorDef2 = box2d.b2PolygonDef()
        sensorDef2.SetAsBox(1.1,1.6,box2d.b2Vec2(0,.5),0)
        sensorDef2.isSensor = True
        sensorShape2 = self.torso.CreateShape(sensorDef2)
        sensorShape2.SetUserData(ROLLCAT_WIN_SENSOR) 
        
        jd = box2d.b2RevoluteJointDef()
        jd.Initialize(body, body3, box2d.b2Vec2(location[0],location[1]))
        revJoint = self.world.CreateJoint(jd).getAsType()
        self.axle = revJoint
        
        revJoint.EnableMotor(True)
        revJoint.SetMotorSpeed(0)
        revJoint.SetMaxMotorTorque(4000)
        self.motorSpeed = 0
        
        self.targetAngle = 0
        
        BodySprite(body3,bottomGraphicFile,2, 2, 0, 0, self.game.worldToScreen, self.game.screenToWorld)
        BodySprite(body,topGraphicFile,2, 2, 0, 0,self.game.worldToScreen, self.game.screenToWorld)
        
    def canJump(self):
        if (self.cachedOnGround and self.jumpState == RollCat.READY_TO_JUMP):
            return True
        return False
        
    def onGround(self):
        for pair in X2OGame.contactList:
            body1 = pair[0].GetBody()
            body2 = pair[1].GetBody()
            if (body1 == self.torso and body2.GetUserData() != ROLLCAT_WHEEL or body2 == self.torso and body1.GetUserData() != ROLLCAT_WHEEL):
                if ( (pair[0].GetUserData() == ROLLCAT_JUMP_SENSOR and body1 == self.torso) or (pair[1].GetUserData() == ROLLCAT_JUMP_SENSOR and body2 == self.torso)):
                #if (pair[0].IsSensor() or pair[1].IsSensor()):
                    #print "got here"
                    self.cachedOnGround = True
                    return True
        self.cachedOnGround = False
        return False
        
    def update(self, keyL, keyR, keyJ):
        self.onGround()
        cj = self.canJump()
        if (self.jumpState == RollCat.NO_GROUND_TOUCH and self.cachedOnGround):
            self.jumpState = RollCat.NO_KEY_RELEASE
        elif (keyJ == False):
            self.jumpState = RollCat.READY_TO_JUMP
        jumpImpulse = 70
        moveSpeed = .1
        moveForce = 100
        angle = self.torso.GetAngle() - self.targetAngle
        angVel = self.torso.GetAngularVelocity()
        if (keyL):
            self.targetAngle = .95*self.targetAngle + .05 * .4
#            X2OGame.game.accelSound.play()
            if cj:
                self.wheel.ApplyForce(box2d.b2Vec2(-moveForce,0),self.wheel.GetWorldCenter())
            else:
                self.torso.ApplyForce(box2d.b2Vec2(-moveForce*.4,0),self.torso.GetWorldCenter())
            
        elif (keyR):
            self.targetAngle = .95*self.targetAngle - .05 * .4
#            X2OGame.game.accelSound.play()
            if cj:
                self.wheel.ApplyForce(box2d.b2Vec2(moveForce,0),self.wheel.GetWorldCenter())
            else:
                self.torso.ApplyForce(box2d.b2Vec2(moveForce*.4,0),self.torso.GetWorldCenter())
        else:
            vx = self.wheel.GetLinearVelocity().x
            self.targetAngle = .9*self.targetAngle
            if cj:
                self.wheel.ApplyForce(box2d.b2Vec2(-.1*moveForce*vx,0),self.wheel.GetWorldCenter())
        while (angle > 3.1415):
            angle -= 2*3.1415
        while (angle < -3.1415):
            angle += 2*3.1415
        correctionFactor = 2
        correctionDragFactor = .25
        #torque = -correctionFactor*angle - correctionDragFactor*angVel
        #self.torso.ApplyTorque(torque)
        changeFactor = 1.0
        if (self.cachedOnGround == False):
            changeFactor = 0.3
        self.motorSpeed += changeFactor*(correctionFactor*angle + correctionDragFactor*angVel)
        self.axle.SetMotorSpeed(self.motorSpeed) 
        

        
        if (keyJ and cj and self.jumpState == RollCat.READY_TO_JUMP and self.jumpTimer < 0):
            self.torso.ApplyImpulse(box2d.b2Vec2(0,jumpImpulse),self.torso.GetWorldCenter())
            X2OGame.game.meowSound.play()
            self.jumpTimer = RollCat.initialJumpTimer
            self.jumpState = RollCat.NO_GROUND_TOUCH
        
        self.jumpTimer -= 1

def main():
    global lvl
    lvl = initializeLevels()
    pygame.init()
    pygame.display.init()
    x, y = (1200,800)  #pygame.display.list_modes()[0]
    #toolbarheight = 10
    #tabheight = 10
    screen = pygame.display.set_mode((x, y))
    # create an instance of the game
    game = X2OGame(screen)    
    # start the main loop
    game.run()

# function for loading sounds (mostly borrowed from Pete Shinners pygame tutorial)
def loadSound(name):
    # if the mixer didn't load, then create an empy class that has an empty play method
    # this way the program will run if the mixer isn't present (sans sound)
    class NoneSound:
        def play(self): pass
        def set_volume(self): pass
    if not pygame.mixer:
        return NoneSound()
    try:
        sound = pygame.mixer.Sound(name)
    except:
        print "error with sound: " + name
        return NoneSound()
        
    return sound

# make sure that main get's called
if __name__ == '__main__':
    main()

