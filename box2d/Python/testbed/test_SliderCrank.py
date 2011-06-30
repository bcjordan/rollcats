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

# A motor driven slider crank with joint friction.

class SliderCrank (test_main.Framework):
    name="SliderCrank"
    m_joint1=None
    m_joint2=None

    def __init__(self):
        super(SliderCrank, self).__init__()
        sd=box2d.b2PolygonDef() 
        sd.SetAsBox(50.0, 10.0)

        bd=box2d.b2BodyDef() 
        bd.position.Set(0.0, -10.0)
        ground = self.world.CreateBody(bd)
        ground.CreateShape(sd)

        # Define crank.
        sd=box2d.b2PolygonDef() 
        sd.SetAsBox(0.5, 2.0)
        sd.density = 1.0

        rjd=box2d.b2RevoluteJointDef() 

        prevBody=ground

        bd=box2d.b2BodyDef() 
        bd.position.Set(0.0, 7.0)
        body = self.world.CreateBody(bd) 
        body.CreateShape(sd)
        body.SetMassFromShapes()

        rjd.Initialize(prevBody, body, box2d.b2Vec2(0.0, 5.0))
        rjd.motorSpeed = 1.0 * box2d.b2_pi
        rjd.maxMotorTorque = 10000.0
        rjd.enableMotor = True
        self.m_joint1 = self.world.CreateJoint(rjd).getAsType()

        prevBody = body

        # Define follower.
        sd.SetAsBox(0.5, 4.0)
        bd.position.Set(0.0, 13.0)
        body = self.world.CreateBody(bd)
        body.CreateShape(sd)
        body.SetMassFromShapes()

        rjd.Initialize(prevBody, body, box2d.b2Vec2(0.0, 9.0))
        rjd.enableMotor = False
        self.world.CreateJoint(rjd).getAsType()

        prevBody = body

        # Define piston
        sd.SetAsBox(1.5, 1.5)
        bd.position.Set(0.0, 17.0)
        body = self.world.CreateBody(bd)
        body.CreateShape(sd)
        body.SetMassFromShapes()

        rjd.Initialize(prevBody, body, box2d.b2Vec2(0.0, 17.0))
        self.world.CreateJoint(rjd).getAsType()

        pjd=box2d.b2PrismaticJointDef() 
        pjd.Initialize(ground, body, box2d.b2Vec2(0.0, 17.0), box2d.b2Vec2(0.0, 1.0))

        pjd.maxMotorForce = 1000.0
        pjd.enableMotor = True

        self.m_joint2 = self.world.CreateJoint(pjd).getAsType()

        # Create a payload
        sd.density = 2.0
        bd.position.Set(0.0, 23.0)
        body = self.world.CreateBody(bd)
        body.CreateShape(sd)
        body.SetMassFromShapes()

    def Keyboard(self, key) :
          if key==K_f:
               self.m_joint2.m_enableMotor = not self.m_joint2.m_enableMotor
               self.m_joint2.GetBody2().WakeUp()
               
          elif key==K_m:
               self.m_joint1.m_enableMotor = not self.m_joint1.m_enableMotor
               self.m_joint1.GetBody2().WakeUp()
     
    def Step(self, settings) :
          self.DrawString(5, self.textLine, "Keys: (f) toggle friction, (m) toggle motor")
          self.textLine += 15

          torque = self.m_joint1.GetMotorTorque()
          self.DrawString(5, self.textLine, "Motor Torque = %.0f" % (torque))
          self.textLine += 15
          super(SliderCrank, self).Step(settings)
     
if __name__=="__main__":
     test_main.main(SliderCrank)
