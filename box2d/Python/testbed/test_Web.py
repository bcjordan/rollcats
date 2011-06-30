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

# This tests distance joints, body destruction, and joint destruction.

class Web (test_main.Framework):
    name="Web"
    m_bodies=[]
    m_joints=[]
    def __init__(self):
        super(Web, self).__init__()
        sd=box2d.b2PolygonDef()
        sd.SetAsBox(50.0, 10.0)

        bd=box2d.b2BodyDef()
        bd.position.Set(0.0, -10.0)
        ground = self.world.CreateBody(bd)
        ground.CreateShape(sd)

        sd=box2d.b2PolygonDef()
        sd.SetAsBox(0.5, 0.5)
        sd.density = 5.0
        sd.friction = 0.2

        bd=box2d.b2BodyDef()

        bd.position.Set(-5.0, 5.0)
        self.m_bodies.append(self.world.CreateBody(bd))
        self.m_bodies[0].CreateShape(sd)
        self.m_bodies[0].SetMassFromShapes()

        bd.position.Set(5.0, 5.0)
        self.m_bodies.append(self.world.CreateBody(bd))
        self.m_bodies[1].CreateShape(sd)
        self.m_bodies[1].SetMassFromShapes()

        bd.position.Set(5.0, 15.0)
        self.m_bodies.append(self.world.CreateBody(bd))
        self.m_bodies[2].CreateShape(sd)
        self.m_bodies[2].SetMassFromShapes()

        bd.position.Set(-5.0, 15.0)
        self.m_bodies.append(self.world.CreateBody(bd))
        self.m_bodies[3].CreateShape(sd)
        self.m_bodies[3].SetMassFromShapes()

        jd=box2d.b2DistanceJointDef()
        p1=box2d.b2Vec2()
        p2=box2d.b2Vec2()
        d=box2d.b2Vec2()

        jd.frequencyHz = 4.0
        jd.dampingRatio = 0.5

        jd.body1 = ground
        jd.body2 = self.m_bodies[0]
        jd.localAnchor1.Set(-10.0, 10.0)
        jd.localAnchor2.Set(-0.5, -0.5)
        p1 = jd.body1.GetWorldPoint(jd.localAnchor1)
        p2 = jd.body2.GetWorldPoint(jd.localAnchor2)
        d = p2 - p1
        jd.length = d.Length()
        self.m_joints.append(self.world.CreateJoint(jd).getAsType())

        jd.body1 = ground
        jd.body2 = self.m_bodies[1]
        jd.localAnchor1.Set(10.0, 10.0)
        jd.localAnchor2.Set(0.5, -0.5)
        p1 = jd.body1.GetWorldPoint(jd.localAnchor1)
        p2 = jd.body2.GetWorldPoint(jd.localAnchor2)
        d = p2 - p1
        jd.length = d.Length()
        self.m_joints.append(self.world.CreateJoint(jd).getAsType())

        jd.body1 = ground
        jd.body2 = self.m_bodies[2]
        jd.localAnchor1.Set(10.0, 30.0)
        jd.localAnchor2.Set(0.5, 0.5)
        p1 = jd.body1.GetWorldPoint(jd.localAnchor1)
        p2 = jd.body2.GetWorldPoint(jd.localAnchor2)
        d = p2 - p1
        jd.length = d.Length()
        self.m_joints.append(self.world.CreateJoint(jd).getAsType())

        jd.body1 = ground
        jd.body2 = self.m_bodies[3]
        jd.localAnchor1.Set(-10.0, 30.0)
        jd.localAnchor2.Set(-0.5, 0.5)
        p1 = jd.body1.GetWorldPoint(jd.localAnchor1)
        p2 = jd.body2.GetWorldPoint(jd.localAnchor2)
        d = p2 - p1
        jd.length = d.Length()
        self.m_joints.append(self.world.CreateJoint(jd).getAsType())

        jd.body1 = self.m_bodies[0]
        jd.body2 = self.m_bodies[1]
        jd.localAnchor1.Set(0.5, 0.0)
        jd.localAnchor2.Set(-0.5, 0.0)
        p1 = jd.body1.GetWorldPoint(jd.localAnchor1)
        p2 = jd.body2.GetWorldPoint(jd.localAnchor2)
        d = p2 - p1
        jd.length = d.Length()
        self.m_joints.append(self.world.CreateJoint(jd).getAsType())

        jd.body1 = self.m_bodies[1]
        jd.body2 = self.m_bodies[2]
        jd.localAnchor1.Set(0.0, 0.5)
        jd.localAnchor2.Set(0.0, -0.5)
        p1 = jd.body1.GetWorldPoint(jd.localAnchor1)
        p2 = jd.body2.GetWorldPoint(jd.localAnchor2)
        d = p2 - p1
        jd.length = d.Length()
        self.m_joints.append(self.world.CreateJoint(jd).getAsType())

        jd.body1 = self.m_bodies[2]
        jd.body2 = self.m_bodies[3]
        jd.localAnchor1.Set(-0.5, 0.0)
        jd.localAnchor2.Set(0.5, 0.0)
        p1 = jd.body1.GetWorldPoint(jd.localAnchor1)
        p2 = jd.body2.GetWorldPoint(jd.localAnchor2)
        d = p2 - p1
        jd.length = d.Length()
        self.m_joints.append(self.world.CreateJoint(jd).getAsType())

        jd.body1 = self.m_bodies[3]
        jd.body2 = self.m_bodies[0]
        jd.localAnchor1.Set(0.0, -0.5)
        jd.localAnchor2.Set(0.0, 0.5)
        p1 = jd.body1.GetWorldPoint(jd.localAnchor1)
        p2 = jd.body2.GetWorldPoint(jd.localAnchor2)
        d = p2 - p1
        jd.length = d.Length()
        self.m_joints.append(self.world.CreateJoint(jd).getAsType())
     
    def Keyboard(self, key) :
        # Note: these functions are still causing some problems
        if key==K_b:
            for body in self.m_bodies:
                self.m_bodies.remove(body)
                self.world.DestroyBody(body)
                break

        elif key==K_j:
            for joint in self.m_joints:
                self.m_joints.remove(joint)
                self.world.DestroyJoint(joint)
                break

    def Step(self, settings) :
          self.DrawString(5, self.textLine, "This demonstrates a soft distance joint.")
          self.textLine += 15
          self.DrawString(5, self.textLine, "Press: (b) to delete a body, (j) to delete a joint")
          self.textLine += 15
          super(Web, self).Step(settings)
     
    def JointDestroyed(self, joint) :
        if joint in self.m_joints:
            print "Joint destroyed and removed from the list"
            self.m_joints.remove(joint)
        else:
            print "Joint destroyed but not found in list", joint
            # bug here? is this box2d's fault? it passes in shapes!

if __name__=="__main__":
     test_main.main(Web)
