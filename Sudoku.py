import numpy as np

sudoku = np.loadtxt('test_1.txt')
print(sudoku)
sud = sudoku.ravel()

q = np.ones((81, 9), np.int32)
g = np.zeros((729, 729), np.int32)
kv = []
for i in range(81):
    ind = (int(int(i/9)/3)*3+int((i%9)/3))*9+((i%3)+(int(i/9)%3)*3)
    kv.append(ind)
    if sud[i] > 0:
        for j in range(9):
            q[ind][j] = 0
        q[ind][int(sud[i])-1] = 1

I = np.ones((9, 9), np.int32)
np.fill_diagonal(I, np.zeros((1, 9), np.int32))

sup = [[3, 6, 1, 2],
       [4, 7, 0, 2],
       [5, 8, 0, 1],
       [0, 6, 4, 5],
       [1, 7, 3, 5],
       [2, 8, 3, 4],
       [0, 3, 7, 8],
       [1, 4, 6, 8],
       [2, 5, 6, 7]]

def upd_g(i, j):
    g[i*9:(i+1)*9,j*9:(j+1)*9] = I

neig = np.zeros((81, 20), np.int32)

for i in range(81):
    cur = 0
    for j in range(9):
        ind = 9*int(i/9)+j
        if (ind != i):
            neig[i][cur] = ind
            cur += 1
    for cell in sup[int(i/9)][0:2]:
        for j in range(3):
            ind = cell*9+j*3+(i%9)%3
            neig[i][cur] = ind
            cur += 1
    for cell in sup[int(i/9)][2:4]:
        for j in range(3):
            ind = cell*9+j+int((i%9)/3)*3
            neig[i][cur] = ind
            cur += 1

for i in range(81):
    for n in neig[i]:
        upd_g(i, n)

def cross(q_, g_):
    q = q_.copy()
    g = g_.copy()

    changed = True

    while changed:
        changed = False

        for i in range(81):
            for k in range(9):
                if q[i][k] == 1:
                    for i1 in neig[i]:
                        cur = 0
                        for k1 in range(9):
                            cur = cur or g[i*9+k][i1*9+k1]
                        if cur == 0:
                            q[i][k] = 0
                            changed = True
                            break   

        for i in range(81):
            for k in range(9):
                for i1 in neig[i]:
                    for k1 in range(9):
                        if g[i*9+k][i1*9+k1] == 1:
                            cur = q[i][k] and q[i1][k1]
                            g[i*9+k][i1*9+k1] = cur
                            if cur == 0:
                                changed = True

    return q, g

def f(q):
    res = 0
    for k in range(9):
        res += q[0][k]
    return int(res > 0)

def gamma(k):
    for i in range(81):
        if q[i][k[i]] == 0:
            return 0
        for i1 in neig[i]:
            if g[i*9+k[i]][i1*9+k1[i1]] == 0:
                return 0
    return 1

q_cur, g_cur = cross(q, g)
k_star = []

if f(q_cur) == 0:
    print("Рішення не знайдено!")
else:
    for i in range(81):
        found = False
        for k in range(9):
            if q_cur[i][k] == 1:
                q = q_cur.copy()
                g = g_cur.copy()
                for k_ in range(9):
                    if k != k_:
                        q[i][k_] = 0
                q_cur, g_cur = cross(q, g)
                if f(q_cur) == 1:
                    k_star.append(k)
                    found = True
                    break
        if found == False:
            print("Рішення не знайдено")
            break
if len(k_star) == 81:
    result = np.zeros((9, 9), np.int32)
    for i in range(9):
        for j in range(9):
            result[i][j] = k_star[kv[i*9+j]]+1
    print(result)

    
                            






    

