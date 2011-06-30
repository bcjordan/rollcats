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
class MotorsAndLimits (test_main.Framework):
    name="MotorsAndLimits"
    m_joint1=None
    m_joint2=None
    m_joint3=None
    def __init__(self):
        super(MotorsAndLimits, self).__init__()
        sd=box2d.b2PolygonDef() 
        sd.SetAsBox(50.0, 10.0)

        bd=box2d.b2BodyDef() 
        bd.position.Set(0.0, -10.0)
        ground = self.world.CreateBody(bd)
        ground.CreateShape(sd)

        sd=box2d.b2PolygonDef() 
        sd.SetAsBox(2.0, 0.5)
        sd.density = 5.0
        sd.friction = 0.05

        bd=box2d.b2BodyDef() 

        rjd=box2d.b2RevoluteJointDef() 

        prevBody=ground
        y = 8.0

        bd.position.Set(3.0, y)
        body = self.world.CreateBody(bd)
        body.CreateShape(sd)
        body.SetMassFromShapes()

        rjd.Initialize(prevBody, body, box2d.b2Vec2(0.0, y))
        rjd.motorSpeed = 1.0 * box2d.b2_pi
        rjd.maxMotorTorque = 10000.0
        rjd.enableMotor = True

        self.m_joint1 = self.world.CreateJoint(rjd).getAsType()

        prevBody = body

        bd.position.Set(9.0, y)
        body = self.world.CreateBody(bd)
        body.CreateShape(sd)
        body.SetMassFromShapes()

        rjd.Initialize(prevBody, body, box2d.b2Vec2(6.0, y))
        rjd.motorSpeed = 0.5 * box2d.b2_pi
        rjd.maxMotorTorque = 2000.0
        rjd.enableMotor = True
        rjd.lowerAngle = - 0.5 * box2d.b2_pi
        rjd.upperAngle = 0.5 * box2d.b2_pi
        rjd.enableLimit = True

        self.m_joint2 = self.world.CreateJoint(rjd).getAsType()

        bd.position.Set(-10.0, 10.0)
        bd.angle = 0.5 * box2d.b2_pi
        body = self.world.CreateBody(bd)
        body.CreateShape(sd)
        body.SetMassFromShapes()

        pjd=box2d.b2PrismaticJointDef() 
        pjd.Initialize(ground, body, box2d.b2Vec2(-10.0, 10.0), box2d.b2Vec2(1.0, 0.0))
        pjd.motorSpeed = 10.0
        pjd.maxMotorForce = 1000.0
        pjd.enableMotor = True
        pjd.lowerTranslation = 0.0
        pjd.upperTranslation = 20.0
        pjd.enableLimit = True

        self.m_joint3 = self.world.CreateJoint(pjd).getAsType()

    def Keyboard(self, key) :
        if key==K_l:
            self.m_joint2.EnableLimit(not self.m_joint2.IsLimitEnabled())
            self.m_joint3.EnableLimit(not self.m_joint3.IsLimitEnabled())
            self.m_joint2.GetBody1().WakeUp()
            self.m_joint3.GetBody2().WakeUp()

        elif key==K_m:
            self.m_joint1.EnableMotor(not self.m_joint1.IsMotorEnabled())
            self.m_joint2.EnableMotor(not self.m_joint2.IsMotorEnabled())
            self.m_joint3.EnableMotor(not self.m_joint3.IsMotorEnabled())
            self.m_joint2.GetBody1().WakeUp()
            self.m_joint3.GetBody2().WakeUp()

        elif key==K_p:
            self.m_joint3.GetBody2().WakeUp()
            self.m_joint3.SetMotorSpeed(-self.m_joint3.GetMotorSpeed())
     
    def Step(self, settings):
        self.DrawString(5, self.textLine, "Keys: (l) limits, (m) motors, (p) prismatic speed")
        self.textLine += 15
        torque1 = self.m_joint1.GetMotorTorque()
        torque2 = self.m_joint2.GetMotorTorque()
        force3 = self.m_joint3.GetMotorForce()
        self.DrawString(5, self.textLine, "Motor Torque = %.0f, %.0f : Motor Force = %.0f" % (torque1,torque2, force3))
        self.textLine += 15
        super(MotorsAndLimits, self).Step(settings)

if __name__=="__main__":
     test_main.main(MotorsAndLimits)
