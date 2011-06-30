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
class PolyCollision (test_main.Framework):
    name="PolyCollision"
    m_body1=None
    m_body2=None

    def __init__(self):
        super(PolyCollision, self).__init__()

        sd=box2d.b2PolygonDef() #box2d.b2PolygonDef sd
        sd.setVertex(0,-9.0, -1.1)
        sd.setVertex(1,7.0, -1.1)
        sd.setVertex(2,5.0, -0.9)
        sd.setVertex(3,-11.0, -0.9)
        sd.vertexCount = 4
        sd.density = 0.0

        bd=box2d.b2BodyDef() #box2d.b2BodyDef bd
        bd.position.Set(0.0, 10.0)
        self.m_body1 = self.world.CreateBody(bd)
        self.m_body1.CreateShape(sd)

        sd=box2d.b2PolygonDef() #box2d.b2PolygonDef sd
        sd.SetAsBox(0.5, 0.5)
        sd.density = 1.0

        bd=box2d.b2BodyDef() #box2d.b2BodyDef bd
        bd.position.Set(0.0, 10.0)
        self.m_body2 = self.world.CreateBody(bd)
        self.m_body2.CreateShape(sd)
        self.m_body2.SetMassFromShapes()

        self.world.SetGravity(box2d.b2Vec2_zero)
        self.world.SetPositionCorrection(False)
     
    def Step(self, settings) :
        settings.pause = True
        super(PolyCollision, self).Step(settings)
        settings.pause = False
     
    def Keyboard(self, key) :
          p = self.m_body2.GetPosition()
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
     test_main.main(PolyCollision)
