#!/usr/bin/python
#
# C++ version Copyright (c) 2006-2007 Erin Catto http://www.gphysics.com
# Python version Copyright (c) 2008 kne / sirkne at gmail dot com
# 
# Implemented using the pybox2d SWIG interface for Box2D (pybox2d.googlepages.com)
# 
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
# 1. The origin of this software must not be misrepresented; you must not
# claim that you wrote the original software. If you use this software
# in a product, an acknowledgment in the product documentation would be
# appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
# misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.

"""
6/1/2008
Added some much needed comments in the code (next to none in the C++ code).
Cleanups all around.

4/27/2008
pygame port. All tests now ported.

4/25/2008
Initial port of the Testbed Framework for Box2D 2.0.1
The 'fw' prefix refers to 'framework'
(Initial port was for pyglet 1.1)

Notes:
* Edit test_settings to change what's displayed. Add your own test based on test_empty.
* Reload is not working.

-kne
"""
import pygame
import Box2D2 as box2d
#import psyco # a few fps faster with psyco
from pygame.locals import *
from settings import fwSettings
from pgu import gui

class fwDestructionListener(box2d.b2DestructionListener):
    """
    The destruction listener callback:
    "SayGoodbye" is called when a joint is deleted.
    """
    test = None
    def __init__(self):
        super(fwDestructionListener, self).__init__()

    def SayGoodbye(self, joint):
        if self.test.mouseJoint:
            self.test.mouseJoint=None
        else:
            self.test.JointDestroyed(joint)

class fwBoundaryListener(box2d.b2BoundaryListener):
    """
    The boundary listener callback:
    Violation is called when the specified body leaves the world AABB.
    """
    test = None
    def __init__(self):
        super(fwBoundaryListener, self).__init__()

    def Violation(self, body):
        # So long as it's not the user-created bomb, let the test know that
        # the specific body has left the world AABB
        if self.test.bomb != body:
            self.test.BoundaryViolated(body)

class fwContactTypes:
    """
    Acts as an enum, holding the types necessary for contacts:
    Added, persisted, and removed
    """
    contactUnknown = 0
    contactAdded = 1
    contactPersisted = 2
    contactRemoved = 3

class fwContactPoint:
    """
    Structure holding the necessary information for a contact point.
    All of the information is copied from the contact listener callbacks.
    """
    shape1 = None
    shape2 = None
    normal = None
    position = None
    velocity = None
    id  = box2d.b2ContactID()
    state = 0

class fwContactListener(box2d.b2ContactListener):
    """
    Handles all of the contact states passed in from Box2D.

    """
    test = None
    def __init__(self):
        super(fwContactListener, self).__init__()

    def handleCall(self, state, point):
        if not self.test: return

        k_maxContactPoints = 2048
        if len(self.test.points) == k_maxContactPoints: return

        self.test.points.append( fwContactPoint() )
        cp = self.test.points[-1]
        cp.shape1 = point.shape1
        cp.shape2 = point.shape2
        cp.position = point.position.copy()
        cp.normal = point.normal.copy()
        cp.id = point.id
        cp.state = state

    def Add(self, point):
        self.handleCall(fwContactTypes.contactAdded, point)

    def Persist(self, point):
        self.handleCall(fwContactTypes.contactPersisted, point)

    def Remove(self, point):
        self.handleCall(fwContactTypes.contactRemoved, point)

