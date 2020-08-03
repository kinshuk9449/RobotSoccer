from controller import Supervisor

TIME_STEP = 32

supervisor = Supervisor()

# do this once only
robot_node = supervisor.getFromDef("BALL")
trans_field = robot_node.getField("translation")

while supervisor.step(TIME_STEP) != -1:
    # this is done repeatedly
    values = trans_field.getSFVec3f()
    if (values[0] > 4.5 or values[0] < -4.5) and (values[2] > -0.75 and values[2] < 0.75):
        print("Ball is at position: %g %g %g" % (values[0], values[1], values[2]))
        INITIAL = [0, 0.07, 0]
        trans_field.setSFVec3f(INITIAL)
        robot_node.resetPhysics()
    else:
        if (values[0] > 4.5):
            print("Ball is at position: %g %g %g" % (values[0], values[1], values[2]))
            INITIAL = [4.5, 0.07, values[2]]
            robot_node.resetPhysics()
            trans_field.setSFVec3f(INITIAL)
        elif (values[0] < -4.5):
            print("Ball is at position: %g %g %g" % (values[0], values[1], values[2]))
            INITIAL = [-4.5, 0.07, values[2]]
            robot_node.resetPhysics()
            trans_field.setSFVec3f(INITIAL)
        elif (values[2] > 3):
            print("Ball is at position: %g %g %g" % (values[0], values[1], values[2]))
            INITIAL = [values[0], 0.07, 3]
            robot_node.resetPhysics()
            trans_field.setSFVec3f(INITIAL)
        elif (values[2] < -3):
            print("Ball is at position: %g %g %g" % (values[0], values[1], values[2]))
            INITIAL = [values[0], 0.07, -3]
            robot_node.resetPhysics()
            trans_field.setSFVec3f(INITIAL)