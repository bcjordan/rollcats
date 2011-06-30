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
class Car (test_main.Framework):
    name="Car"
    m_leftWheel=None
    m_rightWheel=None
    m_vehicle=None
    m_leftJoint=None
    m_rightJoint=None

    def __init__(self):
        super(Car, self).__init__()
        # car body
        poly1=box2d.b2PolygonDef()
        poly2=box2d.b2PolygonDef()

        # bottom half
        poly1.vertexCount = 5
        poly1.setVertex(4,-2.2,-0.74)
        poly1.setVertex(3,-2.2,0)
        poly1.setVertex(2,1.0,0)
        poly1.setVertex(1,2.2,-0.2)
        poly1.setVertex(0,2.2,-0.74)
        poly1.filter.groupIndex = -1

        poly1.density		= 20.0
        poly1.friction		= 0.68
        poly1.filter.groupIndex	= -1

        # top half
        poly2.vertexCount = 4
        poly2.setVertex(3,-1.7,0)
        poly2.setVertex(2,-1.3,0.7)
        poly2.setVertex(1,0.5,0.74)
        poly2.setVertex(0,1.0,0)
        poly2.filter.groupIndex = -1

        poly2.density		= 5.0
        poly2.friction		= 0.68
        poly2.filter.groupIndex	= -1

        bd=box2d.b2BodyDef() 
        bd.position.Set(-35.0, 2.8)

        self.m_vehicle = self.world.CreateBody(bd)
        self.m_vehicle.CreateShape(poly1)
        self.m_vehicle.CreateShape(poly2)
        self.m_vehicle.SetMassFromShapes()

        # vehicle wheels
        circ = box2d.b2CircleDef()
        circ.density = 40.0
        circ.radius = 0.38608
        circ.friction = 0.8
        circ.filter.groupIndex = -1

        bd=box2d.b2BodyDef() 
        bd.allowSleep = False
        bd.position.Set(-33.8, 2.0)

        self.m_rightWheel = self.world.CreateBody(bd)
        self.m_rightWheel.CreateShape(circ)
        self.m_rightWheel.SetMassFromShapes()

        bd.position.Set(-36.2, 2.0)
        self.m_leftWheel = self.world.CreateBody(bd)
        self.m_leftWheel.CreateShape(circ)
        self.m_leftWheel.SetMassFromShapes()

        # join wheels to chassis
        anchor=box2d.b2Vec2() 
        jd=box2d.b2RevoluteJointDef() 
        jd.Initialize(self.m_vehicle, self.m_leftWheel, self.m_leftWheel.GetWorldCenter())
        jd.collideConnected = False
        jd.enableMotor = True
        jd.maxMotorTorque = 10.0
        jd.motorSpeed = 0.0
        self.m_leftJoint = self.world.CreateJoint(jd).getAsType() 

        jd.Initialize(self.m_vehicle, self.m_rightWheel, self.m_rightWheel.GetWorldCenter())
        jd.collideConnected = False
        self.m_rightJoint = self.world.CreateJoint(jd).getAsType() 

        # ground
        box=box2d.b2PolygonDef() 
        box.SetAsBox(19.5, 0.5)
        box.friction = 0.62

        bd=box2d.b2BodyDef() 
        bd.position.Set(-25.0, 1.0)

        ground = self.world.CreateBody(bd) 
        ground.CreateShape(box)

        # more ground
        box=box2d.b2PolygonDef() 
        bd=box2d.b2BodyDef() 

        box.SetAsBox(9.5, 0.5, box2d.b2Vec2_zero, 0.1 * box2d.b2_pi)
        box.friction = 0.62
        bd.position.Set(27.0 - 30.0, 3.1)

        ground = self.world.CreateBody(bd) 
        ground.CreateShape(box)

        # more ground
        box=box2d.b2PolygonDef() 
        bd=box2d.b2BodyDef() 

        box.SetAsBox(9.5, 0.5, box2d.b2Vec2_zero, -0.1 * box2d.b2_pi)
        box.friction = 0.62
        bd.position.Set(55.0 - 30.0, 3.1)

        ground = self.world.CreateBody(bd) 
        ground.CreateShape(box)

        # more ground
        box=box2d.b2PolygonDef() 
        bd=box2d.b2BodyDef() 

        box.SetAsBox(9.5, 0.5, box2d.b2Vec2_zero, 0.03 * box2d.b2_pi)
        box.friction = 0.62
        bd.position.Set(41.0, 2.0)

        ground = self.world.CreateBody(bd) 
        ground.CreateShape(box)

        # more ground
        box=box2d.b2PolygonDef() 
        bd=box2d.b2BodyDef() 

        box.SetAsBox(5.0, 0.5, box2d.b2Vec2_zero, 0.15 * box2d.b2_pi)
        box.friction = 0.62
        bd.position.Set(50.0, 4.0)

        ground = self.world.CreateBody(bd) 
        ground.CreateShape(box)

        # more ground
        box=box2d.b2PolygonDef() 
        bd=box2d.b2BodyDef() 

        box.SetAsBox(20.0, 0.5)
        box.friction = 0.62
        bd.position.Set(85.0, 2.0)

        ground = self.world.CreateBody(bd) 
        ground.CreateShape(box)
     
    def Step(self, settings) :
        self.DrawString(5, self.textLine, "Keys: left = a, brake = s, right = d")
        self.textLine += 15

        super(Car, self).Step(settings)
     
    def Keyboard(self, key) :
        if key==K_a:
           self.m_leftJoint.SetMaxMotorTorque(800.0)
           self.m_leftJoint.SetMotorSpeed(12.0)
           
        elif key==K_s:
           self.m_leftJoint.SetMaxMotorTorque(100.0)
           self.m_leftJoint.SetMotorSpeed(0.0)
           
        elif key==K_d:
           self.m_leftJoint.SetMaxMotorTorque(1200.0)
           self.m_leftJoint.SetMotorSpeed(-36.0)
             
if __name__=="__main__":
     test_main.main(Car)