class fwDebugDraw(box2d.b2DebugDraw):
    """
    This debug draw class accepts callbacks from Box2D (which specifies what to draw)
    and handles all of the rendering.

    If you are writing your own game, you likely will not want to use debug drawing.
    Debug drawing, as its name implies, is for debugging.
    """
    circle_segments = 16
    surface = None
    viewZoom = 1.0
    viewCenter = None
    viewOffset = None
    width, height = 0, 0
    def __init__(self): super(fwDebugDraw, self).__init__()
    def _setValues(self, viewZoom, viewCenter, viewOffset, width, height):
        """
        Sets the view zoom, center, offset, and width and height of the screen such that access 
        to the main window is unnecessary.
        """
        self.viewZoom=viewZoom
        self.viewCenter=viewCenter
        self.viewOffset=viewOffset
        self.width = width 
        self.height = height

    def convertColor(self, color):
        """
        Take a floating point color in range (0..1,0..1,0..1) and convert it to (255,255,255)
        """
        return (int(255*color.r), int(255*color.g), int(255*color.b))

    def DrawPoint(self, p, size, color):
        """
        Draw a single point at point p given a pixel size and color.
        """
        self.DrawCircle(p, size/self.viewZoom, color, drawwidth=0)
        
    def DrawAABB(self, aabb, color):
        """
        Draw a wireframe around the AABB with the given color.
        """
        points = []
        points.append( (aabb.lowerBound.x, aabb.lowerBound.y ) )
        points.append( (aabb.upperBound.x, aabb.lowerBound.y ) )
        points.append( (aabb.upperBound.x, aabb.upperBound.y ) )
        points.append( (aabb.lowerBound.x, aabb.upperBound.y ) )
        
        pygame.draw.aalines(self.surface, color, True, [self.toScreen(p) for p in points])

    def DrawSegment(self, p1, p2, color):
        """
        Draw the line segment from p1-p2 with the specified color.
        """
        color = self.convertColor(color)
        pygame.draw.aaline(self.surface, color, self.toScreen_v(p1), self.toScreen_v(p2))

    def DrawXForm(self, xf):
        """
        Draw the transform xf on the screen
        """
        p1 = xf.position
        k_axisScale = 0.4
        p2 = self.toScreen_v(p1 + k_axisScale * xf.R.col1)
        p3 = self.toScreen_v(p1 + k_axisScale * xf.R.col2)
        p1 = self.toScreen_v(p1)

        color = (255,0,0)
        pygame.draw.aaline(self.surface, color, p1, p2)

        color = (0,255,0)
        pygame.draw.aaline(self.surface, color, p1, p3)

    def DrawCircle(self, center, radius, color, drawwidth=1):
        """
        Draw a circle given the b2Vec2 center_v, radius, axis of orientation and color.
        """
        color = self.convertColor(color)
        radius *= self.viewZoom
        if radius < 1: radius = 1
        else: radius = int(radius)

        center = self.toScreen_v(center)
        pygame.draw.circle(self.surface, color, center, radius, drawwidth)

    def DrawSolidCircle(self, center_v, radius, axis, color):
        """
        Draw a solid circle given the b2Vec2 center_v, radius, axis of orientation and color.
        """
        color = self.convertColor(color)
        radius *= self.viewZoom
        if radius < 1: radius = 1
        else: radius = int(radius)

        center = self.toScreen_v(center_v)
        pygame.draw.circle(self.surface, (color[0]/2, color[1]/2, color[1]/2, 127), center, radius, 0)

        pygame.draw.circle(self.surface, color, center, radius, 1)

        p = radius * axis
        pygame.draw.aaline(self.surface, (255,0,0), center, (center[0] - p.x, center[1] + p.y)) 

    def DrawPolygon(self, in_vertices, vertexCount, color):
        """
        Draw a wireframe polygon given the world b2Vec2 vertices in_vertices with the specified color.
        """
        color = self.convertColor(color)
        vertices = [self.toScreen(v) for v in in_vertices]
        pygame.draw.polygon(self.surface, color, vertices, 1)
        
    def DrawSolidPolygon(self, in_vertices, vertexCount, color):
        color = self.convertColor(color)
        vertices = [self.toScreen(v) for v in in_vertices]
        pygame.draw.polygon(self.surface, (color[0]/2, color[1]/2, color[1]/2, 127), vertices, 0)
        pygame.draw.polygon(self.surface, color, vertices, 1)

    def toScreen_v(self, pt):
        """
        Input:  pt - a b2Vec2 in world coordinates
        Output: (x, y) - a tuple in screen coordinates
        """
        return (int((pt.x * self.viewZoom) - self.viewOffset.x), int(self.height - ((pt.y * self.viewZoom) - self.viewOffset.y)))
    def toScreen(self, pt):
        """
        Input:  (x, y) - a tuple in world coordinates
        Output: (x, y) - a tuple in screen coordinates
        """
        return ((pt[0] * self.viewZoom) - self.viewOffset.x, self.height - ((pt[1] * self.viewZoom) - self.viewOffset.y))
    def scaleValue(self, value):
        """
        Input: value - unscaled value
        Output: scaled value according to the view zoom ratio
        """
        return value/self.viewZoom

