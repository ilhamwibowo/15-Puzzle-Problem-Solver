#asumsi tile kosong adalah ubin dengan nilai 16
import timeit
import numpy as np
import random
from priorityQueue import priorityQueue
from node import node
EMPTY = 16

def newNode(mat, i,j,k,l, parent,target,move):  
    new_mat = copyMatrix(mat)
    swap(new_mat,i,j,k,l)
    #printMatrix(new_mat)
    #new_mat[i][j], new_mat[k][l] = new_mat[k][l], new_mat[i][j]
    fcost = parent.fcost + 1
    cost = fcost + gcost(new_mat,target)
 
    new_node = node(parent, new_mat,fcost, cost,move)
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
    printmove(node.move)
    printMatrix(node.mat)
    print()

#Sumkurang untuk mengetahui sebuah matriks reachable goal atau bukan
def sumkurang(mat):
    sum = 0
    ckr = 0
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            ckr = kurang(mat,mat[i][j])
            #print("KURANG("+str(mat[i][j])+") = " + str(ckr))
            sum += ckr
    #print(sum)
    sum += countX(mat)
    #print("JUMLAH KURANG(i) + X = " + str(sum))
    return sum

def printkurang(mat):
    sum = 0
    ckr = 0
    arr = [0 for i in range(16)]
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            ckr = kurang(mat,mat[i][j])
            arr[mat[i][j]-1] = ckr
            sum += ckr

    for i in range(16):
        print("KURANG("+str(i+1)+") = " + str(arr[i]))
    sum += countX(mat)
    print("JUMLAH KURANG(i) + X = " + str(sum))

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

#print matris
def printMatrix(mat):
    for i in range(len(mat)):
        print("---------------------")
        for j in range(len(mat[0])):
            if (j == 0) :
                    print("| ", end="")
            if (mat[i][j] == EMPTY):
                print(" ", end = "  | ")
            elif (mat[i][j] < 10) :
                print(mat[i][j], end="  | ")
            else :
                print(mat[i][j], end = " | ")
    
        print()
    print("---------------------")

#Cek apakah matriks sudah mencapai solusi
#Mat dan target memiliki ukuran sama
def solution(mat,target):
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if (mat[i][j] != target[i][j]) :
                return False
    return True

def safe(a,b):
    if (b == -1):
        return True
    elif (a == 1):
        if (b == 3):
            return False
        else :
            return True
    elif (a == 0):
        if (b == 2):
            return False
        else :
            return True
    elif (a == 2):
        if (b == 0):
            return False
        else :
            return True
    elif(a == 3):
        if (b == 1):
            return False
        else:
            return True

def printmove(n):
    if (n != -1):
        print("|||||||||||||||||||||")
        if (n == 0):
            print("^^^^^ MOVE UP ^^^^^")
        elif (n == 1):
            print(">>>>> MOVE RIGHT >>>>>")
        elif (n == 2):
            print("vvvvv MOVE DOWN vvvvv")
        elif (n == 3):
            print("<<<<< MOVE LEFT <<<<<")
        print("|||||||||||||||||||||")

#solve
def solve(mat,target):
    start = timeit.default_timer()
    pq = priorityQueue()
    gc = gcost(mat,target)
    found = False
    root = node(None,mat,0,gc,-1)
    pq.push(root)
    jumlahsimpul = 1

    if (sumkurang(mat) %2 != 0) :
        print("SOLUSI TIDAK DITEMUKAN")
    else :
        row = [-1,0,1,0]
        col = [0,1,0,-1]
        while (not pq.empty()):
            next = pq.pop()

            if (solution(next.mat, target)):
                print("SOLUSI YANG DITEMUKAN : ")
                printPath(next)
                found = True
                break
            ipos,jpos = posisi(next.mat,EMPTY)
            #generate kemungkinan matriks
            for i in range(4):
                #mengecek jika move terakhir up maka move selanjutnya != down, left != right dan sebaliknya
                if (safe(i,next.move)):
                    #cek apakah melebihi batas
                    if (ipos+row[i] >= 0 and ipos+row[i] < len(mat) and jpos+col[i] >= 0 and jpos+col[i] < len(mat[0])):
                        new_node = newNode(next.mat,ipos,jpos,ipos+row[i],jpos+col[i],next,target,i)
                        #tidak dimasukkan queue jika tidak menuju solusi
                        if (sumkurang(next.mat)%2 == 0):
                            pq.push(new_node)
                        jumlahsimpul += 1
        if (not found):
            print("SOLUSI TIDAK DITEMUKAN")
    end = timeit.default_timer()         
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

#solvable matrix
#matriks target diacak
def createRandomMatrix(diff,target):
    mtx = copyMatrix(target)
    row = [-1,0,1,0]
    col = [0,1,0,-1]
    i = 0
    while(i != diff):
        ipos,jpos = posisi(mtx,EMPTY)
        x = random.randint(0,3)
        if (ipos+row[x] >= 0 and ipos+row[x] < len(mtx) and jpos+col[x] >= 0 and jpos+col[x] < len(mtx[0])):
            swap(mtx,ipos,jpos,ipos+row[x],jpos+col[x])
            i += 1
    return mtx


#TESTING
finalmat = createTarget(4)
print("SELAMAT DATANG DI 15-PUZZLE SOLVER")
print("1. BANGKITKAN MATRIKS ACAK")
print("2. PILIH MATRIKS DARI MASUKAN FILE")
print("3. KELUAR")
choice = int(input("PILIHAN : "))
while (not choice == 3):
    if (choice == 1):
        difficulty = int(input("MASUKKAN JUMLAH PENGACAKAN : "))
        mats = createRandomMatrix(difficulty, finalmat)
        print("MATRIKS AWAL : ")
        printMatrix(mats)
        printkurang(mats)
        mat = np.matrix(mats)
        solve(mats,finalmat)

    elif (choice == 2):
        filename = input("MASUKKAN NAMA FILE : ")
        mats = read_file(filename)
        print("MATRIKS AWAL : ")
        printMatrix(mats)
        printkurang(mats)
        solve(mats,finalmat)

    else:
        print("MASUKAN TIDAK VALID!")
    print("1. BANGKITKAN MATRIKS ACAK")
    print("2. PILIH MATRIKS DARI MASUKAN FILE")
    print("3. KELUAR")
    choice = int(input("PILIHAN : "))


#def node
#def node_path
#def solve