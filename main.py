import csv
import getopt
import sys
import os

import numpy as np

def vec_max(vector):
    vec_max = 0
    for i in range(len(vector)):
        if vec_max < len(vector[i]):
            vec_max = len(vector[i])
    return vec_max

def apply_zero_padding(vector):
    vec_max = vec_max(vector)
    for i in range(len(vector)):
        for j in range(len(vector[i])):
            if vector[i][j] == '':
                vector[i][j] = 0
            else:
                vector[i][j] = int(vector[i][j])
        for j in (vec_max - len(vector[i])):
            vector[i].append(0)

def lcs(x, y):
    lenX = len(x)
    lenY = len(y)
    L = [[0 for i in range(lenY+1)] for j in range(lenX+1)]
    for i in range(lenX+1):
        for j in range(lenY+1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif x[i-1] == y[j-1]:
                L[i][j] = L[i-1][j-1] + 1
            else:
                L[i][j] = max(L[i-1][j], L[i][j-1])
    lcs = ""
    i = lenX
    j = lenY
    while i > 0 and j > 0:
        if x[i-1] == y[j-1]:
            lcs += x[i-1]
            i -= 1
            j -= 1
        elif L[i-1][j] > L[i][j-1]:
            i -= 1
        else:
            j -= 1
    lcs = lcs[::-1]
    return lcs

def csv_to_array(pool_cv, target_cv):
    f_pool_cv = open(pool_cv, 'r')
    vector_pool = csv.reader(f_pool_cv)
    f_target_cv = open(target_cv, 'r')
    target = csv.reader(f_target_cv)

    vector_pool = np.asarray(list(vector_pool))
    target = np.asarray(list(target))

    return vector_pool, target

def get_sim_vectors(vector_pool, target_vector):
    similarity_array = {}
    for v in vector_pool:
        similarity_array.append(len(lcs(v, target_vector)))

def main(argv):
    try:
        opts, args = getopt.getopt(argv[1:], "h:g:t:r:", ["help", "gumtreeVector", "target", "resultpath"])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    gumtreeVector = "./gumtreeVector.csv"
    targetVector = "./target.csv"
    resultpath = ''
    for o, a in opts:
        if o in ("-H", "--help") or o in ("-h", "--hash"):
            print("")
            sys.exit()
        elif o in ("-t", "--target"):
            targetVector = a
        elif o in ("-g", "--gumtreeVector"):
            gumtreeVector = a
        elif o in ("-r", "--resultpath"):
            resultpath = a
        else:
            assert False, "unhandled option"

    root = os.getcwd()
    target_dir = root+"/target"
    result_dir = root+"/result"

    vector_pool, target = csv_to_array(gumtreeVector, targetVector)

if __name__ == '__main__':
    main(sys.argv)