class fwGUI(gui.Table):
    """
    Deals with the initialization and changing the settings based on the GUI 
    controls. Callbacks are not used, but the checkboxes and sliders are polled
    by the main loop.
    """
    checkboxes = (  ("Position Correction", "enablePositionCorrection"), 
                    ("Warm Starting", "enableWarmStarting"), 
                    ("Time of Impact", "enableTOI"), 
                    ("Draw", None),
                    ("Shapes", "drawShapes"), 
                    ("Joints", "drawJoints"), 
                    ("Core Shapes", "drawCoreShapes"), 
                    ("AABBs", "drawAABBs"), 
                    ("OBBs", "drawOBBs"), 
                    ("Pairs", "drawPairs"), 
                    ("Contact Points", "drawContactPoints"), 
                    ("Contact Normals", "drawContactNormals"), 
#                    ("Contact Forces", "drawContactForces"), # unused
#                    ("Friction Forces", "drawFrictionForces"),  #unused
                    ("Center of Masses", "drawCOMs"), 
                    ("Statistics", "drawStats"),
                    ("FPS", "drawFPS"),
                    ("Control", None),
                    ("Pause", "pause"),
                    ("Single Step", "singleStep") )
    form = None

    def __init__(self,settings, **params):
        # The framework GUI is just basically a HTML-like table.
        # There are 2 columns, and basically everything is right-aligned.
        gui.Table.__init__(self,**params)
        self.form=gui.Form()

        fg = (255,255,255)

        # "Hertz"
        self.tr()
        self.td(gui.Label("Hertz",color=fg),align=1,colspan=2)

        # Hertz slider
        self.tr()
        e = gui.HSlider(settings.hz,5,200,size=20,width=100,height=16,name='hz')
        self.td(e,colspan=2,align=1)

        # "Iterations"
        self.tr()
        self.td(gui.Label("Iterations",color=fg),align=1,colspan=2)

        # Iterations slider (min 1, max 100)
        self.tr()
        e = gui.HSlider(settings.iterationCount,1,100,size=20,width=100,height=16,name='iterationCount')
        self.td(e,colspan=2,align=1)

        # Add each of the checkboxes.
        for text, variable in self.checkboxes:
            self.tr()
            if variable == None:
                # Checkboxes that have no variable (i.e., None) are just labels.
                self.td(gui.Label(text, color=fg), align=1, colspan=2)
            else:
                # Add the label and then the switch/checkbox
                self.td(gui.Label(text, color=fg), align=1)
                self.td(gui.Switch(value=getattr(settings, variable),name=variable))

    def updateSettings(self, settings):
        """
        Change all of the settings based on the current state of the GUI.
        """
        for text, variable in self.checkboxes:
            if variable == None: continue
            setattr(settings, variable, self.form[variable].value)

        # Now do the sliders
        settings.hz = int(self.form['hz'].value)
        settings.iterationCount = int(self.form['iterationCount'].value)

        # If we're in single-step mode, update the GUI to reflect that.
        if settings.singleStep:
            settings.pause=True
            self.form['pause'].value = True
            self.form['singleStep'].value = False

