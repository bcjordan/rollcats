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


from pygame.locals import *
import test_main
from test_main import box2d
from test_main import fwContactTypes
import math

# Contributed by caspin (C++ version)

class ContactCallbackTest (test_main.Framework):
    name="ContactCallbackTest"
     
    m_ball=None 
    m_bullet=None 
    m_ball_shape=None 
     
    def __init__(self):
        super(ContactCallbackTest, self).__init__()

        sd=box2d.b2PolygonDef() 
        sd.friction = 0
        sd.vertexCount = 3
        sd.setVertex(0,10,10)
        sd.setVertex(1,9,7)
        sd.setVertex(2,10,0)
        self.world.GetGroundBody().CreateShape(sd)

        sd.setVertex(0,9,7)
        sd.setVertex(1,8,0)
        sd.setVertex(2,10,0)
        self.world.GetGroundBody().CreateShape(sd)

        sd.setVertex(0,9,7)
        sd.setVertex(1,8,5)
        sd.setVertex(2,8,0)
        self.world.GetGroundBody().CreateShape(sd)

        sd.setVertex(0,8,5)
        sd.setVertex(1,7,4)
        sd.setVertex(2,8,0)
        self.world.GetGroundBody().CreateShape(sd)

        sd.setVertex(0,7,4)
        sd.setVertex(1,5,0)
        sd.setVertex(2,8,0)
        self.world.GetGroundBody().CreateShape(sd)

        sd.setVertex(0,7,4)
        sd.setVertex(1,5,3)
        sd.setVertex(2,5,0)
        self.world.GetGroundBody().CreateShape(sd)

        sd.setVertex(0,5,3)
        sd.setVertex(1,2,2)
        sd.setVertex(2,5,0)
        self.world.GetGroundBody().CreateShape(sd)

        sd.setVertex(0,2,2)
        sd.setVertex(1,0,0)
        sd.setVertex(2,5,0)
        self.world.GetGroundBody().CreateShape(sd)

        sd.setVertex(0,2,2)
        sd.setVertex(1,-2,2)
        sd.setVertex(2,0,0)
        self.world.GetGroundBody().CreateShape(sd)

        sd.setVertex(2,-2,2)
        sd.setVertex(1,0,0)
        sd.setVertex(0,-5,0)
        self.world.GetGroundBody().CreateShape(sd)

        sd.setVertex(2,-5,3)
        sd.setVertex(1,-2,2)
        sd.setVertex(0,-5,0)
        self.world.GetGroundBody().CreateShape(sd)

        sd.setVertex(2,-7,4)
        sd.setVertex(1,-5,3)
        sd.setVertex(0,-5,0)
        self.world.GetGroundBody().CreateShape(sd)

        sd.setVertex(2,-7,4)
        sd.setVertex(1,-5,0)
        sd.setVertex(0,-8,0)
        self.world.GetGroundBody().CreateShape(sd)

        sd.setVertex(2,-8,5)
        sd.setVertex(1,-7,4)
        sd.setVertex(0,-8,0)
        self.world.GetGroundBody().CreateShape(sd)

        sd.setVertex(2,-9,7)
        sd.setVertex(1,-8,5)
        sd.setVertex(0,-8,0)
        self.world.GetGroundBody().CreateShape(sd)

        sd.setVertex(2,-9,7)
        sd.setVertex(1,-8,0)
        sd.setVertex(0,-10,0)
        self.world.GetGroundBody().CreateShape(sd)

        sd.setVertex(2,-10,10)
        sd.setVertex(1,-9,7)
        sd.setVertex(0,-10,0)
        self.world.GetGroundBody().CreateShape(sd)

        sd.SetAsBox(.5,6,box2d.b2Vec2(10.5,6),0)
        self.world.GetGroundBody().CreateShape(sd)

        sd.SetAsBox(.5,6,box2d.b2Vec2(-10.5,6),0)
        self.world.GetGroundBody().CreateShape(sd)

        bd=box2d.b2BodyDef() 
        bd.position.Set(9.5,60)
        self.m_ball = self.world.CreateBody( bd ) 

        cd=box2d.b2PolygonDef() 
        cd.vertexCount = 8
        w = 1.0
        b = w / (2.0 + math.sqrt(2.0))
        s = math.sqrt(2.0) * b
        cd.setVertex(0,0.5 * s, 0.0)
        cd.setVertex(1,0.5 * w, b)
        cd.setVertex(2,0.5 * w, b + s)
        cd.setVertex(3,0.5 * s, w)
        cd.setVertex(4,-0.5 * s, w)
        cd.setVertex(5,-0.5 * w, b + s)
        cd.setVertex(6,-0.5 * w, b)
        cd.setVertex(7,-0.5 * s, 0.0)
        cd.density = 1.0

        self.m_ball_shape = self.m_ball.CreateShape(cd)
        self.m_ball.SetMassFromShapes()

    def Step(self, settings):
        strings = []
        for point in self.points:
            if  point.state ==fwContactTypes.contactAdded:
                strings.append("added:   " + str(point.shape1) + " . " + str(point.shape2) + ":" + str(point.id.key))
            elif  point.state ==fwContactTypes.contactRemoved:
                strings.append("removed: " + str(point.shape1) + " . " + str(point.shape2) + ":" + str(point.id.key))
            elif  point.state ==fwContactTypes.contactPersisted:
                strings.append("persisted:" + str(point.shape1) + " . " + str(point.shape2) + ":" + str(point.id.key))

        if len(strings) > 15:
            strings = strings[:14]

        for string in strings:
           self.DrawString(5, self.textLine, string)
           self.textLine += 15

        super(ContactCallbackTest, self).Step(settings)

if __name__=="__main__":
     test_main.main(ContactCallbackTest)
