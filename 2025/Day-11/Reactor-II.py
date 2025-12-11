import sys,math,cmath,random,os,time,psutil
from heapq import heappush,heappop
from bisect import bisect_right,bisect_left
from collections import Counter,deque,defaultdict
from itertools import permutations,combinations
from io import BytesIO, IOBase
from decimal import Decimal,getcontext

process = psutil.Process(os.getpid())
BUFSIZE = 8192
class FastIO(IOBase):
    newlines = 0
    def __init__(self, file):
        self._file = file
        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.writable = "x" in file.mode or "r" not in file.mode
        self.write = self.buffer.write if self.writable else None
    def read(self):
        while True:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            if not b:
                break
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()
    def readline(self):
        while self.newlines == 0:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            self.newlines = b.count(b"\n") + (not b)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()
    def flush(self):
        if self.writable:
            os.write(self._fd, self.buffer.getvalue())
            self.buffer.truncate(0), self.buffer.seek(0)
class IOWrapper(IOBase):
    def __init__(self, file):
        self.buffer = FastIO(file)
        self.flush = self.buffer.flush
        self.writable = self.buffer.writable
        self.write = lambda s: self.buffer.write(s.encode("ascii"))
        self.read = lambda: self.buffer.read().decode("ascii")
        self.readline = lambda: self.buffer.readline().decode("ascii")
sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)

# functions #
# MOD = 998244353
MOD = 10**9 + 7
RANDOM = random.randrange(1,2**62)
def gcd(a,b):
    while b:
        a,b = b,a%b
    return a
def lcm(a,b):
    return a//gcd(a,b)*b

II = lambda : int(sys.stdin.readline().strip())
LII = lambda : list(map(int, sys.stdin.readline().split()))
MI = lambda x : x(map(int, sys.stdin.readline().split()))
SI = lambda : sys.stdin.readline().strip()
SLI = lambda : list(map(lambda x:ord(x)-97,sys.stdin.readline().strip()))
LII_1 = lambda : list(map(lambda x:int(x)-1, sys.stdin.readline().split()))
LII_C = lambda x : list(map(x, sys.stdin.readline().split()))
MATI = lambda x : [list(map(int, sys.stdin.readline().split())) for _ in range(x)]

base = os.path.dirname(os.path.abspath(__file__))
sys.stdin  = open(os.path.join(base, "input.txt"), "r")
sys.stdout = open(os.path.join(base, "output.txt"), "w")
sys.stderr = open(os.path.join(base, "error.txt"), "w")

start = time.time()

def euler_path(d):
    start = [1]
    ans = []
    while start:
        cur = start[-1]
        if len(d[cur])==0:
            ans.append(start.pop())
            continue
        k1 = d[cur].pop()
        d[k1].remove(cur) # if undirected
        start.append(k1)
    return ans

def floyd_warshall(n, edges):
    dist = [[0 if i == j else float("inf") for i in range(n)] for j in range(n)]
    pred = [[None] * n for _ in range(n)]

    for u, v, d in edges:
        dist[u][v] = d
        pred[u][v] = u

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    pred[i][j] = pred[k][j]
    # Sanity Check
    # for u, v, d in edges:
    #	 if dist[u] + d < dist[v]:
    #		 return None
    return dist, pred

def bellman_ford(n, edges, start=0):
    dist = [float("inf")] * n
    pred = [None] * n
    dist[start] = 0
    for _ in range(n):
        for u, v, d in edges:
            if dist[u] + d < dist[v]:
                dist[v] = dist[u] + d
                pred[v] = u
    # for u, v, d in edges:
    #	 if dist[u] + d < dist[v]:
    #		 return -1
    # This returns -1 , if there is a negative cycle
    return dist

def toposort(graph):
    res, found = [], [0] * len(graph)
    stack = list(range(len(graph)))
    while stack:
        node = stack.pop()
        if node < 0:
            res.append(~node)
        elif not found[node]:
            found[node] = 1
            stack.append(~node)
            stack += graph[node]
    for node in res:
        if any(found[nei] for nei in graph[node]):
            return None
        found[node] = 0
    return res[::-1]

def solve():
    L = sys.stdin.readlines()
    d2 = {}
    count = 0

    edge = []
    d = [[] for _ in range(1000)]
    for i in range(len(L)):
        L[i] = L[i].strip()
        f = L[i].split(' ')
        f[0] = f[0][:-1]
        if f[0] not in d2:
            d2[f[0]] = count
            count += 1

        for j in f[1:]:
            if j not in d2:
                d2[j] = count
                count += 1
            d[d2[f[0]]].append(d2[j])
            edge.append((d2[f[0]],d2[j]))

    d = d[:count]
    start = d2["svr"]
    end = d2["out"]
    dp = [[0,0,0,0] for i in range(count)]
    dp[start][0] = 1

    L = toposort(d)
    d = defaultdict(list)

    for u,v in edge:
        d[v].append(u)

    k1 = d2["dac"]
    k2 = d2["fft"]

    for i in range(len(L)):
        for j in d[L[i]]:
            if j not in [k1,k2]:
                for k in range(4):
                    dp[L[i]][k] += dp[j][k]
            elif j==k1:
                for k in range(4):
                    dp[L[i]][k|1] += dp[j][k]
            else:
                for k in range(4):
                    dp[L[i]][k|2] += dp[j][k]

    print(dp[end][-1])

    return

solve()

print("\n\n\n########## Stats ##########")
print(f"Time Taken : {time.time()-start:.2f} s")
mem = process.memory_info().rss / 1e6
print(f"Memory Used : {mem:.2f} MB")