import csv
import getopt
import sys
import os
import numpy as np
import pandas as pd
from keras.preprocessing.sequence import pad_sequences

def vec_max(vector):
    vec_max = 0
    for i in range(len(vector)):
        if vec_max < len(vector[i]):
            vec_max = len(vector[i])
    return vec_max

def apply_zero_padding(vector):
    vector_size = vec_max(vector)
    for i in range(len(vector)):
        for j in range(len(vector[i])):
            if vector[i][j] == '':
                vector[i][j] = 0
            else:
                vector[i][j] = int(vector[i][j])
        for j in (vector_size - len(vector[i])):
            vector[i].append(0)

def lcs(vector_pool, target_vector):
    len_vp = len(vector_pool)
    # print("[debug.log] length vector pool = %d"% (len_vp))
    len_tv = len(target_vector)
    # print("[debug.log] length target vector = %d" % (len_tv))
    return lcs_algo(vector_pool, target_vector, len_vp, len_tv)

def lcs_algo(vector_pool, target_vector, len_vp, len_tv):
    L = [[0 for x in range(len_tv+1)] for x in range(len_vp+1)]
    for i in range(len_vp+1):
        for j in range(len_tv+1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif vector_pool[i-1] == target_vector[j-1]:
                L[i][j] = L[i-1][j-1] + 1
            else:
                L[i][j] = max(L[i-1][j], L[i][j-1])

    index = L[len_vp][len_tv]

    result_vector = [0] * (index+1)
    result_vector[index] = 0

    i = len_vp
    j = len_tv
    while i > 0 and j > 0:
        if vector_pool[i-1] == target_vector[j-1]:
            result_vector[index-1] = vector_pool[i-1]
            i -= 1
            j -= 1
            index -= 1
        elif L[i-1][j] > L[i][j-1]:
            i -= 1
        else:
            j -= 1
    return result_vector

def vecs_on_csv(resultPath, vector):
    # writing out the features learned by the model on a csv file
    vector_arr = np.array(vector)
    with open(resultPath, 'w', newline='') as file:
        csv_writer = csv.writer(file, delimiter=',')
        csv_writer.writerow(vector_arr)

def csv_to_array(pool_cv, target_cv):
    f_pool_cv = open(pool_cv, 'r')
    vector_pool = csv.reader(f_pool_cv)
    f_target_cv = open(target_cv, 'r')
    target = csv.reader(f_target_cv)

    vector_pool = np.asarray(list(vector_pool))
    target = np.asarray(list(target))

    return vector_pool, target

def trim_on_array(vector):
    trimed = list()
    for i in range(len(vector)):
        trimed.append(list(vector[i][:-1]))
    return trimed

def lcs_extract(vector_pool, targetVector):
    result_list = list()
    max_lcs_size = 0
    for i in range(len(vector_pool)):
        lcs_result = lcs(vector_pool[i], targetVector)
        # print("[debug.log] lcs result #%d = %s" %(i, lcs_result))
        if max_lcs_size < len(lcs_result):
            max_lcs_size = len(lcs_result)
        result_list.append(len(lcs_result))
    return result_list, max_lcs_size

def main(argv):
    try:
        opts, args = getopt.getopt(argv[1:], "h:g:t:r:", ["help", "gumtreeVector", "target","resultSize"])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    gumtreeVector = ''
    targetVector = ''
    result_size = 0
    for o, a in opts:
        if o in ("-H", "--help") or o in ("-h", "--hash"):
            print("")
            sys.exit()
        elif o in ("-t", "--target"):
            targetVector = a
        elif o in ("-g", "--gumtreeVector"):
            gumtreeVector = a
        elif o in ("-r", "--resultSize"):
            result_size = int(a)
        else:
            assert False, "unhandled option"

    target_dir = "./target/"
    result_dir = "./result/"
    
    
    targetVector = target_dir+targetVector
    gumtreeVector = target_dir+gumtreeVector

    vector_pool, target = csv_to_array(gumtreeVector, targetVector)

    vector_pool = trim_on_array(vector_pool)
    if result_size == 0:
        result_size = int(len(vector_pool) / 10)
    target = list(target[0])
    
    result_vector, max_lcs_size = lcs_extract(vector_pool, target)
    meta_result = dict()
    for i in range(max_lcs_size+1):
        meta_result[i] = result_vector.count(i)
    
    print("[debug.log] meta result:")
    print(meta_result.items())

    print("[debug.log] result:")
    print(result_vector)

    vecs_on_csv(result_dir+"result_vector.csv", result_vector)

if __name__ == '__main__':
    main(sys.argv)