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
class DistanceTest (test_main.Framework):
    name="DistanceTest"
    m_body1=None
    m_body2=None
    m_shape1=None
    m_shape2=None
    def __init__(self):
        super(DistanceTest, self).__init__()
        sd=box2d.b2PolygonDef() 
        sd.SetAsBox(1.0, 1.0)
        sd.density = 0.0

        bd=box2d.b2BodyDef() 
        bd.position.Set(0.0, 10.0)
        self.m_body1 = self.world.CreateBody(bd)
        self.m_shape1 = self.m_body1.CreateShape(sd)

        sd=box2d.b2PolygonDef() 
        sd.vertexCount = 3
        sd.setVertex(0,-1.0, 0.0)
        sd.setVertex(1,1.0, 0.0)
        sd.setVertex(2,0.0, 15.0)
        sd.density = 1.0
        bd=box2d.b2BodyDef() 
        #bd.position.Set(-48.377853, 0.49244255)
        #bd.rotation = 90.475891
        bd.position.Set(0.0, 10.0)
        self.m_body2 = self.world.CreateBody(bd)
        self.m_shape2 = self.m_body2.CreateShape(sd)
        self.m_body2.SetMassFromShapes()

        self.world.SetGravity(box2d.b2Vec2(0.0, 0.0))
        self.world.SetPositionCorrection(False)
     
    def Step(self, settings) :
        x1=box2d.b2Vec2()
        x2=box2d.b2Vec2()
        distance = box2d.b2Distance(x1, x2, self.m_shape1, self.m_body1.GetXForm(), self.m_shape2, self.m_body2.GetXForm())

        self.DrawString(5, self.textLine, "distance = %g" % distance)
        self.textLine += 15

          # ?
          #g_GJK_Iterations = 5
          #self.DrawString(5, self.textLine, "iterations = %d" % g_GJK_Iterations)
          #self.textLine += 15
          
#          glPointSize(4.0)
#          glColor3(1.0, 0.0, 0.0)
#          glBegin(GL_POINTS)
#          glVertex2(x1.x, x1.y)
#          glVertex2(x2.x, x2.y)
#          glEnd()
#          glPointSize(1.0)
#          
#          glColor3(1.0, 1.0, 0.0)
#          glBegin(GL_LINES)
#          glVertex2(x1.x, x1.y)
#          glVertex2(x2.x, x2.y)
#          glEnd()

        settings.pause = True
        super(DistanceTest, self).Step(settings)
        settings.pause = False
     
    def Keyboard(self, key) :
        p = self.m_body2.GetPosition=box2d.b2Vec2()
        a = self.m_body2.GetAngle()

        if key==K_a:
           p.x -= 0.1
        elif key==K_d:
           p.x += 0.1
        elif key==K_s:
           p.y -= 0.1
        elif key==K_w:
           p.y += 0.1
        elif key==K_q:
           a += 0.1 * box2d.b2_pi
        elif key==K_e:
           a -= 0.1 * box2d.b2_pi
        self.m_body2.SetXForm(p, a)
     
if __name__=="__main__":
     test_main.main(DistanceTest)
