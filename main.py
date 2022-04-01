#asumsi tile kosong adalah ubin dengan nilai 16
import timeit
import numpy as np

EMPTY = 16
#priority queue
class priorityQueue:
    def __init__(self):
        self.queue = []
 
    def push(self, node):
        self.queue.append(node)
 
    def pop(self):
        minidx = 0
        for i in range(len(self.queue)):
            if (self.queue[i].cost < self.queue[minidx].cost):
                minidx = i
        min = self.queue[minidx]
        del self.queue[minidx]
        return min
 
    def empty(self):
        if not self.queue:
            return True
        else:
            return False

#nodes
class node:
     
    def __init__(self, parent, mat, fcost, cost):
        self.parent = parent
        self.mat = mat
        self.fcost = fcost
        self.cost = cost

def newNode(mat, i,j,k,l, parent,target):  
    new_mat = copyMatrix(mat)
    swap(new_mat,i,j,k,l)
    #printMatrix(new_mat)
    #new_mat[i][j], new_mat[k][l] = new_mat[k][l], new_mat[i][j]
    fcost = parent.fcost + 1
    cost = fcost + gcost(new_mat,target) + 1
 
    new_node = node(parent, new_mat,fcost, cost)
    return new_node

#read from file
def read_file(filename):
    with open(filename, 'r') as f:
        l = [[int(num) for num in line.split(' ')] for line in f]
    return l

#Copy matrix, return matriks hasil copy
def copyMatrix(mat2):
    mat1 = [[0 for i in range(4)] for j in range(4)]
    for i in range(len(mat1)):
        for j in range(len(mat1[0])):
            mat1[i][j] = mat2[i][j]
    return mat1

#menghitung cost g(P) menuju target 
def gcost(mat, targetmat):
    count = 0
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if (mat[i][j] != targetmat[i][j]) :
                count += 1
    
    return count

#mengembalikan posisi bilangan n pada matrix
def posisi(mat,n):
    for i in range(4):
        for j in range(4):
            if (mat[i][j] == n):
                return i,j
    
    return -1,-1

#fungsi KURANG(i)
def kurang(mat,num):
    ipos,jpos = posisi(mat,num)
    countkurang = 0
    for i in range(ipos,len(mat)):
        if (i == ipos) :
            for j in range(jpos,len(mat[0])):
                if (mat[i][j] < num) :
                    countkurang += 1
        else :
            for j in range(len(mat[0])):
                if (mat[i][j] < num) :
                    countkurang += 1
    return countkurang

#Print solusi 
def printPath(node):
     
    if node == None:
        return
     
    printPath(node.parent)
    printMatrix(node.mat)
    print()

#Sumkurang untuk mengetahui sebuah matriks reachable goal atau bukan
def sumkurang(mat):
    sum = 0
    ckr = 0
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            ckr = kurang(mat,mat[i][j])
            print("KURANG("+str(mat[i][j])+") = " + str(ckr))
            sum += ckr

    sum += countX(mat)
    print("JUMLAH KURANG(i) + X = " + str(sum))
    return sum

#menentukan nilai x, 0 atau 1
def countX(mat):
    ipos,jpos = posisi(mat,EMPTY)
    if (ipos%2 == 0) :
        if (jpos %2 == 0) :
            return 0
        else :
            return 1
    else :
        if (jpos%2 == 0) :
            return 1
        else :
            return 0

#Swap matriks dengan posisi mat[i][j] dengan mat[k][l]
def swap(mat, i,j, k,l):
    temp = mat[k][l]
    mat[k][l] = mat[i][j]
    mat[i][j] = temp

def move_up(mat):
    i,j = posisi(mat,16)
    iup,jup = i-1,j
    swap(mat,i,j,iup,jup)

def move_right(mat):
    i,j = posisi(mat,16)
    iup,jup = i,j+1
    swap(mat,i,j,iup,jup)

def move_down(mat):
    i,j = posisi(mat,16)
    iup,jup = i+1,j
    swap(mat,i,j,iup,jup)

def move_left(mat):
    i,j = posisi(mat,16)
    iup,jup = i,j-1
    swap(mat,i,j,iup,jup)

#print matris
def printMatrix(mat):
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if (mat[i][j] == EMPTY):
                print(" ", end = "  ")
            elif (mat[i][j] < 10) :
                print(mat[i][j], end="  ")
            else :
                print(mat[i][j], end = " ")
             
        print()

#Cek apakah matriks sudah mencapai solusi
#Mat dan target memiliki ukuran sama
def solution(mat,target):
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if (mat[i][j] != target[i][j]) :
                return False
    return True

#solve
def solve(mat,target):
    start = timeit.default_timer()
    pq = priorityQueue()
    gc = gcost(mat,target)
    root = node(None,mat,0,gc)
    pq.push(root)
    jumlahsimpul = 1

    if (sumkurang(mat) %2 != 0) :
        print("Tidak ada solusi")
        end = timeit.default_timer()
    else :
        row = [-1,0,1,0]
        col = [0,1,0,-1]
        while (not pq.empty()):
            next = pq.pop()
            if (solution(next.mat, target)):
                print("SOLUSI YANG DITEMUKAN : ")
                printPath(next)
                end = timeit.default_timer()
                break
            ipos,jpos = posisi(next.mat,EMPTY)
            #generate kemungkinan matriks
            for i in range(4):
                #cek apakah melebihi batas
                if (ipos+row[i] >= 0 and ipos+row[i] < len(mat) and jpos+col[i] >= 0 and jpos+col[i] < len(mat[0])):
                    new_node = newNode(next.mat,ipos,jpos,ipos+row[i],jpos+col[i],next,target)
                    pq.push(new_node)
                    jumlahsimpul += 1
    print("Waktu eksekusi program : " + str(end-start))
    print("Jumlah simpul yang dibangkitkan : " + str(jumlahsimpul))

def createTarget(n):
    targetmats = [[0 for i in range(n)] for j in range(n)]
    num34 = 1
    for i in range(n):
        for j in range(n):
            targetmats[i][j] = num34
            num34 += 1
    return targetmats

def createRandomMatrix(n):
    lst = []
    for i in range(n*n):
        lst.append(i+1)
    
    np.random.shuffle(lst)
    idx = 0
    mat = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            mat[i][j] = lst[idx]
            idx += 1
    return mat

#TESTING
finalmat = createTarget(4)
print("SELAMAT DATANG DI 15-PUZZLE SOLVER")
print("1. BANGKITKAN MATRIKS ACAK")
print("2. PILIH MATRIKS DARI MASUKAN FILE")
choice = int(input("PILIHAN (1 ATAU 2) : "))
if (choice == 1):
    mats = createRandomMatrix(4)
    printMatrix(mats)
    solve(mats,finalmat)
elif (choice == 2):
    filename = input("MASUKKAN NAMA FILE : ")
    mats = read_file(filename)
    solve(mats,finalmat)
else:
    print("MASUKAN TIDAK VALID!")


#def node
#def node_path
#def solve