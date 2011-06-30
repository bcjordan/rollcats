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


import test_main
from test_main import box2d
class TimeOfImpact (test_main.Framework):
    name="TimeOfImpact"
    m_body1=None
    m_body2=None
    m_shape1=None
    m_shape2=None
    def __init__(self):
        super(TimeOfImpact, self).__init__()
        sd=box2d.b2PolygonDef() 
        sd.density = 0.0

        sd.SetAsBox(0.1, 10.0, box2d.b2Vec2(10.0, 0.0), 0.0)

        bd=box2d.b2BodyDef() 
        bd.position.Set(0.0, 20.0)
        bd.angle = 0.0
        self.m_body1 = self.world.CreateBody(bd)
        self.m_shape1 = self.m_body1.CreateShape(sd)

        sd=box2d.b2PolygonDef() 
        sd.SetAsBox(0.25, 0.25)
        sd.density = 1.0

        bd=box2d.b2BodyDef() 
        bd.position.Set(9.6363468, 28.050615)
        bd.angle = 1.6408679
        self.m_body2 = self.world.CreateBody(bd)
        self.m_shape2 = self.m_body2.CreateShape(sd).getAsType()
        self.m_body2.SetMassFromShapes()

    def Step(self, settings) :
        sweep1=box2d.b2Sweep()
        sweep1.c0.Set(0.0, 20.0)
        sweep1.a0 = 0.0
        sweep1.c = sweep1.c0
        sweep1.a = sweep1.a0
        sweep1.t0 = 0.0
        sweep1.localCenter = self.m_body1.GetLocalCenter()

        sweep2=box2d.b2Sweep()
        sweep2.c0.Set(9.6363468, 28.050615)
        sweep2.a0 = 1.6408679
        sweep2.c = sweep2.c0 + box2d.b2Vec2(-0.075121880, 0.27358246)
        sweep2.a = sweep2.a0 - 10.434675
        sweep2.t0 = 0.0
        sweep2.localCenter = self.m_body2.GetLocalCenter()

        toi = box2d.b2TimeOfImpact(self.m_shape1, sweep1, self.m_shape2, sweep2)

        self.DrawString(5, self.textLine, "toi = %g" % (toi))
        self.textLine += 15

        xf2=box2d.b2XForm ()
        sweep2.GetXForm(xf2, toi)
        vertexCount = self.m_shape2.GetVertexCount()
        vertices = []

        localVertices = self.m_shape2.getVertices_b2Vec2()
        for vertex in localVertices:
            vertices.append( box2d.b2Mul(xf2, vertex).tuple() )

        self.debugDraw.DrawPolygon(vertices, vertexCount, box2d.b2Color(0.5, 0.7, 0.9))

        localVertices = self.m_shape2.getCoreVertices_b2Vec2()
        for vertex in localVertices:
            vertices.append( box2d.b2Mul(xf2, vertex).tuple() )
        self.debugDraw.DrawPolygon(vertices, vertexCount, box2d.b2Color(0.5, 0.7, 0.9))
     
        settings.pause = True
        super(TimeOfImpact, self).Step(settings)
        settings.pause = False

if __name__=="__main__":
     test_main.main(TimeOfImpact)
