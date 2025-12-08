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

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, a):
        acopy = a
        while a != self.parent[a]:
            a = self.parent[a]
        while acopy != a:
            self.parent[acopy], acopy = a, self.parent[acopy]
        return a

    def union(self, a, b):
        self.parent[self.find(b)] = self.find(a)


class DisjointSetUnion:
    def __init__(self, n):
        self.parent = list(range(n))
        self.s = set(self.parent)
        self.size = [1] * n

    def find(self, a):
        acopy = a
        while a != self.parent[a]:
            a = self.parent[a]
        while acopy != a:
            self.parent[acopy], acopy = a, self.parent[acopy]
        return a

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a != b:
            if self.size[a] < self.size[b]:
                a, b = b, a
            self.s.remove(b)
            self.parent[b] = a
            self.size[a] += self.size[b]

    def set_size(self, a):
        return self.size[self.find(a)]

    def __len__(self):
        return len(self.s)

    def notfind(self, a):
        k = self.find(a)
        for j in self.s:
            if j!=k:
                return j
        return -1
    
def solve():
    L = []
    
    while True:
        try:
            L.append(list(map(int,SI().split(','))))
            if not L[-1]:
                break
        except:
            break
    k = 1000
    H = []

    def dist(a,b):
        ans = 0
        for i in range(len(a)):
            ans += (a[i]-b[i])**2
        return ans

    for i in range(len(L)):
        for j in range(i+1,len(L)):
            H.append((dist(L[i],L[j]),i,j))
    
    H.sort()

    ds = DisjointSetUnion(len(L))

    for d,x,y in H:
        if k==0:
            break
        if ds.find(x)!=ds.find(y):
            ds.union(x,y)
            ans = L[x][0]*L[y][0]

    
    # print(ans)
    print(ans)

    return

solve()

print("\n\n\n########## Stats ##########")
print(f"Time Taken : {time.time()-start:.2f} s")
mem = process.memory_info().rss / 1e6
print(f"Memory Used : {mem:.2f} MB")