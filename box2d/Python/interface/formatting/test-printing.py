from Box2D2 import *

print "Creating world..."
worldAABB = b2AABB()
world = b2World(worldAABB, b2Vec2_zero, True)

print "Testing pretty printing..."
test=b2AABB(); print test, "\n"
test=b2BlockAllocator(); print test, "\n"
test=b2BodyDef(); print test, "\n"
body = world.CreateBody(test)
print body, "\n"

test=b2Bound(); print test, "\n"
#test=b2BroadPhase(worldAABB); print test, "\n"
test=b2BufferedPair(); print test, "\n"
test=b2CircleDef(); print test, "\n"
#test=b2CircleShape(); print test, "\n"
test.radius, test.density = 1, 1
shape=body.CreateShape(test)
print shape, "\n"
shape = shape.getAsType()
print shape, "\n"
body.SetMassFromShapes()

test=b2Color(); print test, "\n"
#test=b2Contact(); print test, "\n"
test=b2ContactEdge(); print test, "\n"
test=b2ContactFilter(); print test, "\n"
test=b2ContactID(); print test, "\n"
test=b2ContactID_features(); print test, "\n"
#? test=b2ContactManager(); print test, "\n"
test=b2ContactPoint(); print test, "\n"
test=b2ContactRegister(); print test, "\n"
#? test=b2ContactResult(); print test, "\n"
#test=b2DistanceJoint(); print test, "\n"
test=b2DistanceJointDef(); print test, "\n"
test.body1, test.body2 = body, body
joint=world.CreateJoint(test).getAsType(); print joint, "\n"

test=b2FilterData(); print test, "\n"

test=b2Jacobian(); print test, "\n"
#test=b2Joint(); print test, "\n"
test=b2JointDef(); print test, "\n"
test=b2JointEdge(); print test, "\n"
test=b2Manifold(); print test, "\n"
test=b2ManifoldPoint(); print test, "\n"
test=b2MassData(); print test, "\n"
test=b2Mat22(); print test, "\n"
#test=b2MouseJoint(); print test, "\n"
test=b2MouseJointDef(); print test, "\n"
test.body1, test.body2= world.GetGroundBody(), body
test.maxForce= 1000.0 * body.GetMass()
joint=world.CreateJoint(test).getAsType(); print joint, "\n"

test=b2NullContact(); print test, "\n"
test=b2OBB(); print test, "\n"
test=b2Pair(); print test, "\n"
#test=b2PairCallback(); print test, "\n"
#? test=b2PairManager(); print test, "\n"
test=b2PolygonDef(); print test, "\n"
#test=b2PolygonShape(); print test, "\n"
#test=b2PrismaticJoint(); print test, "\n"
test=b2PrismaticJointDef(); print test, "\n"
test.body1, test.body2= world.GetGroundBody(), body
joint=world.CreateJoint(test).getAsType(); print joint, "\n"

test=b2Proxy(); print test, "\n"
#test=b2PulleyJoint(); print test, "\n"
test=b2PulleyJointDef(); print test, "\n"
#test=b2RevoluteJoint(); print test, "\n"
test=b2RevoluteJointDef(); print test, "\n"
test.body1, test.body2 = world.GetGroundBody(), world.GetGroundBody()
joint=world.CreateJoint(test).getAsType(); print joint, "\n"

test=b2GearJointDef(); print test, "\n"
test.body1, test.body2 = world.GetGroundBody(), body
test.joint1, test.joint2 = joint, joint
joint=world.CreateJoint(test).getAsType(); print joint, "\n"

test=b2Segment(); print test, "\n"
#test=b2Shape(); print test, "\n"
test=b2ShapeDef(); print test, "\n"
test=b2StackAllocator(); print test, "\n"
test=b2StackEntry(); print test, "\n"
test=b2Sweep(); print test, "\n"
test=b2TimeStep(); print test, "\n"
test=b2Vec2(); print test, "\n"
test=b2Version(); print test, "\n"
#test=b2World(); print test, "\n"
print world, "\n"
test=b2XForm(); print test, "\n"
