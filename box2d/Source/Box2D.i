/*
* Python SWIG interface file for Box2D (www.box2d.org)
*
* Copyright (c) 2008 kne / sirkne at gmail dot com
* 
* This software is provided 'as-is', without any express or implied
* warranty.  In no event will the authors be held liable for any damages
* arising from the use of this software.
* Permission is granted to anyone to use this software for any purpose,
* including commercial applications, and to alter it and redistribute it
* freely, subject to the following restrictions:
* 1. The origin of this software must not be misrepresented; you must not
* claim that you wrote the original software. If you use this software
* in a product, an acknowledgment in the product documentation would be
* appreciated but is not required.
* 2. Altered source versions must be plainly marked as such, and must not be
* misrepresented as being the original software.
* 3. This notice may not be removed or altered from any source distribution.
*/

%module(directors="1") Box2D2
%{
    #include "../Include/Box2D.h"
    
    //Define these functions so that SWIG does not fail
    void b2BroadPhase::ValidatePairs() { }
%}

#ifdef SWIGPYTHON
    %inline %{
        bool __b2PythonJointPointerEquals__(b2Joint* a, b2Joint* b) {
            return a==b;
        }
        bool __b2PythonBodyPointerEquals__(b2Body* a, b2Body* b) {
            return a==b;
        }
        bool __b2PythonShapePointerEquals__(b2Shape* a, b2Shape* b) {
            return a==b;
        }
    %}

    #ifdef TARGET_FLOAT32_IS_FIXED
        //figure out what to do here :)
        %include "Box2D_fixed.i"
    #endif

    %include "Box2D_printing.i"

    //Autodoc puts the basic docstrings for each function
    %feature("autodoc", "1");

    //Add callback support for the following classes:
    %feature("director") b2ContactListener;
    %feature("director") b2ContactFilter;
    %feature("director") b2BoundaryListener;
    %feature("director") b2DestructionListener;
    %feature("director") b2DebugDraw;

    //These operators do not work unless explicitly defined like this 
    %rename(b2add) operator  + (const b2Vec2& a, const b2Vec2& b);
    %rename(b2add) operator  + (const b2Mat22& A, const b2Mat22& B);
    %rename(b2sub) operator  - (const b2Vec2& a, const b2Vec2& b);
    %rename(b2mul) operator  * (float32 s, const b2Vec2& a);
    %rename(b2equ) operator == (const b2Vec2& a, const b2Vec2& b);
    
    //Since Python (apparently) requires __imul__ to return self,
    //these void operators will not do. So, rename them, then call them
    //with Python code, and return self. (see further down in b2Vec2)
    %rename(add_vector) b2Vec2::operator += (const b2Vec2& v);
    %rename(sub_vector) b2Vec2::operator -= (const b2Vec2& v);
    %rename(mul_float ) b2Vec2::operator *= (float32 a);

    //Allow access to (m_)userData
    %typemap(in) void* userData, void* m_userData {
        //In
        if ($input == Py_None) {
            $1 = NULL;
        } else {
            $1 = (void*)( $input );
            Py_INCREF($input);
        }
    }

    %typemap(out) void* userData, void* m_userData {
        //Out
        if ($1 == NULL) {
            $result = Py_None;
        } else {
            $result = (PyObject*)( $1 );
        }
        Py_INCREF($result);
    }


    %extend b2World {
    public:
        PyObject* Query(const b2AABB& aabb, uint32 maxCount) {
            PyObject* ret=Py_None;
            b2Shape** shapes=(b2Shape**)malloc(maxCount * sizeof(b2Shape*));

            if (!shapes) {
                PyErr_SetString(PyExc_MemoryError, "Insufficient memory");
                return ret;
            }

            int32 num=$self->Query(aabb, shapes, maxCount);
            if (num < 0)
                num = 0;

            ret = PyTuple_New(2);
            
            PyObject* shapeList=PyTuple_New(num);
            PyObject* shape;

            for (int i=0; i < num; i++) {
                shape=SWIG_NewPointerObj(SWIG_as_voidptr(shapes[i]), SWIGTYPE_p_b2Shape, 0 );
                PyTuple_SetItem(shapeList, i, shape);
            }

            PyTuple_SetItem(ret, 0, SWIG_From_int(num));
            PyTuple_SetItem(ret, 1, shapeList);

            free(shapes);
            return ret;
        }
    }
        
    %typemap(directorin) b2Vec2* vertices {
        $input = PyTuple_New(vertexCount);
        PyObject* vertex;
        for (int i=0; i < vertexCount; i++) {
            vertex = PyTuple_New(2);
            PyTuple_SetItem(vertex, 0, PyFloat_FromDouble((float32)vertices[i].x));
            PyTuple_SetItem(vertex, 1, PyFloat_FromDouble((float32)vertices[i].y));

            PyTuple_SetItem($input, i, vertex);
        }
    }

    %feature("shadow") GetUserData {
        def GetUserData(self): # override the C++ version as it does not work. 
            """Get the specified userData (m_userData)"""
            return self.pyGetUserData()
    }

    %feature("shadow") SetUserData {
        def SetUserData(self, value): # override the C++ version as it does not work. 
            """Get the specified userData (m_userData)"""
            return self.pySetUserData(value)
    }

    //Typecast the shape as necessary so Python can use them properly (2.0)
    %extend b2Shape {
    public:
        %pythoncode %{
        __eq__ = b2ShapeCompare
        def typeName(self):
            types = {  e_unknownShape   : "Unknown",
                        e_circleShape   : "Circle",
                        e_polygonShape  : "Polygon",
                        e_shapeTypeCount: "ShapeType" }
            return types[self.GetType()]
        def getAsType(self):
            """Return a typecasted version of the shape"""
            return (getattr(self, "as%s" % self.typeName())) ()
        %}
        b2CircleShape* asCircle() {
            if ($self->GetType()==e_circleShape)
                return (b2CircleShape*)$self;
            return NULL;
        }
        b2PolygonShape* asPolygon() {
            if ($self->GetType()==e_polygonShape)
                return (b2PolygonShape*)$self;
            return NULL;
        }
        PyObject* pyGetUserData() {
            PyObject* ret=(PyObject*)self->GetUserData();
            Py_INCREF(ret);
            return ret;
        }
        void pySetUserData(PyObject* value) {
            self->SetUserData((void*)value);
            Py_INCREF(value);
        }
    }
   
    //Support using == on bodies, joints, and shapes
    %pythoncode %{
        def b2ShapeCompare(a, b):
            if not isinstance(a, b2Shape) or not isinstance(b, b2Shape):
                return False
            return __b2PythonShapePointerEquals__(a, b)
        def b2BodyCompare(a, b):
            if not isinstance(a, b2Body) or not isinstance(b, b2Body):
                return False
            return __b2PythonBodyPointerEquals__(a, b)
        def b2JointCompare(a, b):
            if not isinstance(a, b2Joint) or not isinstance(b, b2Joint):
                return False
            return __b2PythonJointPointerEquals__(a, b)
    %}

    %extend b2MouseJoint {
    public:
        %pythoncode %{
        __eq__ = b2JointCompare
        %}
    }

    %extend b2GearJoint {
    public:
        %pythoncode %{
        __eq__ = b2JointCompare
        %}
    }

    %extend b2DistanceJoint {
    public:
        %pythoncode %{
        __eq__ = b2JointCompare
        %}
    }

    %extend b2PrismaticJoint {
    public:
        %pythoncode %{
        __eq__ = b2JointCompare
        %}
    }
 
   %extend b2PulleyJoint {
    public:
        %pythoncode %{
        __eq__ = b2JointCompare
        %}
    }

   %extend b2RevoluteJoint {
    public:
        %pythoncode %{
        __eq__ = b2JointCompare
        %}
    }

    %include "Dynamics/Joints/b2Joint.h"

    %extend b2JointDef {
    public:
        %pythoncode %{
        def typeName(self):
            """
            Return the name of the joint from:
             Unknown, Mouse, Gear, Distance, Prismatic, Pulley, Revolute
            """
            types = { e_unknownJoint  : "Unknown",
                      e_mouseJoint    : "Mouse", 
                      e_gearJoint     : "Gear",
                      e_distanceJoint : "Distance",
                      e_prismaticJoint: "Prismatic",
                      e_pulleyJoint   : "Pulley",
                      e_revoluteJoint : "Revolute" }
            return types[self.type]
        %}
    }

    %extend b2Joint {
    public:
        %pythoncode %{
        __eq__ = b2JointCompare
        def typeName(self):
            """
            Return the name of the joint from:
             Unknown, Mouse, Gear, Distance, Prismatic, Pulley, Revolute
            """
            types = { e_unknownJoint  : "Unknown",
                      e_mouseJoint    : "Mouse", 
                      e_gearJoint     : "Gear",
                      e_distanceJoint : "Distance",
                      e_prismaticJoint: "Prismatic",
                      e_pulleyJoint   : "Pulley",
                      e_revoluteJoint : "Revolute" }
            return types[self.GetType()]
        def getAsType(self):
            """
            Return a typecasted version of the joint
            """
            return (getattr(self, "as%sJoint" % self.typeName())) ()
        %}
        PyObject* pyGetUserData() {
            PyObject* ret=(PyObject*)self->GetUserData();
            Py_INCREF(ret);
            return ret;
        }
        void pySetUserData(PyObject* value) {
            self->SetUserData((void*)value);
            Py_INCREF(value);
        }

        b2MouseJoint* asMouseJoint() {
            if ($self->GetType()==e_mouseJoint)
                return (b2MouseJoint*)$self;
            return NULL;
        }

        b2GearJoint* asGearJoint() {
            if ($self->GetType()==e_gearJoint)
                return (b2GearJoint*)$self;
            return NULL;
        }

        b2DistanceJoint* asDistanceJoint() {
            if ($self->GetType()==e_distanceJoint)
                return (b2DistanceJoint*)$self;
            return NULL;
        }

        b2PrismaticJoint* asPrismaticJoint() {
            if ($self->GetType()==e_prismaticJoint)
                return (b2PrismaticJoint*)$self;
            return NULL;
        }

        b2PulleyJoint* asPulleyJoint() {
            if ($self->GetType()==e_pulleyJoint)
                return (b2PulleyJoint*)$self;
            return NULL;
        }

        b2RevoluteJoint* asRevoluteJoint() {
            if ($self->GetType()==e_revoluteJoint)
                return (b2RevoluteJoint*)$self;
            return NULL;
        }
    }

    %ignore b2PolygonShape::GetVertices; //Inaccessible 

    %extend b2CircleShape {
    public:
        %pythoncode %{
        __eq__ = b2ShapeCompare
        %}
    }

    //Let python access all the vertices in the b2PolygonDef/Shape
    %extend b2PolygonShape {
    public:
        %pythoncode %{
        __eq__ = b2ShapeCompare
        def __repr__(self):
            return "b2PolygonShape(vertices: %s count: %d)" % (self.getVertices_tuple(), self.GetVertexCount())
        def getCoreVertices_tuple(self):
            """Returns all of the core vertices as a list of tuples [ (x1,y1), (x2,y2) ... (xN,yN) ]"""
            vertices = []
            for i in range(0, self.GetVertexCount()):
                vertices.append( (self.getCoreVertex(i).x, self.getCoreVertex(i).y ) )
            return vertices
        def getCoreVertices_b2Vec2(self):
            """Returns all of the core vertices as a list of b2Vec2's [ (x1,y1), (x2,y2) ... (xN,yN) ]"""
            vertices = []
            for i in range(0, self.GetVertexCount()):
                vertices.append(self.getCoreVertex(i))
            return vertices
        def getVertices_tuple(self):
            """Returns all of the vertices as a list of tuples [ (x1,y1), (x2,y2) ... (xN,yN) ]"""
            vertices = []
            for i in range(0, self.GetVertexCount()):
                vertices.append( (self.getCoreVertex(i).x, self.getCoreVertex(i).y ) )
            return vertices
        def getVertices_b2Vec2(self):
            """Returns all of the vertices as a list of b2Vec2's [ (x1,y1), (x2,y2) ... (xN,yN) ]"""
            vertices = []
            for i in range(0, self.GetVertexCount()):
                vertices.append(self.getVertex(i))
            return vertices
        %}
        const b2Vec2* getVertex(uint16 vnum) {
            if (vnum > b2_maxPolygonVertices || vnum > self->GetVertexCount()) return NULL;
            return &( $self->GetVertices() [vnum] );
        }
        const b2Vec2* getCoreVertex(uint16 vnum) {
            if (vnum > b2_maxPolygonVertices || vnum > self->GetVertexCount()) return NULL;
            return &( $self->GetCoreVertices() [vnum] );
        }
    }
    
    %extend b2PolygonDef{
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2PolygonDef(vertices: %s count: %d)" % (self.getVertices_tuple(), self.vertexCount)
        def checkValues(self):
            return b2PythonCheckPolygonDef(self)
        def getVertices_tuple(self):
            """Returns all of the vertices as a list of tuples [ (x1,y1), (x2,y2) ... (xN,yN) ]"""
            vertices = []
            for i in range(0, self.vertexCount):
                vertices.append( (self.getVertex(i).x, self.getVertex(i).y ) )
            return vertices
        def getVertices_b2Vec2(self):
            """Returns all of the vertices as a list of b2Vec2's [ (x1,y1), (x2,y2) ... (xN,yN) ]"""
            vertices = []
            for i in range(0, self.vertexCount):
                vertices.append(self.getVertex(i))
            return vertices
        def setVertices_tuple(self, vertices):
            """Sets all of the vertices (up to b2_maxPolygonVertices) given a tuple 
                in the format ( (x1,y1), (x2,y2) ... (xN,yN) )"""
            if len(vertices) > b2_maxPolygonVertices:
                raise ValueError
            self.vertexCount = len(vertices)
            for i in range(0, self.vertexCount):
                self.setVertex(i, vertices[i][0], vertices[i][1])
        def setVertices_b2Vec2(self, vertices):
            """Sets all of the vertices (up to b2_maxPolygonVertices) given a tuple 
                in the format ( (x1,y1), (x2,y2) ... (xN,yN) ) where each vertex
                is a b2Vec2"""
            if len(vertices) > b2_maxPolygonVertices:
                raise ValueError
            self.vertexCount = len(vertices)
            for i in range(0, self.vertexCount):
                self.setVertex(i, vertices[i])
        %}
        b2Vec2* getVertex(uint16 vnum) {
            if (vnum > b2_maxPolygonVertices || vnum > self->vertexCount) return NULL;
            return &( $self->vertices[vnum] );
        }
        void setVertex(uint16 vnum, b2Vec2& value) {
            if (vnum > b2_maxPolygonVertices) return;
            $self->vertices[vnum].Set(value.x, value.y);
        }
        void setVertex(uint16 vnum, float32 x, float32 y) {
            if (vnum > b2_maxPolygonVertices) return;
            $self->vertices[vnum].Set(x, y);
        }
    }

    //Extend the vector class to support Python print statements
    //Also, add vector addition and scalar multiplication
    %extend b2Vec2 {
        %pythoncode %{
        def __repr__(self):
            return "b2Vec2(%g,%g)" % (self.x, self.y)
        def tuple(self):
            """
            Return the vector as a tuple (x,y)
            """
            return (self.x, self.y)
        def fromTuple(self, tuple):
            """
            Set the vector to the values found in the tuple (x,y)
            """
            self.x, self.y = tuple
            return self
        def copy(self):
            """
            Return a copy of the vector.
            Remember that the following:
                a = b2Vec2()
                b = a
            Does not copy the vector itself, but b now refers to a.
            """
            return b2Vec2(self.x, self.y)
        def __iadd__(self, other):
            self.add_vector(other)
            return self
        def __isub__(self, other):
            self.sub_vector(other)
            return self
        def __imul__(self, a):
            self.mul_float(a)
            return self
        def __idiv__(self, a):
            self.div_float(a)
            return self

        %}
        b2Vec2 __div__(float32 a) { //convenience function
            return b2Vec2($self->x / a, $self->y / a);
        }
        b2Vec2 __mul__(float32 a) {
            return b2Vec2($self->x * a, $self->y * a);
        }
        b2Vec2 __add__(b2Vec2* other) {
            return b2Vec2($self->x + other->x, $self->y + other->y);
        }
        b2Vec2 __sub__(b2Vec2* other) {
            return b2Vec2($self->x - other->x, $self->y - other->y);
        }

        b2Vec2 __rmul__(float32 a) {
            return b2Vec2($self->x * a, $self->y * a);
        }
        b2Vec2 __rdiv__(float32 a) { //perhaps not _correct_, but convenient
            return b2Vec2($self->x / a, $self->y / a);
        }
        void div_float(float32 a) {
            self->x /= a;
            self->y /= a;
        }
    }

    %extend b2Body {
        %pythoncode %{
        __eq__ = b2BodyCompare
        %}
        PyObject* pyGetUserData() {
            PyObject* ret=(PyObject*)self->GetUserData();
            Py_INCREF(ret);
            return ret;
        }
        void pySetUserData(PyObject* value) {
            self->SetUserData((void*)value);
            Py_INCREF(value);
        }
    }

    // Additional supporting code
    %pythoncode %{
    # Checks the Polygon definition to see if upon creation it will cause an assertion.
    # Raises ValueError if an assertion would be raised.
    FLT_EPSILON = 1.192092896e-07
    def b2PythonComputeCentroid(pd):
        """
            Computes the centroid of the polygon shape definition, pd.
            Raises ValueError on an invalid vertex count or a small area.

            Ported from the Box2D C++ code.
        """
        count = pd.vertexCount

        if count < 3:
            raise ValueError, "ComputeCentroid: vertex count < 3"

        c = b2Vec2(0, 0)
        area = 0.0

        # pRef is the reference point for forming triangles.
        # It's location doesn't change the result (except for rounding error).
        pRef = b2Vec2(0.0, 0.0)

        inv3 = 1.0 / 3.0

        for i in range(count):
            # Triangle vertices.
            p1 = pRef
            p2 = pd.getVertex(i)
            if i + 1 < count: 
                p3 = pd.getVertex(i+1)
            else: p3 = pd.getVertex(0)

            e1 = p2 - p1
            e2 = p3 - p1

            D = b2Cross(e1, e2)

            triangleArea = 0.5 * D
            area += triangleArea

            # Area weighted centroid
            c += triangleArea * inv3 * (p1 + p2 + p3)

        # Centroid
        if area < FLT_EPSILON:
            raise ValueError, "ComputeCentroid: area < FLT_EPSILON"

        return c / area

    def b2PythonCheckPolygonDef(pd):
        """
            Checks the Polygon definition to see if upon creation it will cause an assertion.
            Raises ValueError if an assertion would be raised.

            Ported from the Box2D C++ code for CreateShape().
        """

        if pd.vertexCount < 3 or pd.vertexCount > b2_maxPolygonVertices:
            raise ValueError, "Invalid vertexCount"

        threshold = FLT_EPSILON * FLT_EPSILON
        verts = pd.getVertices_b2Vec2()
        normals = []
        v0 = verts[0]
        for i in range(pd.vertexCount):
            if i == pd.vertexCount-1:
                v1 = verts[0]
            else: v1 = verts[i+1]
            edge=v1 - v0
            if edge.LengthSquared() < threshold:
                raise ValueError, "edge.LengthSquared < FLT_EPSILON**2" 
            normals.append( b2Cross(edge, 1.0) )
            normals[-1].Normalize()
            v0=v1

        centroid = b2PythonComputeCentroid(pd)

        d=b2Vec2()
        for i in range(pd.vertexCount):
            i1 = i - 1 
            if i1 < 0: i1 = pd.vertexCount - 1
            i2 = i
            n1 = normals[i1]
            n2 = normals[i2]
            v = verts[i] - centroid

            d.x = b2Dot(n1, v) - b2_toiSlop
            d.y = b2Dot(n2, v) - b2_toiSlop

            # Shifting the edge inward by b2_toiSlop should
            # not cause the plane to pass the centroid.

            # Your shape has a radius/extent less than b2_toiSlop.
            if d.x < 0.0 or d.y <= 0.0: 
                raise ValueError, "Your shape has a radius/extent less than b2_toiSlop."

            A = b2Mat22()
            A.col1.x = n1.x; A.col2.x = n1.y
            A.col1.y = n2.x; A.col2.y = n2.y
            #coreVertices[i] = A.Solve(d) + m_centroid

        return True
    %}
#endif

%include "../Include/Box2D.h"


