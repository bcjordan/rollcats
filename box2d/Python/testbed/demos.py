import os
import pygame
import Box2D2 as box2d
from pygame.locals import *
from settings import fwSettings
from pgu import gui
from test_main import fwDebugDraw

global width, height
width, height = 640, 480
from distutils import sysconfig

def main():
    #gui initialization

    screen = pygame.display.set_mode((width,height))

    caption= "Python Box2D Testbed Demos"
    pygame.display.set_caption(caption)

    theme = gui.Theme("default")
    app = gui.Desktop(theme=theme)

    app.connect(gui.QUIT,app.quit,None)

    main = gui.Container(width=width, height=height)

    main.add(gui.Label("Box2D Testbed Demos", cls="h1"), 20, 20)

    list_size= (width / 2, height / 2)
    list_pos = (width/2 - list_size[0]/2, height/2 - list_size[1]/2)

    demolist = gui.List(width=list_size[0], height=list_size[1])
    main.add(demolist, list_pos[0], list_pos[1])

    add_demos(demolist)

    buttonw = (list_size[0]/2-20)
    bottom = list_pos[1]+list_size[1]+20

    b = gui.Button("Run", width=buttonw)
    main.add(b, list_pos[0], bottom)
    b.connect(gui.CLICK, run_demo, demolist)

    b = gui.Button("Quit", width=buttonw)
    main.add(b, list_pos[0]+buttonw+30, bottom)
    b.connect(gui.CLICK, lambda x:pygame.event.post(pygame.event.Event(pygame.QUIT)), None)

    # box2d initialization
    z=10 #scale
    renderer = fwDebugDraw()
    renderer.surface = screen
    renderer.viewZoom=z
    renderer.viewCenter=box2d.b2Vec2(0,0)
    renderer.width, renderer.height = width, height
    renderer.viewOffset = renderer.viewCenter - box2d.b2Vec2(width, height)/2
    renderer.SetFlags(box2d.b2DebugDraw.e_shapeBit)
    renderer.DrawSolidPolygon = lambda a,b,c: 0
    renderer.DrawPolygon = lambda a,b,c: 0
    worldAABB=box2d.b2AABB()
    worldAABB.lowerBound.Set(-100.0, -100.0)
    worldAABB.upperBound.Set( 100.0, 100.0)
    gravity = box2d.b2Vec2(0.0, -10.0)

    world = box2d.b2World(worldAABB, gravity, True)
    world.SetDebugDraw(renderer)

    bd = box2d.b2BodyDef()
    bd.position.Set(0.0, 0.0)
    ground = world.CreateBody(bd)
    
    # the borders and the world shapes for the file listing, etc.
    sd = box2d.b2PolygonDef()
    sd.SetAsBox(1, height/z, box2d.b2Vec2(-width/(2*z)-1, 0), 0)
    ground.CreateShape(sd)
    sd.SetAsBox(1, height/z, box2d.b2Vec2(width/(2*z)+1, 0), 0)
    ground.CreateShape(sd)
    sd.SetAsBox(width/z, 1, box2d.b2Vec2(0,-height/(2*z)-1), 0)
    ground.CreateShape(sd)
    sd.SetAsBox(width/z, 1, box2d.b2Vec2(0,height/(2*z)+1), 0)
    ground.CreateShape(sd)
    sd.SetAsBox(list_size[0]/(2*z), list_size[1]/(2*z))
    ground.CreateShape(sd)

    for i in range(10):
        bd = box2d.b2BodyDef()
        bd.allowSleep = True
        bd.position.Set(box2d.b2Random(-width/(2*z), width/(2*z)), box2d.b2Random(-height/(2*z), height/(2*z)))
        bd.isBullet = True
        bomb = world.CreateBody(bd)
        bomb.SetLinearVelocity(-5.0 * bd.position)

        sd = box2d.b2CircleDef()
        sd.radius = 1
        sd.density = 1.0
        sd.restitution = 0.7
        bomb.CreateShape(sd)
        
        bomb.SetMassFromShapes()

    app.init(main)
    main_loop(world, screen, demolist, app)

def get_shapes(world):
    for body in get_bodies(world):
        shape = body.GetShapeList()
        while shape:
            yield (body, shape.getAsType())
            shape=shape.GetNext()

def get_bodies(world):
    body = world.GetBodyList()
    while body:
        yield body
        body = body.GetNext()

def update_shapes(world):
    for body in get_bodies(world):
        v = body.GetLinearVelocity()
        if body.IsSleeping() or v.LengthSquared() < 0.2:
            i = body.GetWorldVector(box2d.b2Vec2(box2d.b2Random(-200,200), box2d.b2Random(-200,200)))
            p = body.GetWorldPoint(box2d.b2Vec2(0.0, 0.0))
            body.ApplyImpulse(i, p)
       
def main_loop(world, screen, demolist, app):
    app_surface = pygame.Surface((width,height), SWSURFACE)
    hz = 60.0
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    run_demo(demolist)
            elif event.type == MOUSEBUTTONDOWN:
                if event.button ==3:
                    run_demo(demolist)
                elif event.button ==4:
                    demolist.set_vertical_scroll(demolist.vscrollbar.value-100)
                elif event.button ==5:
                    demolist.set_vertical_scroll(demolist.vscrollbar.value+100)

            app.event(event)

        app.update(app_surface)
        screen.blit(app_surface, (0,0))

        update_shapes(world)
        world.Step(1/hz, 5)

        clock.tick(hz)        
        #fps = clock.get_fps()
        pygame.display.flip()

def add_demos(demolist):
    import glob

    ignore_list=("main")

    files = glob.glob("test_*.py")

    for f in files:
        name = f[5:-3]
        if name.lower() in ignore_list:
            continue
        demolist.add(name,value=f)

def run_demo(demolist):
    if demolist.value == None: return

    print "Running: ", demolist.value
    from sys import executable as python_interpreter
    from platform import system as sys_platform

    if sys_platform() == "Windows":
        cmd = '"%s" -OO %s' % (python_interpreter, demolist.value)
    else:
        cmd = "%s -OO %s" % (python_interpreter, demolist.value)

    print "-> %s" % cmd

    ret = os.system(cmd)

    if ret == 10 or ret/256 == 10: run_demo(demolist) # user hit reload

if __name__=="__main__":
    main()
