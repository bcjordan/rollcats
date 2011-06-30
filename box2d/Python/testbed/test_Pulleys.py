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
class Pulleys (test_main.Framework):
    name="Pulleys"
    def __init__(self):
        super(Pulleys, self).__init__()
        sd=box2d.b2PolygonDef() 
        sd.SetAsBox(50.0, 10.0)

        bd=box2d.b2BodyDef() 
        bd.position.Set(0.0, -10.0)
        ground = self.world.CreateBody(bd)
        ground.CreateShape(sd)

        a = 2.0
        b = 4.0
        y = 16.0
        L = 12.0

        sd=box2d.b2PolygonDef() 
        sd.SetAsBox(a, b)
        sd.density = 5.0

        bd=box2d.b2BodyDef() 

        bd.position.Set(-10.0, y)
        body1 = self.world.CreateBody(bd) 
        body1.CreateShape(sd)
        body1.SetMassFromShapes()

        bd.position.Set(10.0, y)
        body2 = self.world.CreateBody(bd) 
        body2.CreateShape(sd)
        body2.SetMassFromShapes()

        pulleyDef=box2d.b2PulleyJointDef() 

        anchor1=box2d.b2Vec2(-10.0, y + b)

        anchor2=box2d.b2Vec2(10.0, y + b)

        groundAnchor1=box2d.b2Vec2(-10.0, y + b + L)

        groundAnchor2=box2d.b2Vec2(10.0, y + b + L)
        pulleyDef.Initialize(body1, body2, groundAnchor1, groundAnchor2, anchor1, anchor2, 2.0)

        self.m_joint1 = self.world.CreateJoint(pulleyDef).getAsType() 
     
    def Step(self, settings) :
        ratio = self.m_joint1.GetRatio()
        L = self.m_joint1.GetLength1() + ratio * self.m_joint1.GetLength2()
        self.DrawString(5, self.textLine, "L1 + %.2f * L2 = %.2f" % (ratio, L))
        self.textLine += 15
        super(Pulleys, self).Step(settings)

if __name__=="__main__":
    test_main.main(Pulleys)
