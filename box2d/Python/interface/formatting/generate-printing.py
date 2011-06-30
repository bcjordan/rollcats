import Box2D2 as box2d

#classes = ('b2AABB','b2BlockAllocator','b2Body','b2BodyDef','b2Bound','b2BoundaryListener','b2BroadPhase','b2BufferedPair','b2CircleDef','b2CircleShape','b2Color','b2Contact','b2ContactEdge','b2ContactFilter','b2ContactID','b2ContactID_features','b2ContactListener','b2ContactManager','b2ContactPoint','b2ContactRegister','b2ContactResult','b2DebugDraw','b2DestructionListener','b2DistanceJoint','b2DistanceJointDef','b2FilterData','b2GearJoint','b2GearJointDef','b2Jacobian','b2Joint','b2JointDef','b2JointEdge','b2Manifold','b2ManifoldPoint','b2MassData','b2Mat22','b2MouseJoint','b2MouseJointDef','b2NullContact','b2OBB','b2Pair','b2PairCallback','b2PairManager','b2PolygonDef','b2PolygonShape','b2PrismaticJoint','b2PrismaticJointDef','b2Proxy','b2PulleyJoint','b2PulleyJointDef','b2RevoluteJoint','b2RevoluteJointDef','b2Segment','b2Shape','b2ShapeDef','b2StackAllocator','b2StackEntry','b2Sweep','b2TimeStep','b2Vec2','b2Version','b2World','b2XForm')
classes = ('b2AABB','b2BlockAllocator','b2Body','b2BodyDef','b2Bound','b2BroadPhase','b2BufferedPair','b2CircleDef','b2CircleShape','b2Color','b2Contact','b2ContactEdge','b2ContactFilter','b2ContactID','b2ContactID_features','b2ContactManager','b2ContactPoint','b2ContactRegister','b2ContactResult','b2DistanceJoint','b2DistanceJointDef','b2FilterData','b2GearJoint','b2GearJointDef','b2Jacobian','b2Joint','b2JointDef','b2JointEdge','b2Manifold','b2ManifoldPoint','b2MassData','b2Mat22','b2MouseJoint','b2MouseJointDef','b2NullContact','b2OBB','b2Pair','b2PairCallback','b2PairManager','b2PolygonDef','b2PolygonShape','b2PrismaticJoint','b2PrismaticJointDef','b2Proxy','b2PulleyJoint','b2PulleyJointDef','b2RevoluteJoint','b2RevoluteJointDef','b2Segment','b2Shape','b2ShapeDef','b2StackAllocator','b2StackEntry','b2Sweep','b2TimeStep','b2Version','b2World','b2XForm')

def evaluate(name):
    """Return a rather verbose string representation of a joint"""
    ignoreList = ('this', 'thisown', 'next', 'prev', 'm_next', 'm_prev')
    ignoreAccessor = ('prev', 'next', 'jointlist', 'bodylist', 'shapelist', 'world', 'body1', 'body2', 'joint1', 'joint2')
    def checkArgs(prop):
        # uses a really stupid method of determining if it's really just an accessor
        # or if it's used like GetLocalPoint(). introspection like func_code doesn't seem
        # to work with swig
        doc = prop.__doc__
        if doc.find("->") == -1:
            return False
        lines = doc.split("->")
        if lines[0].find(",") > -1:
            return False
        return True
    def checkProperty(prop):
        if prop.lower() in ignoreList: return False
        if prop[:2]=="__": return False
        if callable(getattr(inst, prop)): 
            if prop[:3]=="Get":
                if prop[3:].lower() in ignoreAccessor: return False
            elif prop[:2]=="Is":
                if prop[2:].lower() in ignoreAccessor: return False
            else:
                return False
            # todo: see if arguments can be determined through introspection
            if not checkArgs(getattr(inst, prop)):
                return False
            prop += "()"
        return prop
    inst = getattr(box2d, name)
    props = []

    for prop in dir(inst):
        prop = checkProperty(prop)
        if prop:
            props.append(prop)

    props.sort()

    prop_strings  = ["%s:%%s" % prop for prop in props]
    value_strings = ["self.%s" % prop for prop in props]

    if len(value_strings) == 0:
        return '"%s()"' % name
    elif len(value_strings) == 1:
        return '"%s(%s)" %% (%s)' % (name, " ".join(prop_strings), value_strings)
    else:
        return '"%s(%s)" %%\\\n                tuple([str(a) for a in (%s)])' % (name, " ".join(prop_strings), ",".join(value_strings))


swig_template = open("printing-template.i", "r").read()

for c in classes:
    print swig_template % (c, evaluate(c))
