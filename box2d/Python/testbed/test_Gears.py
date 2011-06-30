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

class Gears (test_main.Framework):
    name="Gears"
    m_joint1=None
    m_joint2=None
    m_joint3=None
    m_joint4=None
    m_joint5=None
    def __init__(self):
        super(Gears, self).__init__()
        bd=box2d.b2BodyDef() 
        bd.position.Set(0.0, -10.0)
        ground = self.world.CreateBody(bd)

        sd=box2d.b2PolygonDef() 
        sd.SetAsBox(50.0, 10.0)
        ground.CreateShape(sd)

        circle1=box2d.b2CircleDef() 
        circle1.radius = 1.0
        circle1.density = 5.0

        circle2=box2d.b2CircleDef() 
        circle2.radius = 2.0
        circle2.density = 5.0

        box=box2d.b2PolygonDef() 
        box.SetAsBox(0.5, 5.0)
        box.density = 5.0

        bd1=box2d.b2BodyDef() 
        bd1.position.Set(-3.0, 12.0)
        body1 = self.world.CreateBody(bd1) 
        body1.CreateShape(circle1)
        body1.SetMassFromShapes()

        jd1=box2d.b2RevoluteJointDef() 
        jd1.body1 = ground
        jd1.body2 = body1
        jd1.localAnchor1 = ground.GetLocalPoint(bd1.position)
        jd1.localAnchor2 = body1.GetLocalPoint(bd1.position)
        jd1.referenceAngle = body1.GetAngle() - ground.GetAngle()
        self.m_joint1 = self.world.CreateJoint(jd1).getAsType()

        bd2=box2d.b2BodyDef() 
        bd2.position.Set(0.0, 12.0)
        body2 = self.world.CreateBody(bd2) 
        body2.CreateShape(circle2)
        body2.SetMassFromShapes()

        jd2=box2d.b2RevoluteJointDef() 
        jd2.Initialize(ground, body2, bd2.position)
        self.m_joint2 = self.world.CreateJoint(jd2).getAsType()

        bd3=box2d.b2BodyDef() 
        bd3.position.Set(2.5, 12.0)
        body3 = self.world.CreateBody(bd3) 
        body3.CreateShape(box)
        body3.SetMassFromShapes()

        jd3=box2d.b2PrismaticJointDef() 
        jd3.Initialize(ground, body3, bd3.position, box2d.b2Vec2(0.0, 1.0))
        jd3.lowerTranslation = -5.0
        jd3.upperTranslation = 5.0
        jd3.enableLimit = True

        self.m_joint3 = self.world.CreateJoint(jd3).getAsType()

        jd4=box2d.b2GearJointDef() 
        jd4.body1 = body1
        jd4.body2 = body2
        jd4.joint1 = self.m_joint1
        jd4.joint2 = self.m_joint2
        jd4.ratio = circle2.radius / circle1.radius
        self.m_joint4 = self.world.CreateJoint(jd4).getAsType()

        jd5=box2d.b2GearJointDef() 
        jd5.body1 = body2
        jd5.body2 = body3
        jd5.joint1 = self.m_joint2
        jd5.joint2 = self.m_joint3
        jd5.ratio = -1.0 / circle2.radius
        self.m_joint5 = self.world.CreateJoint(jd5).getAsType()
             
    def Step(self, settings):
        ratio = self.m_joint4.GetRatio()
        value = self.m_joint1.GetJointAngle() + ratio * self.m_joint2.GetJointAngle()
        self.DrawString(5, self.textLine, "theta1 + %.2f * theta2 = %.2f" % (ratio, value))
        self.textLine += 15

        ratio = self.m_joint5.GetRatio()
        value = self.m_joint2.GetJointAngle() + ratio * self.m_joint3.GetJointTranslation()
        self.DrawString(5, self.textLine, "theta2 + %.2f * delta = %.2f" % (ratio, value))
        self.textLine += 15

        super(Gears, self).Step(settings)

if __name__=="__main__":
     test_main.main(Gears)
