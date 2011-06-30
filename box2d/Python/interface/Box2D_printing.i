    %extend b2AABB {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2AABB(IsValid():%s lowerBound:%s upperBound:%s)" %\
                tuple([str(a) for a in (self.IsValid(),self.lowerBound,self.upperBound)])
        %}
    }

    %extend b2BlockAllocator {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2BlockAllocator()"
        %}
    }

    %extend b2Body {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2Body(GetAngle():%s GetAngularVelocity():%s GetInertia():%s GetLinearVelocity():%s GetLocalCenter():%s GetMass():%s GetPosition():%s GetWorldCenter():%s GetXForm():%s IsBullet():%s IsDynamic():%s IsFrozen():%s IsSleeping():%s IsStatic():%s)" %\
                tuple([str(a) for a in (self.GetAngle(),self.GetAngularVelocity(),self.GetInertia(),self.GetLinearVelocity(),self.GetLocalCenter(),self.GetMass(),self.GetPosition(),self.GetWorldCenter(),self.GetXForm(),self.IsBullet(),self.IsDynamic(),self.IsFrozen(),self.IsSleeping(),self.IsStatic())])
        %}
    }

    %extend b2BodyDef {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2BodyDef(allowSleep:%s angle:%s angularDamping:%s fixedRotation:%s isBullet:%s isSleeping:%s linearDamping:%s massData:%s position:%s userData:%s)" %\
                tuple([str(a) for a in (self.allowSleep,self.angle,self.angularDamping,self.fixedRotation,self.isBullet,self.isSleeping,self.linearDamping,self.massData,self.position,self.userData)])
        %}
    }

    %extend b2Bound {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2Bound(IsLower():%s IsUpper():%s proxyId:%s stabbingCount:%s value:%s)" %\
                tuple([str(a) for a in (self.IsLower(),self.IsUpper(),self.proxyId,self.stabbingCount,self.value)])
        %}
    }

    %extend b2BroadPhase {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2BroadPhase(m_bounds:%s m_freeProxy:%s m_pairManager:%s m_proxyCount:%s m_proxyPool:%s m_quantizationFactor:%s m_queryResultCount:%s m_queryResults:%s m_timeStamp:%s m_worldAABB:%s s_validate:%s)" %\
                tuple([str(a) for a in (self.m_bounds,self.m_freeProxy,self.m_pairManager,self.m_proxyCount,self.m_proxyPool,self.m_quantizationFactor,self.m_queryResultCount,self.m_queryResults,self.m_timeStamp,self.m_worldAABB,self.s_validate)])
        %}
    }

    %extend b2BufferedPair {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2BufferedPair(proxyId1:%s proxyId2:%s)" %\
                tuple([str(a) for a in (self.proxyId1,self.proxyId2)])
        %}
    }

    %extend b2CircleDef {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2CircleDef(density:%s filter:%s friction:%s isSensor:%s localPosition:%s radius:%s restitution:%s type:%s userData:%s)" %\
                tuple([str(a) for a in (self.density,self.filter,self.friction,self.isSensor,self.localPosition,self.radius,self.restitution,self.type,self.userData)])
        %}
    }

    %extend b2CircleShape {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2CircleShape(GetBody():%s GetFilterData():%s GetFriction():%s GetLocalPosition():%s GetRadius():%s GetRestitution():%s GetSweepRadius():%s GetType():%s IsSensor():%s)" %\
                tuple([str(a) for a in (self.GetBody(),self.GetFilterData(),self.GetFriction(),self.GetLocalPosition(),self.GetRadius(),self.GetRestitution(),self.GetSweepRadius(),self.GetType(),self.IsSensor())])
        %}
    }

    %extend b2Color {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2Color(b:%s g:%s r:%s)" %\
                tuple([str(a) for a in (self.b,self.g,self.r)])
        %}
    }

    %extend b2Contact {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2Contact(GetManifoldCount():%s GetManifolds():%s GetShape1():%s GetShape2():%s IsSolid():%s e_islandFlag:%s e_nonSolidFlag:%s e_slowFlag:%s e_toiFlag:%s m_flags:%s m_friction:%s m_manifoldCount:%s m_node1:%s m_node2:%s m_restitution:%s m_shape1:%s m_shape2:%s m_toi:%s s_initialized:%s s_registers:%s)" %\
                tuple([str(a) for a in (self.GetManifoldCount(),self.GetManifolds(),self.GetShape1(),self.GetShape2(),self.IsSolid(),self.e_islandFlag,self.e_nonSolidFlag,self.e_slowFlag,self.e_toiFlag,self.m_flags,self.m_friction,self.m_manifoldCount,self.m_node1,self.m_node2,self.m_restitution,self.m_shape1,self.m_shape2,self.m_toi,self.s_initialized,self.s_registers)])
        %}
    }

    %extend b2ContactEdge {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2ContactEdge(contact:%s other:%s)" %\
                tuple([str(a) for a in (self.contact,self.other)])
        %}
    }

    %extend b2ContactFilter {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2ContactFilter()"
        %}
    }

    %extend b2ContactID {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2ContactID(features:%s key:%s)" %\
                tuple([str(a) for a in (self.features,self.key)])
        %}
    }

    %extend b2ContactID_features {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2ContactID_features(flip:%s incidentEdge:%s incidentVertex:%s referenceEdge:%s)" %\
                tuple([str(a) for a in (self.flip,self.incidentEdge,self.incidentVertex,self.referenceEdge)])
        %}
    }

    %extend b2ContactManager {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2ContactManager(m_destroyImmediate:%s m_nullContact:%s m_world:%s)" %\
                tuple([str(a) for a in (self.m_destroyImmediate,self.m_nullContact,self.m_world)])
        %}
    }

    %extend b2ContactPoint {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2ContactPoint(friction:%s id:%s normal:%s position:%s restitution:%s separation:%s shape1:%s shape2:%s velocity:%s)" %\
                tuple([str(a) for a in (self.friction,self.id,self.normal,self.position,self.restitution,self.separation,self.shape1,self.shape2,self.velocity)])
        %}
    }

    %extend b2ContactRegister {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2ContactRegister(createFcn:%s destroyFcn:%s primary:%s)" %\
                tuple([str(a) for a in (self.createFcn,self.destroyFcn,self.primary)])
        %}
    }

    %extend b2ContactResult {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2ContactResult(id:%s normal:%s normalImpulse:%s position:%s shape1:%s shape2:%s tangentImpulse:%s)" %\
                tuple([str(a) for a in (self.id,self.normal,self.normalImpulse,self.position,self.shape1,self.shape2,self.tangentImpulse)])
        %}
    }

    %extend b2DistanceJoint {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2DistanceJoint(GetAnchor1():%s GetAnchor2():%s GetReactionForce():%s GetReactionTorque():%s GetType():%s m_bias:%s m_dampingRatio:%s m_frequencyHz:%s m_gamma:%s m_impulse:%s m_length:%s m_localAnchor1:%s m_localAnchor2:%s m_mass:%s m_u:%s)" %\
                tuple([str(a) for a in (self.GetAnchor1(),self.GetAnchor2(),self.GetReactionForce(),self.GetReactionTorque(),self.GetType(),self.m_bias,self.m_dampingRatio,self.m_frequencyHz,self.m_gamma,self.m_impulse,self.m_length,self.m_localAnchor1,self.m_localAnchor2,self.m_mass,self.m_u)])
        %}
    }

    %extend b2DistanceJointDef {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2DistanceJointDef(body1:%s body2:%s collideConnected:%s dampingRatio:%s frequencyHz:%s length:%s localAnchor1:%s localAnchor2:%s type:%s userData:%s)" %\
                tuple([str(a) for a in (self.body1,self.body2,self.collideConnected,self.dampingRatio,self.frequencyHz,self.length,self.localAnchor1,self.localAnchor2,self.type,self.userData)])
        %}
    }

    %extend b2FilterData {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2FilterData(categoryBits:%s groupIndex:%s maskBits:%s)" %\
                tuple([str(a) for a in (self.categoryBits,self.groupIndex,self.maskBits)])
        %}
    }

    %extend b2GearJoint {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2GearJoint(GetAnchor1():%s GetAnchor2():%s GetRatio():%s GetReactionForce():%s GetReactionTorque():%s GetType():%s m_J:%s m_constant:%s m_force:%s m_ground1:%s m_ground2:%s m_groundAnchor1:%s m_groundAnchor2:%s m_localAnchor1:%s m_localAnchor2:%s m_mass:%s m_prismatic1:%s m_prismatic2:%s m_ratio:%s m_revolute1:%s m_revolute2:%s)" %\
                tuple([str(a) for a in (self.GetAnchor1(),self.GetAnchor2(),self.GetRatio(),self.GetReactionForce(),self.GetReactionTorque(),self.GetType(),self.m_J,self.m_constant,self.m_force,self.m_ground1,self.m_ground2,self.m_groundAnchor1,self.m_groundAnchor2,self.m_localAnchor1,self.m_localAnchor2,self.m_mass,self.m_prismatic1,self.m_prismatic2,self.m_ratio,self.m_revolute1,self.m_revolute2)])
        %}
    }

    %extend b2GearJointDef {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2GearJointDef(body1:%s body2:%s collideConnected:%s joint1:%s joint2:%s ratio:%s type:%s userData:%s)" %\
                tuple([str(a) for a in (self.body1,self.body2,self.collideConnected,self.joint1,self.joint2,self.ratio,self.type,self.userData)])
        %}
    }

    %extend b2Jacobian {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2Jacobian(angular1:%s angular2:%s linear1:%s linear2:%s)" %\
                tuple([str(a) for a in (self.angular1,self.angular2,self.linear1,self.linear2)])
        %}
    }

    %extend b2Joint {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2Joint(GetAnchor1():%s GetAnchor2():%s GetReactionForce():%s GetReactionTorque():%s GetType():%s)" %\
                tuple([str(a) for a in (self.GetAnchor1(),self.GetAnchor2(),self.GetReactionForce(),self.GetReactionTorque(),self.GetType())])
        %}
    }

    %extend b2JointDef {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2JointDef(body1:%s body2:%s collideConnected:%s type:%s userData:%s)" %\
                tuple([str(a) for a in (self.body1,self.body2,self.collideConnected,self.type,self.userData)])
        %}
    }

    %extend b2JointEdge {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2JointEdge(joint:%s other:%s)" %\
                tuple([str(a) for a in (self.joint,self.other)])
        %}
    }

    %extend b2Manifold {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2Manifold(normal:%s pointCount:%s points:%s)" %\
                tuple([str(a) for a in (self.normal,self.pointCount,self.points)])
        %}
    }

    %extend b2ManifoldPoint {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2ManifoldPoint(id:%s localPoint1:%s localPoint2:%s normalImpulse:%s separation:%s tangentImpulse:%s)" %\
                tuple([str(a) for a in (self.id,self.localPoint1,self.localPoint2,self.normalImpulse,self.separation,self.tangentImpulse)])
        %}
    }

    %extend b2MassData {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2MassData(I:%s center:%s mass:%s)" %\
                tuple([str(a) for a in (self.I,self.center,self.mass)])
        %}
    }

    %extend b2Mat22 {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2Mat22(GetAngle():%s col1:%s col2:%s)" %\
                tuple([str(a) for a in (self.GetAngle(),self.col1,self.col2)])
        %}
    }

    %extend b2MouseJoint {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2MouseJoint(GetAnchor1():%s GetAnchor2():%s GetReactionForce():%s GetReactionTorque():%s GetType():%s m_C:%s m_beta:%s m_gamma:%s m_impulse:%s m_localAnchor:%s m_mass:%s m_maxForce:%s m_target:%s)" %\
                tuple([str(a) for a in (self.GetAnchor1(),self.GetAnchor2(),self.GetReactionForce(),self.GetReactionTorque(),self.GetType(),self.m_C,self.m_beta,self.m_gamma,self.m_impulse,self.m_localAnchor,self.m_mass,self.m_maxForce,self.m_target)])
        %}
    }

    %extend b2MouseJointDef {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2MouseJointDef(body1:%s body2:%s collideConnected:%s dampingRatio:%s frequencyHz:%s maxForce:%s target:%s timeStep:%s type:%s userData:%s)" %\
                tuple([str(a) for a in (self.body1,self.body2,self.collideConnected,self.dampingRatio,self.frequencyHz,self.maxForce,self.target,self.timeStep,self.type,self.userData)])
        %}
    }

    %extend b2NullContact {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2NullContact(GetManifoldCount():%s GetManifolds():%s GetShape1():%s GetShape2():%s IsSolid():%s e_islandFlag:%s e_nonSolidFlag:%s e_slowFlag:%s e_toiFlag:%s m_flags:%s m_friction:%s m_manifoldCount:%s m_node1:%s m_node2:%s m_restitution:%s m_shape1:%s m_shape2:%s m_toi:%s s_initialized:%s s_registers:%s)" %\
                tuple([str(a) for a in (self.GetManifoldCount(),self.GetManifolds(),self.GetShape1(),self.GetShape2(),self.IsSolid(),self.e_islandFlag,self.e_nonSolidFlag,self.e_slowFlag,self.e_toiFlag,self.m_flags,self.m_friction,self.m_manifoldCount,self.m_node1,self.m_node2,self.m_restitution,self.m_shape1,self.m_shape2,self.m_toi,self.s_initialized,self.s_registers)])
        %}
    }

    %extend b2OBB {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2OBB(R:%s center:%s extents:%s)" %\
                tuple([str(a) for a in (self.R,self.center,self.extents)])
        %}
    }

    %extend b2Pair {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2Pair(IsBuffered():%s IsFinal():%s IsRemoved():%s e_pairBuffered:%s e_pairFinal:%s e_pairRemoved:%s proxyId1:%s proxyId2:%s status:%s userData:%s)" %\
                tuple([str(a) for a in (self.IsBuffered(),self.IsFinal(),self.IsRemoved(),self.e_pairBuffered,self.e_pairFinal,self.e_pairRemoved,self.proxyId1,self.proxyId2,self.status,self.userData)])
        %}
    }

    %extend b2PairCallback {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2PairCallback()"
        %}
    }

    %extend b2PairManager {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2PairManager(m_broadPhase:%s m_callback:%s m_freePair:%s m_hashTable:%s m_pairBuffer:%s m_pairBufferCount:%s m_pairCount:%s m_pairs:%s)" %\
                tuple([str(a) for a in (self.m_broadPhase,self.m_callback,self.m_freePair,self.m_hashTable,self.m_pairBuffer,self.m_pairBufferCount,self.m_pairCount,self.m_pairs)])
        %}
    }

    %extend b2PolygonDef {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2PolygonDef(density:%s filter:%s friction:%s isSensor:%s restitution:%s type:%s userData:%s vertexCount:%s vertices:%s)" %\
                tuple([str(a) for a in (self.density,self.filter,self.friction,self.isSensor,self.restitution,self.type,self.userData,self.vertexCount,self.vertices)])
        %}
    }

    %extend b2PolygonShape {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2PolygonShape(GetBody():%s GetCentroid():%s GetCoreVertices():%s GetFilterData():%s GetFriction():%s GetNormals():%s GetOBB():%s GetRestitution():%s GetSweepRadius():%s GetType():%s GetVertexCount():%s IsSensor():%s)" %\
                tuple([str(a) for a in (self.GetBody(),self.GetCentroid(),self.GetCoreVertices(),self.GetFilterData(),self.GetFriction(),self.GetNormals(),self.GetOBB(),self.GetRestitution(),self.GetSweepRadius(),self.GetType(),self.GetVertexCount(),self.IsSensor())])
        %}
    }

    %extend b2PrismaticJoint {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2PrismaticJoint(GetAnchor1():%s GetAnchor2():%s GetJointSpeed():%s GetJointTranslation():%s GetLowerLimit():%s GetMotorForce():%s GetMotorSpeed():%s GetReactionForce():%s GetReactionTorque():%s GetType():%s GetUpperLimit():%s IsLimitEnabled():%s IsMotorEnabled():%s m_angularMass:%s m_enableLimit:%s m_enableMotor:%s m_force:%s m_limitForce:%s m_limitPositionImpulse:%s m_limitState:%s m_linearJacobian:%s m_linearMass:%s m_localAnchor1:%s m_localAnchor2:%s m_localXAxis1:%s m_localYAxis1:%s m_lowerTranslation:%s m_maxMotorForce:%s m_motorForce:%s m_motorJacobian:%s m_motorMass:%s m_motorSpeed:%s m_refAngle:%s m_torque:%s m_upperTranslation:%s)" %\
                tuple([str(a) for a in (self.GetAnchor1(),self.GetAnchor2(),self.GetJointSpeed(),self.GetJointTranslation(),self.GetLowerLimit(),self.GetMotorForce(),self.GetMotorSpeed(),self.GetReactionForce(),self.GetReactionTorque(),self.GetType(),self.GetUpperLimit(),self.IsLimitEnabled(),self.IsMotorEnabled(),self.m_angularMass,self.m_enableLimit,self.m_enableMotor,self.m_force,self.m_limitForce,self.m_limitPositionImpulse,self.m_limitState,self.m_linearJacobian,self.m_linearMass,self.m_localAnchor1,self.m_localAnchor2,self.m_localXAxis1,self.m_localYAxis1,self.m_lowerTranslation,self.m_maxMotorForce,self.m_motorForce,self.m_motorJacobian,self.m_motorMass,self.m_motorSpeed,self.m_refAngle,self.m_torque,self.m_upperTranslation)])
        %}
    }

    %extend b2PrismaticJointDef {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2PrismaticJointDef(body1:%s body2:%s collideConnected:%s enableLimit:%s enableMotor:%s localAnchor1:%s localAnchor2:%s localAxis1:%s lowerTranslation:%s maxMotorForce:%s motorSpeed:%s referenceAngle:%s type:%s upperTranslation:%s userData:%s)" %\
                tuple([str(a) for a in (self.body1,self.body2,self.collideConnected,self.enableLimit,self.enableMotor,self.localAnchor1,self.localAnchor2,self.localAxis1,self.lowerTranslation,self.maxMotorForce,self.motorSpeed,self.referenceAngle,self.type,self.upperTranslation,self.userData)])
        %}
    }

    %extend b2Proxy {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2Proxy(IsValid():%s lowerBounds:%s overlapCount:%s timeStamp:%s upperBounds:%s userData:%s)" %\
                tuple([str(a) for a in (self.IsValid(),self.lowerBounds,self.overlapCount,self.timeStamp,self.upperBounds,self.userData)])
        %}
    }

    %extend b2PulleyJoint {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2PulleyJoint(GetAnchor1():%s GetAnchor2():%s GetGroundAnchor1():%s GetGroundAnchor2():%s GetLength1():%s GetLength2():%s GetRatio():%s GetReactionForce():%s GetReactionTorque():%s GetType():%s m_constant:%s m_force:%s m_ground:%s m_groundAnchor1:%s m_groundAnchor2:%s m_limitForce1:%s m_limitForce2:%s m_limitMass1:%s m_limitMass2:%s m_limitPositionImpulse1:%s m_limitPositionImpulse2:%s m_limitState1:%s m_limitState2:%s m_localAnchor1:%s m_localAnchor2:%s m_maxLength1:%s m_maxLength2:%s m_positionImpulse:%s m_pulleyMass:%s m_ratio:%s m_state:%s m_u1:%s m_u2:%s)" %\
                tuple([str(a) for a in (self.GetAnchor1(),self.GetAnchor2(),self.GetGroundAnchor1(),self.GetGroundAnchor2(),self.GetLength1(),self.GetLength2(),self.GetRatio(),self.GetReactionForce(),self.GetReactionTorque(),self.GetType(),self.m_constant,self.m_force,self.m_ground,self.m_groundAnchor1,self.m_groundAnchor2,self.m_limitForce1,self.m_limitForce2,self.m_limitMass1,self.m_limitMass2,self.m_limitPositionImpulse1,self.m_limitPositionImpulse2,self.m_limitState1,self.m_limitState2,self.m_localAnchor1,self.m_localAnchor2,self.m_maxLength1,self.m_maxLength2,self.m_positionImpulse,self.m_pulleyMass,self.m_ratio,self.m_state,self.m_u1,self.m_u2)])
        %}
    }

    %extend b2PulleyJointDef {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2PulleyJointDef(body1:%s body2:%s collideConnected:%s groundAnchor1:%s groundAnchor2:%s length1:%s length2:%s localAnchor1:%s localAnchor2:%s maxLength1:%s maxLength2:%s ratio:%s type:%s userData:%s)" %\
                tuple([str(a) for a in (self.body1,self.body2,self.collideConnected,self.groundAnchor1,self.groundAnchor2,self.length1,self.length2,self.localAnchor1,self.localAnchor2,self.maxLength1,self.maxLength2,self.ratio,self.type,self.userData)])
        %}
    }

    %extend b2RevoluteJoint {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2RevoluteJoint(GetAnchor1():%s GetAnchor2():%s GetJointAngle():%s GetJointSpeed():%s GetLowerLimit():%s GetMotorSpeed():%s GetMotorTorque():%s GetReactionForce():%s GetReactionTorque():%s GetType():%s GetUpperLimit():%s IsLimitEnabled():%s IsMotorEnabled():%s m_enableLimit:%s m_enableMotor:%s m_limitForce:%s m_limitPositionImpulse:%s m_limitState:%s m_localAnchor1:%s m_localAnchor2:%s m_lowerAngle:%s m_maxMotorTorque:%s m_motorForce:%s m_motorMass:%s m_motorSpeed:%s m_pivotForce:%s m_pivotMass:%s m_referenceAngle:%s m_upperAngle:%s)" %\
                tuple([str(a) for a in (self.GetAnchor1(),self.GetAnchor2(),self.GetJointAngle(),self.GetJointSpeed(),self.GetLowerLimit(),self.GetMotorSpeed(),self.GetMotorTorque(),self.GetReactionForce(),self.GetReactionTorque(),self.GetType(),self.GetUpperLimit(),self.IsLimitEnabled(),self.IsMotorEnabled(),self.m_enableLimit,self.m_enableMotor,self.m_limitForce,self.m_limitPositionImpulse,self.m_limitState,self.m_localAnchor1,self.m_localAnchor2,self.m_lowerAngle,self.m_maxMotorTorque,self.m_motorForce,self.m_motorMass,self.m_motorSpeed,self.m_pivotForce,self.m_pivotMass,self.m_referenceAngle,self.m_upperAngle)])
        %}
    }

    %extend b2RevoluteJointDef {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2RevoluteJointDef(body1:%s body2:%s collideConnected:%s enableLimit:%s enableMotor:%s localAnchor1:%s localAnchor2:%s lowerAngle:%s maxMotorTorque:%s motorSpeed:%s referenceAngle:%s type:%s upperAngle:%s userData:%s)" %\
                tuple([str(a) for a in (self.body1,self.body2,self.collideConnected,self.enableLimit,self.enableMotor,self.localAnchor1,self.localAnchor2,self.lowerAngle,self.maxMotorTorque,self.motorSpeed,self.referenceAngle,self.type,self.upperAngle,self.userData)])
        %}
    }

    %extend b2Segment {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2Segment(p1:%s p2:%s)" %\
                tuple([str(a) for a in (self.p1,self.p2)])
        %}
    }

    %extend b2Shape {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2Shape(GetBody():%s GetFilterData():%s GetFriction():%s GetRestitution():%s GetSweepRadius():%s GetType():%s IsSensor():%s)" %\
                tuple([str(a) for a in (self.GetBody(),self.GetFilterData(),self.GetFriction(),self.GetRestitution(),self.GetSweepRadius(),self.GetType(),self.IsSensor())])
        %}
    }

    %extend b2ShapeDef {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2ShapeDef(density:%s filter:%s friction:%s isSensor:%s restitution:%s type:%s userData:%s)" %\
                tuple([str(a) for a in (self.density,self.filter,self.friction,self.isSensor,self.restitution,self.type,self.userData)])
        %}
    }

    %extend b2StackAllocator {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2StackAllocator(GetMaxAllocation():%s)" % (['self.GetMaxAllocation()'])
        %}
    }

    %extend b2StackEntry {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2StackEntry(data:%s size:%s usedMalloc:%s)" %\
                tuple([str(a) for a in (self.data,self.size,self.usedMalloc)])
        %}
    }

    %extend b2Sweep {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2Sweep(a:%s a0:%s c:%s c0:%s localCenter:%s t0:%s)" %\
                tuple([str(a) for a in (self.a,self.a0,self.c,self.c0,self.localCenter,self.t0)])
        %}
    }

    %extend b2TimeStep {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2TimeStep(dt:%s dtRatio:%s inv_dt:%s maxIterations:%s positionCorrection:%s warmStarting:%s)" %\
                tuple([str(a) for a in (self.dt,self.dtRatio,self.inv_dt,self.maxIterations,self.positionCorrection,self.warmStarting)])
        %}
    }

    %extend b2Version {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2Version(major:%s minor:%s revision:%s)" %\
                tuple([str(a) for a in (self.major,self.minor,self.revision)])
        %}
    }

    %extend b2World {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2World(GetBodyCount():%s GetContactCount():%s GetGroundBody():%s GetJointCount():%s GetPairCount():%s GetProxyCount():%s)" %\
                tuple([str(a) for a in (self.GetBodyCount(),self.GetContactCount(),self.GetGroundBody(),self.GetJointCount(),self.GetPairCount(),self.GetProxyCount())])
        %}
    }

    %extend b2XForm {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2XForm(R:%s position:%s)" %\
                tuple([str(a) for a in (self.R,self.position)])
        %}
    }

