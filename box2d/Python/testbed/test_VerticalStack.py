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
class VerticalStack (test_main.Framework):
    name="VerticalStack"
    m_bullet=None
    def __init__(self):
        super(VerticalStack, self).__init__()
        sd=box2d.b2PolygonDef()
        sd.SetAsBox(50.0, 10.0, box2d.b2Vec2(0.0, -10.0), 0.0)

        bd=box2d.b2BodyDef()
        bd.position.Set(0.0, 0.0)
        ground = self.world.CreateBody(bd) 
        ground.CreateShape(sd)

        sd.SetAsBox(0.1, 10.0, box2d.b2Vec2(20.0, 10.0), 0.0)
        ground.CreateShape(sd)

        xs = [0.0, -10.0, -5.0, 5.0, 10.0]

        for j in range(5):
            sd=box2d.b2PolygonDef()
            sd.SetAsBox(0.5, 0.5)
            sd.density = 1.0
            sd.friction = 0.3

            for i in range(12):
                bd=box2d.b2BodyDef()

                # For this test we are using continuous physics for all boxes.
                # This is a stress test, you normally wouldn't do this for
                # performance reasons.
                #bd.isBullet = True
                bd.allowSleep = True

                #x = b2Random(-0.1, 0.1)
                #x = i % 2 == 0 ? -0.025 : 0.025
                bd.position.Set(xs[j], 0.752 + 1.54 * i)
                #bd.position.Set(xs[j], 2.51 + 4.02 * i)
                body = self.world.CreateBody(bd) #

                body.CreateShape(sd)
                body.SetMassFromShapes()

        self.m_bullet = None 
     
    def Keyboard(self, key) :
        if key == K_COMMA:
            if self.m_bullet:
                self.world.DestroyBody(self.m_bullet)
                self.m_bullet = None

            sd=box2d.b2CircleDef()
            sd.density = 20.0
            sd.radius = 0.25
            sd.restitution = 0.05

            bd=box2d.b2BodyDef()
            bd.isBullet = True
            bd.allowSleep = False
            bd.position.Set(-31.0, 5.0)

            self.m_bullet = self.world.CreateBody(bd)
            self.m_bullet.CreateShape(sd)
            self.m_bullet.SetMassFromShapes()

            self.m_bullet.SetLinearVelocity(box2d.b2Vec2(400.0, 0.0))
     
    def Step(self, settings) :
          self.DrawString(5, self.textLine, "Press: (,) to launch a bullet.")
          self.textLine += 15

          super(VerticalStack, self).Step(settings)

if __name__=="__main__":
     test_main.main(VerticalStack)
