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
class ShapeEditing (test_main.Framework):
    name="ShapeEditing"
    m_body=None
    m_shape1=None
    m_shape2=None
    def __init__(self):
        super(ShapeEditing, self).__init__()
        sd=box2d.b2PolygonDef()
        sd.SetAsBox(50.0, 10.0)

        bd=box2d.b2BodyDef()
        bd.position.Set(0.0, -10.0)

        ground = self.world.CreateBody(bd) #
        ground.CreateShape(sd)

        bodydef=box2d.b2BodyDef()
        bodydef.position.Set(0.0, 10.0)
        self.m_body = self.world.CreateBody(bodydef)

        sd=box2d.b2PolygonDef()
        sd.SetAsBox(4.0, 4.0, box2d.b2Vec2(0.0, 0.0), 0.0)
        sd.density = 10.0
        self.m_shape1 = self.m_body.CreateShape(sd)
        self.m_body.SetMassFromShapes()

        self.m_shape2 = None
             
    def Keyboard(self, key) :
        if key==K_c:
            if not self.m_shape2:
                sd=box2d.b2CircleDef()
                sd.radius = 3.0
                sd.density = 10.0
                sd.localPosition.Set(0.5, -4.0)
                self.m_shape2 = self.m_body.CreateShape(sd)
                self.m_body.SetMassFromShapes()
                self.m_body.WakeUp()

        elif key==K_d:
            if self.m_shape2:
                self.m_body.DestroyShape(self.m_shape2)
                self.m_shape2 = None
                self.m_body.SetMassFromShapes()
                self.m_body.WakeUp()

    def Step(self, settings) :
        self.DrawString(5, self.textLine, "Press: (c) create a shape, (d) destroy a shape.")
        self.textLine += 15
        super(ShapeEditing, self).Step(settings)

if __name__=="__main__":
     test_main.main(ShapeEditing)
