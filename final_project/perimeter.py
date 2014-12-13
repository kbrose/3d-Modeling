import matplotlib.pyplot as plt
import copy

class grid:
    def __init__(self,M):
        self.M = M
        self.originalM = copy.deepcopy(M)
        self.m = len(M)
        self.n = len(M[0])
        self.perimeter = []
        self.calcPerimeter()
        self.orderPerimeter()
        self.perimeters = []
        while self.perimeter != []:
            # self.show()
            self.perimeters.append(self.perimeter)
            self.iterateM(self.getCoveredPoints())
            self.perimeter = []
            self.calcPerimeter()
            self.orderPerimeter()

    def getCoveredPoints(self):
        covered = []
        for p in self.perimeter:
            p1 = p[0]
            p2 = p[1]
            if p1[1] == p2[1]:
                for i in range(min(p1[0],p2[0]),max(p1[0],p2[0])+1):
                    covered.append([i,p1[1]])
            else:
                covered.append(p1)
                covered.append(p2)
        return covered

    def iterateM(self,pts):
        for pt in pts:
            self.M[pt[0]][pt[1]] = 0
        for i in range(len(self.M)):
            for j in range(len(self.M[0])):
                if self.M[i][j]:
                    self.M[i][j] = 1

    def orderPerimeter(self):
        P = self.perimeter
        if len(P) == 0:
            return
        P1 = [P[0]]
        P = P[1:]
        start = P1[0][0]
        while len(P):
            coord = P1[-1][1]
            if coord == start:
                P1.append(P[0])
                P = P[1:]
                start = P1[-1][0]
                continue
            if coord not in [x[0] for x in P] and coord not in [x[1] for x in P]:
                print 'Error! Perimeter poorly formed'
                return
            if coord in [x[0] for x in P]:
                i = [x[0] for x in P].index(coord)
                P1.append(P[i])
            elif coord in [x[1] for x in P]:
                i = [x[1] for x in P].index(coord)
                P1.append(P[i][::-1])
            P = P[:i] + P[i+1:]
        self.perimeter = P1


    # M = m X n binary matrix
    def calcPerimeter(self):
        M = self.M
        self.queue = []
        start = 0
        while start < self.m and sum(M[start]) == 0:
            start = start + 1
        if start == self.n:
            return
        self.parentlessQueue(start) # add all nodes with no parent
        curr_col = start
        for c in range(start+1,self.n+1):
            # print ''
            # for thing in M[::-1]:
            #     print thing
            curr_Q = self.queue
            self.queue = []

            for q in curr_Q:
                if q.col+1 == self.n:
                    continue
                if len(q.rows) == 1:
                    if q.midrow not in [q.min_row,q.max_row]:
                        if M[q.midrow][q.col+1] and M[q.midrow-1][q.col+1] and M[q.midrow+1][q.col+1]:
                            q.l = [q.midrow-1]
                            q.u = [q.midrow+1]
                            M[q.midrow][q.col+1] = 2
                            M[q.midrow-1][q.col+1] = 2
                            M[q.midrow+1][q.col+1] = 2
                    if q.l == []:
                        if q.midrow+1 < self.m and M[q.midrow][q.col+1] and M[q.midrow+1][q.col+1]:
                            q.l = [q.midrow]
                            q.u = [q.midrow+1]
                            M[q.midrow][q.col+1] = 2
                            M[q.midrow+1][q.col+1] = 2
                    if q.l == []:
                        if q.midrow-1 > 0 and M[q.midrow][q.col+1] and M[q.midrow-1][q.col+1]:
                            M[q.midrow-1][q.col+1] = 2
                            M[q.midrow][q.col+1] = 2
                            q.l = [q.midrow-1]
                            q.u = [q.midrow]
                else:
                    i = max(q.rows[0]-1,q.min_row)
                    while i <= min(q.rows[1]+1,q.max_row):
                        if M[i][q.col+1]:
                            q.l.append(i)
                            j = i
                            while j <= min(q.rows[1]+1,q.max_row) and M[j][q.col+1]:
                                M[j][q.col+1] = 2
                                j = j+1
                            q.u.append(j-1)
                            i = j
                        i = i + 1

            while any([q.searching for q in curr_Q]):
                for q in curr_Q:
                    d = q.curr_dist
                    j = len(q.l)-1

                    if q.col+1 == self.n or q.l == [] or (q.l[0]-1 < q.min_row and q.u[j]+1 > q.max_row): 
                        q.searching = False
                    if not q.searching:
                        continue

                    if M[max(q.l[0]-1,q.min_row)][q.col+1] != 1:
                        q.min_row = max(q.l[0]-1,q.min_row)
                    if M[min(q.u[j]+1,q.max_row)][q.col+1] != 1:
                        q.max_row = min(q.u[j]+1,q.max_row)

                    if M[max(q.l[0]-1,q.min_row)][q.col+1] == 1:
                        M[max(q.l[0]-1,q.min_row)][q.col+1] = 2
                        q.l[0] = max(q.l[0]-1,q.min_row)
                    else:
                        q.min_row = q.l[0]

                    if M[min(q.u[j]+1,q.max_row)][q.col+1] == 1:
                        M[min(q.u[j]+1,q.max_row)][q.col+1] = 2
                        q.u[j] = min(q.u[j]+1,q.max_row)
                    else:
                        q.max_row = q.u[j]

                    q.curr_dist = q.curr_dist + 1

            curr_Q = sorted(curr_Q, key=lambda q:q.l)
            i = 0
            while i < len(curr_Q) - 1:
                q1 = curr_Q[i]
                q2 = curr_Q[i+1]
                if q1.l == []:
                    i = i + 1
                    continue
                j = len(q1.u)-1
                if q1.u[j] == q2.l[0]-1 or q1.u[j] == q2.l[0]:
                    if q1.u[j] != q2.l[0]:
                        self.perimeter.append([[q1.u[j],q1.col+1],[q2.l[0],q2.col+1]])
                    self.perimeter.append([[q2.rows[0],q2.col],[q2.l[0],q2.col+1]])
                    self.perimeter.append([[q1.rows[-1],q1.col],[q1.u[j],q1.col+1]])
                    if len(q1.rows) == 2 and not q1.par:
                        self.perimeter.append([[q1.rows[0],q1.col],[q1.rows[1],q1.col]])
                    if len(q2.rows) == 2 and not q2.par:
                        self.perimeter.append([[q2.rows[0],q2.col],[q2.rows[1],q2.col]])
                    if len(q1.rows) == 2:
                        q1.rows[1] = q2.rows[-1]
                    else:
                        q1.rows.append(q2.rows[-1])
                    q1.l = q1.l + q2.l[1:]
                    q1.u = q1.u[:-1] + q2.u
                    q1.par = True
                    curr_Q = curr_Q[:i+1] + curr_Q[i+2:]
                    i = i - 1
                i = i + 1

            for q in curr_Q:
                if q.l == []:
                    if len(q.rows) == 2 and q.par:
                        self.perimeter.append([[q.rows[0],q.col],[q.rows[1],q.col]])
                    continue
                if len(q.rows) == 2 and not q.par:
                    self.perimeter.append([[q.rows[0],q.col],[q.rows[1],q.col]])
                if len(q.rows) == 2:
                    self.perimeter.append([[q.rows[0],q.col],[q.l[0],q.col+1]])
                    for i in range(len(q.l)-1):
                        conn_point = (q.u[i] + q.l[i+1]) / 2
                        self.perimeter.append([[conn_point,q.col],[q.u[i],q.col+1]])
                        self.perimeter.append([[conn_point,q.col],[q.l[i+1],q.col+1]])
                    self.perimeter.append([[q.rows[1],q.col],[q.u[len(q.u)-1],q.col+1]])                        
                else:
                    self.perimeter.append([[q.rows[0],q.col],[q.l[0],q.col+1]])
                    self.perimeter.append([[q.rows[0],q.col],[q.u[0],q.col+1]])
                for pair in zip(q.l, q.u):
                    if pair[0] != pair[1] and q.col+1 == self.n:
                        self.perimeter.append([[pair[0],q.col+1],[pair[1],q.col+1]])
                if q.col+1 != self.n:
                    for pair in zip(q.l,q.u):
                        l = pair[0]
                        u = pair[1]
                        if l == u:
                            self.queue.append(self.node([l],q.col+1,True,0,self.m-1,True,0))
                        else:
                            self.queue.append(self.node([l,u],q.col+1,True,0,self.m-1,True,0))

            if c+1 <= self.n:
                self.parentlessQueue(c) # add new-comers
            # self.show()

    # adds all "in" nodes that weren't found in column k
    # by iterating through nodes in the queue from column k-1
    def parentlessQueue(self,k):
        if k >= self.n:
            return
        col = [self.M[i][k] for i in range(self.m)]
        Q = []
        for i in range(self.m):
            if col[i] == 1:
                self.M[i][k] = 2
                j = i+1
                while j < self.m and col[j] == 1:
                    self.M[j][k] = 2
                    col[j] = 0
                    j = j+1
                if j == i+1:
                    Q.append(self.node([i],k,False,0,self.m-1,True,0))
                else:
                    Q.append(self.node([i,j-1],k,False,0,self.m-1,True,0))

        # don't look further down than the previous guy
        for i in range(len(Q)-1):
            Q[i+1].min_row = Q[i].midrow

        # don't look further up than the next guy
        for i in range(1,len(Q)):
            Q[i-1].max_row = Q[i].midrow
        self.queue = self.queue + Q

    def show(self):
        plt.axis((-1,self.n,-1,self.m))
        plt.grid()
        plt.scatter([j for i in range(self.m) for j in range(self.n) if self.M[i][j]],
                    [i for i in range(self.m) for j in range(self.n) if self.M[i][j]])
        for pair in self.perimeter[::-1]:
            plt.plot([pair[0][1], pair[1][1]], [pair[0][0], pair[1][0]],'r')
        plt.show()

    def showAll(self):
        for perimeter in self.perimeters:
            plt.axis((-1,self.n,-1,self.m))
            plt.grid()
            plt.scatter([j for i in range(self.m) for j in range(self.n) if self.originalM[i][j]],
                        [i for i in range(self.m) for j in range(self.n) if self.originalM[i][j]])
            for pair in perimeter[::-1]:
                plt.plot([pair[0][1], pair[1][1]], [pair[0][0], pair[1][0]],'r')
        plt.show()


    class node:
        def __init__(self,rows,col,par,
                      min_row,max_row,searching,dist):
            self.rows = rows
            if len(rows) == 2:
                self.midrow = sum(rows) / 2 # roundoff error OK here
                self.diff = max(rows[1] - self.midrow, self.midrow - rows[0])
            else:
                self.midrow = rows[0]
                self.diff = 0
            self.col = col
            self.par = par
            self.min_row = min_row
            self.max_row = max_row
            self.searching = searching
            self.l = []
            self.u = []
            self.curr_dist = dist

if __name__ == '__main__':
    # M = [[0,0,0,0,0,0],[0,1,1,1,1,0],[0,1,1,1,1,0],[0,0,0,0,0,0]]
    # g = grid(M)

    M = [[1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
         [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
         [1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
         [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
         [0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
         [0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]]
    M = M[::-1]

    g = grid(M)

    # for p in g.perimeters:
    #     print p
    #     print ''

    # print g.perimeters[0] + g.perimeters[1]

    # g.showAll()