class Framework(object):
    """
    The main testbed framework.
    It handles basically everything:
    * The initialization of pygame, Box2D
    * Contains the main loop
    * Handles all user input.

    You should derive your class from this one to implement your own tests.
    See test_Empty.py or any of the other tests for more information.
    """
    name = "None"

    # Box2D-related
    worldAABB = box2d.b2AABB()
    points = []
    world = None
    bomb = None
    mouseJoint = None
    settings = fwSettings()

    # Box2D-callbacks
    destructionListener = None
    boundaryListener = None
    contactListener = None
    debugDraw = None

    # Screen-related
    viewZoom = 10.0
    viewCenter = box2d.b2Vec2(0,10.0*20.0) # y = viewZoom * (pos)
    viewOffset = box2d.b2Vec2(0,0)
    screenSize = None
    rMouseDown = False
    textLine = 30
    font = None
    fps = 0

    # GUI-related (PGU)
    gui_app   = None
    gui_table = None
    def __init__(self):
        # Pygame Initialization
        pygame.init()

        caption= "Python Box2D Testbed - " + self.name
        pygame.display.set_caption(caption)

        self.screen = pygame.display.set_mode( (640,480) )
        self.screenSize = box2d.b2Vec2(*self.screen.get_size())
        self.font = pygame.font.Font(None, 15)

        # GUI Initialization
        self.gui_app = gui.App()
        self.gui_table=fwGUI(self.settings)
        container = gui.Container(align=1,valign=-1)
        container.add(self.gui_table,0,0)
        self.gui_app.init(container)

        # Box2D Initialization
        self.worldAABB.lowerBound.Set(-200.0, -100.0)
        self.worldAABB.upperBound.Set( 200.0, 200.0)
        gravity = box2d.b2Vec2(0.0, -10.0)

        doSleep = True
        self.world = box2d.b2World(self.worldAABB, gravity, doSleep)
        self.destructionListener = fwDestructionListener()
        self.boundaryListener = fwBoundaryListener()
        self.contactListener = fwContactListener()
        self.debugDraw = fwDebugDraw()

        self.debugDraw.surface = self.screen

        self.destructionListener.test = self
        self.boundaryListener.test = self
        self.contactListener.test = self
        
        self.world.SetDestructionListener(self.destructionListener)
        self.world.SetBoundaryListener(self.boundaryListener)
        self.world.SetContactListener(self.contactListener)
        self.world.SetDebugDraw(self.debugDraw)

        self.updateCenter()

    def updateCenter(self):
        """
        Updates the view offset based on the center of the screen.
        
        Tells the debug draw to update its values also.
        """
        self.viewOffset = self.viewCenter - self.screenSize/2

        self.debugDraw._setValues(self.viewZoom, self.viewCenter, self.viewOffset, self.screenSize.x, self.screenSize.y)
        
    def checkEvents(self):
        """
        Check for pygame events (mainly keyboard/mouse events).
        Passes the events onto the GUI also.
        """
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return False
            elif event.type == KEYDOWN:
                self._Keyboard_Event(event.key)
            elif event.type == MOUSEBUTTONDOWN:
                p = self.ConvertScreenToWorld(*event.pos)
                if event.button == 1: # left
                    self.MouseDown( p )
                elif event.button == 2: #middle
                    pass
                elif event.button == 3: #right
                    self.rMouseDown = True
                elif event.button ==4:
                    self.viewZoom *= 1.1
                    self.updateCenter()
                elif event.button == 5:
                    self.viewZoom /= 1.1
                    self.updateCenter()
            elif event.type == MOUSEBUTTONUP:
                if event.button == 3: #right
                    self.rMouseDown = False
                else:
                    self.MouseUp()
            elif event.type == MOUSEMOTION:
                p = self.ConvertScreenToWorld(*event.pos)

                self.MouseMove(p)

                if self.rMouseDown:
                    self.viewCenter -= box2d.b2Vec2(event.rel[0], -event.rel[1])
                    self.updateCenter()

            self.gui_app.event(event) #Pass the event to the GUI

        return True

    def run(self):
        """
        Main loop.

        Continues to run while checkEvents indicates the user has 
        requested to quit.

        Updates the screen and tells the GUI to paint itself.
        """
        running = True
        clock = pygame.time.Clock()

        while running:
            running = self.checkEvents()
            self.screen.fill( (0,0,0) )

            # Check keys that should be checked every loop (not only on initial keydown)
            self.CheckKeys()

            # Run the simulation loop 
            self.SimulationLoop()

            if self.settings.drawMenu:
                self.gui_app.paint(self.screen)

            pygame.display.flip()
            clock.tick(self.settings.hz)
            self.fps = clock.get_fps()

    def SetTextLine(self, line):
        """
        Kept for compatibility with C++ Box2D's testbeds.
        
        ** TODO: Probably should update this to be more logical and easy to use.
        """
        self.textLine=line

    def Step(self, settings):
        """
        The main physics step.

        Takes care of physics drawing (callbacks are executed after the world.Step() )
        and drawing additional information.
        """

        # Update the settings based on the GUI
        self.gui_table.updateSettings(settings)

        # Don't do anything if the setting's Hz are <= 0
        if settings.hz > 0.0:
            timeStep = 1.0 / settings.hz
        else:
            timeStep = 0.0
        
        # If paused, display so
        if settings.pause:
            if settings.singleStep:
                settings.singleStep=False
            else:
                timeStep = 0.0

            self.DrawString(5, self.textLine, "****PAUSED****")
            self.textLine += 15

        # Set the flags based on what the settings show (uses a bitwise or mask)
        flags = 0
        if settings.drawShapes:     flags |= box2d.b2DebugDraw.e_shapeBit
        if settings.drawJoints:     flags |= box2d.b2DebugDraw.e_jointBit
        if settings.drawCoreShapes: flags |= box2d.b2DebugDraw.e_coreShapeBit
        if settings.drawAABBs:      flags |= box2d.b2DebugDraw.e_aabbBit
        if settings.drawOBBs:       flags |= box2d.b2DebugDraw.e_obbBit
        if settings.drawPairs:      flags |= box2d.b2DebugDraw.e_pairBit
        if settings.drawCOMs:       flags |= box2d.b2DebugDraw.e_centerOfMassBit
        self.debugDraw.SetFlags(flags)

        # Set the other settings that aren't contained in the flags
        self.world.SetWarmStarting(settings.enableWarmStarting)
    	self.world.SetPositionCorrection(settings.enablePositionCorrection)
    	self.world.SetContinuousPhysics(settings.enableTOI)

        # Reset the collision points
        self.points = []

        # Tell Box2D to step
        self.world.Step(timeStep, settings.iterationCount)
        self.world.Validate()

        # If the bomb is frozen, get rid of it.
        if self.bomb and self.bomb.IsFrozen():
            self.world.DestroyBody(self.bomb)
            self.bomb = None

        if settings.drawStats:
            self.DrawString(5, self.textLine, "proxies(max) = %d(%d), pairs(max) = %d(%d)" % (
                self.world.GetProxyCount(), box2d.b2_maxProxies, self.world.GetPairCount(), box2d.b2_maxPairs) )
            self.textLine += 15

            self.DrawString(5, self.textLine, "bodies/contacts/joints = %d/%d/%d" %
                (self.world.GetBodyCount(), self.world.GetContactCount(), self.world.GetJointCount()))
            self.textLine += 15

            self.DrawString(5, self.textLine, "hz %d iterations %d" %
                (settings.hz, settings.iterationCount))
            self.textLine += 15

            #self.DrawString(5, self.textLine, "heap bytes = %d" % box2d.b2_byteCount) # not wrapped?
            #self.textLine += 15

        if settings.drawFPS: #python version only
            self.DrawString(5, self.textLine, "FPS %d" % self.fps)
            self.textLine += 15
        
        # If there's a mouse joint, draw the connection between the object and the current pointer position.
        if self.mouseJoint:
            body = self.mouseJoint.GetBody2()
            p1 = body.GetWorldPoint(self.mouseJoint.m_localAnchor)
            p2 = self.mouseJoint.m_target

            self.debugDraw.DrawPoint(p1, settings.pointSize, box2d.b2Color(0,1.0,0))
            self.debugDraw.DrawPoint(p2, settings.pointSize, box2d.b2Color(0,1.0,0))
            self.debugDraw.DrawSegment(p1, p2, box2d.b2Color(0.8,0.8,0.8))

        # Draw each of the contact points in different colors.
        if self.settings.drawContactPoints:
            #k_impulseScale = 0.1
            k_axisScale = 0.3

            for point in self.points:
                if point.state == fwContactTypes.contactAdded:
                    self.debugDraw.DrawPoint(point.position, settings.pointSize, box2d.b2Color(0.3, 0.95, 0.3))
                elif point.state == fwContactTypes.contactPersisted:
                    self.debugDraw.DrawPoint(point.position, settings.pointSize, box2d.b2Color(0.3, 0.3, 0.95))
                else: #elif point.state == fwContactTypes.contactRemoved:
                    self.debugDraw.DrawPoint(point.position, settings.pointSize, box2d.b2Color(0.95, 0.3, 0.3))

                if settings.drawContactNormals:
                    p1 = point.position
                    p2 = p1 + k_axisScale * point.normal
                    self.debugDraw.DrawSegment(p1, p2, box2d.b2Color(0.4, 0.9, 0.4))

                # point.normalForce, point.tangentForce don't exist, so we can't use these two:
                #if settings.drawContactForces: # commented out in the testbed code
                    #k_forceScale=1.0 #? unknown
                    #p1 = point.position
                    #p2 = p1 + k_forceScale * point.normalForce * point.normal
                    #self.DrawSegment(p1, p2, box2d.b2Color(0.9, 0.9, 0.3))

                #if settings.drawFrictionForces: # commented out in the testbed code                    
                    #k_forceScale=1.0 #? unknown
                    #tangent = box2d.b2Cross(point.normal, 1.0)
                    #p1 = point.position
                    #p2 = p1 + k_forceScale * point.tangentForce * tangent
                    #DrawSegment(p1, p2, box2d.b2Color(0.9, 0.9, 0.3))

    def _Keyboard_Event(self, key):
        """
        Internal keyboard event, don't override this.

        Checks for the initial keydown of the basic testbed keys. Passes the unused
        ones onto the test via the Keyboard() function.
        """
        if key==K_z:
            # Zoom in
            self.viewZoom = min(1.1 * self.viewZoom, 20.0)
            self.updateCenter()
        elif key==K_x:
            # Zoom out
            self.viewZoom = max(0.9 * self.viewZoom, 0.02)
            self.updateCenter()
        elif key==K_r:
            # Reload (disabled)
            #print "Reload not functional"
            exit(10)
        elif key==K_SPACE:
            # Launch a bomb
            self.LaunchBomb()
        elif key==K_F1:
            # Toggle drawing the menu
            self.settings.drawMenu = not self.settings.drawMenu
        else:
            # Inform the test of the key press
            self.Keyboard(key)
        
    def MouseDown(self, p):
        """
        Indicates that there was a left click at point p (world coordinates)
        """
        if self.mouseJoint != None:
            return

        # Create a mouse joint on the selected body (assuming it's dynamic)

        # Make a small box.
        aabb = box2d.b2AABB()
        d = box2d.b2Vec2(0.001, 0.001)
        aabb.lowerBound = p - d
        aabb.upperBound = p + d

        # Query the world for overlapping shapes.
        body = None
        k_maxCount = 10 # maximum amount of shapes to return

        (count, shapes) = self.world.Query(aabb, k_maxCount)
        for shape in shapes:
            shapeBody = shape.GetBody()
            if shapeBody.IsStatic() == False and shapeBody.GetMass() > 0.0:
                if shape.TestPoint(shapeBody.GetXForm(), p): # is it inside?
                    body = shapeBody
                    break
        
        if body:
            md = box2d.b2MouseJointDef()
            md.body1   = self.world.GetGroundBody()
            md.body2   = body
            md.target  = p
            md.maxForce= 1000.0 * body.GetMass()
            self.mouseJoint = self.world.CreateJoint(md).getAsType()
            body.WakeUp()

    def MouseUp(self):
        """
        Left mouse button up.
        """     
        if self.mouseJoint:
            self.world.DestroyJoint(self.mouseJoint)
            self.mouseJoint = None

    def MouseMove(self, p):
        """
        Mouse moved to point p, in world coordinates.
        """
        if self.mouseJoint:
            self.mouseJoint.SetTarget(p)

    def LaunchBomb(self):
        """
        Create a new bomb and launch it at the testbed.
        A bomb is a simple circle which has a random position and velocity.
        """
        if self.bomb:
            self.world.DestroyBody(self.bomb)
            self.bomb = None
        bd = box2d.b2BodyDef()
        bd.allowSleep = True
        bd.position.Set(box2d.b2Random(-15.0, 15.0), 30.0)
        bd.isBullet = True
        self.bomb = self.world.CreateBody(bd)
        self.bomb.SetLinearVelocity(-5.0 * bd.position)

        sd = box2d.b2CircleDef()
        sd.radius = 0.3
        sd.density = 20.0
        sd.restitution = 0.1
        self.bomb.CreateShape(sd)
        
        self.bomb.SetMassFromShapes()
     
    def CheckKeys(self):
        """
        Check the keys that are evaluated on every main loop iteration.
        I.e., they aren't just evaluated when first pressed down
        """

        pygame.event.pump()
        self.keys = keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.viewCenter.x -= 0.5
            self.updateCenter()
        elif keys[K_RIGHT]:
            self.viewCenter.x += 0.5
            self.updateCenter()
        if keys[K_UP]:
            self.viewCenter.y += 0.5
            self.updateCenter()
        elif keys[K_DOWN]:
            self.viewCenter.y -= 0.5
            self.updateCenter()

        if keys[K_HOME]:
            self.viewZoom = 1.0
            self.viewCenter.Set(0.0, 20.0)
            self.updateCenter()

    def SimulationLoop(self):
        """
        The main simulation loop contents.
        """
        # TODO: perhaps just stick this all in Step()? Is it really necessary?
        self.SetTextLine(30)
        self.DrawString(5, 15, self.name)
        self.Step(self.settings)

    def ConvertScreenToWorld(self, x, y):
        """
        Return a b2Vec2 in world coordinates of the passed in screen coordinates x, y
        """
        return box2d.b2Vec2((x + self.viewOffset.x) / self.viewZoom, ((self.screenSize.y - y + self.viewOffset.y) / self.viewZoom))

    def DrawString(self, x, y, str):
        """
        Draw some text, str, at screen coordinates (x, y).
        """
        color = (229, 153, 153, 255) # 0.9, 0.6, 0.6
        text = self.font.render(str, True, color)
        self.screen.blit(text, (x,y))

    # These should be implemented in the subclass: (Step() also if necessary)
    def JointDestroyed(self, joint):
        """
        Callback indicating 'joint' has been destroyed.
        """
        pass

    def BoundaryViolated(self, body):
        """
        Callback indicating 'body' has left the world AABB.
        """
        pass

    def Keyboard(self, key):
        """
        Callback indicating 'key' has been pressed down.
        The key is from pygame.locals.K_*:

         from pygame.locals import *
         ...
         if key == K_z:
             pass
        """
        pass

def main(test_class):
    """
    Loads the test class and executes it.
    """
    print "----------------------------------"
    print "Loading %s..." % test_class.name
    test = test_class()
    test.run()

if __name__=="__main__":
    from test_empty import Empty
    main(Empty)
