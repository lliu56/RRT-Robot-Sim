import pygame
from src.RRTbasePy import RRTGraph,RRTMap
from src.robotSim_module import Robot,Envir
import time
import images
skins = [r'RobotPathFinder\DDR_RRT\\images\\robot_img.png',0.0211*3779.52]
dimensions = (600, 1200)
start = (50, 50)
goal = (800, 50)
obsdim = 80
obsnum = 30

def main():
    iteration=0
    pygame.init()
    map=RRTMap(start,goal,dimensions,obsdim,obsnum)
    graph=RRTGraph(start,goal,dimensions,obsdim,obsnum)

    obstacles=graph.makeobs()
    true_obstacles=graph.getTrueObs(obstacles)
    map.drawMap(obstacles)


    t1=time.time()
    while (not graph.path_to_goal()):
        time.sleep(0.005)
        elapsed=time.time()-t1
        t1=time.time()
        #raise exception if timeout
        if elapsed > 10:
            print('timeout re-initiating the calculations')
            raise

        if iteration % 10 == 0:
            X, Y, Parent = graph.bias(goal)
            pygame.draw.circle(map.graph_map, map.grey, (X[-1], Y[-1]), map.nodeRad * 2, 0)
            pygame.draw.line(map.graph_map, map.Blue, (X[-1], Y[-1]), (X[Parent[-1]], Y[Parent[-1]]),
                             map.edgeThickness)

        else:
            X, Y, Parent = graph.expand()
            pygame.draw.circle(map.graph_map, map.grey, (X[-1], Y[-1]), map.nodeRad * 2, 0)
            pygame.draw.line(map.graph_map, map.Blue, (X[-1], Y[-1]), (X[Parent[-1]], Y[Parent[-1]]),
                             map.edgeThickness)
            pygame.display.update()

        map.map.blit(map.graph_map,(0,0))
        map.drawMap(obstacles)
        iteration += 1
    time.sleep(3)
    newPath = graph.waypoints2path()
    map.drawPath(newPath)
    pygame.display.update()
    time.sleep(3)
    running = True
    dt = 0
    lasttime = pygame.time.get_ticks()
    environment = Envir(dimensions,map.map)
    robot=Robot(start, skins[0],newPath, width=80)


    while running:
        map.map.blit(map.graph_map,(0,0))
        map.drawMap(true_obstacles)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            robot.robot_simulate(robot, environment,dt, event)
        robot.robot_simulate(robot, environment, dt)
        pygame.display.update()

        dt = (pygame.time.get_ticks() - lasttime) / 1000  # secs
        lasttime = pygame.time.get_ticks()


if __name__ == '__main__':
    main()















