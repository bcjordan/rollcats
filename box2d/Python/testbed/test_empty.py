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

class Empty(test_main.Framework):
    """You can use this class as an outline for your tests.

    """
    name = "Empty" # Name of the class to display
    def __init__(self):
        """ 
        Initialize all of your objects here.
        Be sure to call the Framework's initializer first.
        """
        super(Empty, self).__init__()

        # Initialize all of the objects


    def Keyboard(self, key):
        """
        The key is from pygame.locals.K_*
        (e.g., if key == K_z: ... )
        """
        pass

    def Step(self, settings):
        """Called upon every step.
        You should always call
         -> super(Your_Test_Class, self).Step(settings)
        at the _end_ of your function.
        """

        # do stuff
        self.DrawString(0,self.textLine,"*** Base your own testbeds on me! ***")
        self.textLine+=15

        super(Empty, self).Step(settings)

    def JointDestroyed(self, joint):
        """
        The joint passed in was removed.
        """
        pass


    def BoundaryViolated(self, body):
        """
        The body went out of the world's extents.
        """
        pass

if __name__=="__main__":
    test_main.main(Empty)

