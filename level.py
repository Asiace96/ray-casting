import pygame, sys, random, math
from cell import Cell
from player import Player
from settings import FPS

class Level:
    def __init__(self, clock, num_cols):
        self.clock = clock
        self.screen = pygame.display.get_surface()
        self.width = self.screen.get_size()[0]//2
        self.height = self.screen.get_size()[1]

        self.cols = num_cols
        self.cell_size = self.width // num_cols
        self.rows = self.height // self.cell_size

        self.cell_group = pygame.sprite.Group()
        self.map = self.initialize_map()
        self.wall_map()

        self.running = True

        #player
        self.px = 2.5*self.cell_size
        self.py = 2.5*self.cell_size
        self.pa = 1 
        self.pdx = 5*math.cos(self.pa)
        self.pdy = 5*math.sin(self.pa)
        self.radius = 5
        self.rect = pygame.Rect((self.px-self.radius,self.py-self.radius), (self.radius,self.radius))

    def input(self, dt):
        keys = pygame.key.get_pressed()
        speed = 1/float(dt)

        if keys[pygame.K_a]:
            self.pa -= 0.7*speed
            if self.pa < 0:
                self.pa += 2*math.pi
            self.pdx = math.cos(self.pa)
            self.pdy = math.sin(self.pa)

        if keys[pygame.K_d]:
            self.pa += 0.7*speed
            if self.pa > 2*math.pi:
                self.pa -= 2*math.pi
            self.pdx = math.cos(self.pa)
            self.pdy = math.sin(self.pa)

        #checking collisions
        xo = -3*self.radius if self.pdx<0 else 3*self.radius
        yo = -3*self.radius if self.pdy<0 else 3*self.radius
        crow,ccol = self.get_cell_pos(self.px, self.py)
        nrow,ncol = self.get_cell_pos(self.px+xo, self.py+yo)
        prow,pcol = self.get_cell_pos(self.px-xo, self.py-yo)

        if keys[pygame.K_w]:
            if not self.map[crow][ncol].barrier:
                self.px += self.pdx*speed*70
            if not self.map[nrow][ccol].barrier:
                self.py += self.pdy*speed*70
        if keys[pygame.K_s]:
            if not self.map[crow][pcol].barrier:
                self.px -= self.pdx*speed*70
            if not self.map[prow][ccol].barrier:
                self.py -= self.pdy*speed*70
    

    def draw_player(self):
        self.rect = pygame.draw.circle(self.screen, 'yellow', (self.px, self.py), self.radius)
        pygame.draw.line(self.screen, 'green', (self.px,self.py), (self.px+5*self.pdx, self.py+5*self.pdy))
        self.draw_rays()

    def distance(self,x1,y1,x2,y2):
        return math.sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))


    def draw_rays(self):
        rad = math.radians(0.5)
        ra = self.pa - 30*rad
        if ra<0: ra+=2*math.pi
        if ra>2*math.pi: ra-=2*math.pi
        final_dist = 0

        for i in range(120):
            #  ------ Check Horzintal Lines ------ #
            dof = 0
            dist_h, hx, hy = float('inf'), self.px, self.py
            cotan = -1/math.tan(ra)

            #looking up
            if ra > math.pi:
                ry = (self.py // self.cell_size) * self.cell_size - 0.0001
                rx = (self.py - ry)*cotan + self.px
                yo = -self.cell_size
                xo = -yo*cotan
            
            #looking down
            if ra < math.pi:
                ry = (self.py // self.cell_size) * self.cell_size + self.cell_size
                rx = (self.py - ry)*cotan + self.px
                yo = self.cell_size
                xo = -yo*cotan
            
            #looking straight left/right
            if ra == 0 or ra == math.pi:
                rx = self.px
                ry = self.py
                dof = self.rows
            
            while dof < self.rows:
                mx = int(rx // self.cell_size)
                my = int(ry // self.cell_size)
                
                if 0<=mx<self.cols and 0<=my<self.rows:
                    if self.map[my][mx].barrier:
                        hx, hy = rx, ry
                        dist_h = self.distance(self.px,self.py,hx,hy)
                        dof = self.rows
                    else: 
                        rx += xo
                        ry += yo
                        dof += 1
                        continue
                else:
                    rx += xo
                    ry += yo
                    dof += 1

            #  ------ Check Vertical Lines ------ #
            dof = 0
            dist_v, vx, vy = float('inf'), self.px, self.py
            tan = -math.tan(ra)

            #looking left
            if ra > math.pi/2 and ra < 3*math.pi/2:
                rx = (self.px // self.cell_size) * self.cell_size - 0.0001
                ry = (self.px - rx)*tan + self.py
                xo = -self.cell_size
                yo = -xo*tan
            
            #looking right
            if ra < math.pi/2 or ra > 3*math.pi/2:
                rx = (self.px // self.cell_size) * self.cell_size + self.cell_size
                ry = (self.px - rx)*tan + self.py
                xo = self.cell_size
                yo = -xo*tan
            
            #looking straight up/down
            if ra == 0 or ra == math.pi:
                rx = self.px
                ry = self.py
                dof = self.cols
            
            while dof < self.cols:
                mx = int(rx // self.cell_size)
                my = int(ry // self.cell_size)
                
                if 0<=mx<self.cols and 0<=my<self.rows:
                    if self.map[my][mx].barrier:
                        vx, vy = rx, ry
                        dist_v = self.distance(self.px,self.py,vx,vy)
                        dof = self.cols
                    else: 
                        rx += xo
                        ry += yo
                        dof += 1
                        continue
                else:
                    rx += xo
                    ry += yo
                    dof += 1


            if dist_v < dist_h: rx,ry, final_dist,color = vx,vy, dist_v,'seagreen1' # verical hit
            if dist_h < dist_v: rx,ry, final_dist,color = hx,hy, dist_h,'seagreen' # horizontal hit
            pygame.draw.line(self.screen,'green',(self.px,self.py),(rx,ry)) # draw ray

            #  ------ Draw 3D Walls ------ #
            angle = self.pa - ra
            if angle<0: angle+=2*math.pi
            if angle>2*math.pi: angle-=2*math.pi
            final_dist = final_dist*math.cos(angle) # fix 'fisheye' effect
            
            lh = (self.height / final_dist)*self.cell_size
            if lh > self.height-self.cell_size: lh = self.height-self.cell_size
            lo = self.height - lh//2
            le = lo-self.height//2
            ls = lh+lo-self.height//2
            pygame.draw.line(self.screen,color,(i*6+self.width,ls),(i*6+self.width,le),6)

            ra += rad
            if ra<0: ra+=2*math.pi
            if ra>2*math.pi: ra-=2*math.pi


    def initialize_map(self):
        grid = []
        for i in range(self.rows):
            grid.append([])
            for j in range(self.cols):
                grid[i].append(Cell(i,j,self.cell_size,self.rows,self.cols,[self.cell_group]))
        return grid

    def clear_map(self):
        for row in self.map:
            for cell in row:
                cell.reset()
        self.wall_map()

    def wall_map(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if i==0 or i==self.rows-1 or j==0 or j==self.cols-1:
                    self.map[i][j].make_barrier()
        
    def random_walls(self):
        for row in self.map:
            for cell in row:
                if not random.randint(0,5):
                    cell.make_barrier()

    def get_clicked_cell_pos(self):
        x,y = pygame.mouse.get_pos()
        row = y // self.cell_size
        col = x // self.cell_size
        return row,col   

    def get_cell_pos(self, x, y):
        row = y // self.cell_size
        col = x // self.cell_size
        return int(row),int(col)  


    def run(self):
        while self.running:
            dt=self.clock.tick(FPS)
            self.screen.fill('grey20')
            self.screen.fill('skyblue',(self.width,0, self.width,self.height//2))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit(1)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if event.key == pygame.K_c:
                        self.clear_map()
                    if event.key == pygame.K_r:
                        self.clear_map()
                        self.random_walls()

            self.cell_group.update()
            self.cell_group.draw(self.screen)
            self.input(dt)
            self.draw_player()
            pygame.display.set_caption(f'FPS: {self.clock.get_fps()}')
            pygame.display.flip()