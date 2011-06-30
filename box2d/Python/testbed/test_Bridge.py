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

class Bridge(test_main.Framework):
    name = "Bridge"
    def __init__(self):
        super(Bridge, self).__init__()
        
        sd = box2d.b2PolygonDef()
        sd.SetAsBox(50.0, 10.0)

        bd = box2d.b2BodyDef()
        bd.position.Set(0.0, -10.0)
        ground = self.world.CreateBody(bd)
        ground.CreateShape(sd)

        sd = box2d.b2PolygonDef()        
        sd.SetAsBox(0.5, 0.125)
        sd.density = 20.0
        sd.friction = 0.2

        jd = box2d.b2RevoluteJointDef()
        numPlanks = 30

        prevBody = ground
        for i in range(numPlanks):
            bd = box2d.b2BodyDef()
            bd.position.Set(-14.5 + 1.0 * i, 5.0)

            body = self.world.CreateBody(bd)
            body.CreateShape(sd)
            body.SetMassFromShapes()

            anchor=box2d.b2Vec2(-15.0 + 1.0 * i, 5.0)
            jd.Initialize(prevBody, body, anchor)
            self.world.CreateJoint(jd)

            prevBody = body

        anchor = box2d.b2Vec2(-15.0 + 1.0 * numPlanks, 5.0)
        jd.Initialize(prevBody, ground, anchor)
        self.world.CreateJoint(jd)

        for i in range(2):
            sd=box2d.b2PolygonDef()
            sd.vertexCount = 3
            sd.setVertex(0,-0.5, 0.0)
            sd.setVertex(1,0.5, 0.0)
            sd.setVertex(2,0.0, 1.5)
            sd.density = 1.0

            bd=box2d.b2BodyDef()
            bd.position.Set(-8.0 + 8.0 * i, 12.0)
            body = self.world.CreateBody(bd)
            body.CreateShape(sd)
            body.SetMassFromShapes()

        for i in range(3):
            sd=box2d.b2CircleDef()
            sd.radius = 0.5
            sd.density = 1.0

            bd=box2d.b2BodyDef()
            bd.position.Set(-6.0 + 6.0 * i, 10.0)
            body = self.world.CreateBody(bd)
            body.CreateShape(sd)
            body.SetMassFromShapes()
 
if __name__=="__main__":
    test_main.main(Bridge)
