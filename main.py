import csv
import getopt
import sys
import os
import numpy as np
import pandas as pd
from keras.preprocessing.sequence import pad_sequences

# find longest common subsequence of target vector within vector pool
def lcs(vector_pool, target_vector):
    len_vp = len(vector_pool)
    # print("[debug.log] length vector pool = %d"% (len_vp))
    len_tv = len(target_vector)
    # print("[debug.log] length target vector = %d" % (len_tv))
    return lcs_algo(vector_pool, target_vector, len_vp, len_tv)

def int_array_equal(a, b):
    a = a.strip()
    if len(a) != len(b):
        return False
    for i in range(len(a)):
        if a[i]==' ': del a[i]
        if int(a[i]) != int(b[i]):
            return False
    return True

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

# write in result path the given vector list as csv file
def array2d_to_csv(resultPath, vector):
    vector_arr = np.array(vector)
    # for each in vector_arr:
    #     print(f"[debug.log] each line = {each}")
    with open(resultPath, 'w', newline='') as file:
        csv_writer = csv.writer(file, delimiter=',')
        csv_writer.writerows(vector_arr)

# write in result path the given vector list as csv file
def array1d_to_csv(resultPath, vector):
    vector_arr = np.array(vector,dtype=np.int32)
    with open(resultPath, 'w', newline='') as file:
        csv_writer = csv.writer(file, delimiter=',')
        csv_writer.writerow(vector_arr)
        

# get pool csv file and target csv file as array.
def csv_to_array(pool_cv):
    f_pool_cv = open(pool_cv, 'r')
    vector_pool = csv.reader(f_pool_cv)

    vector_pool = np.asarray(list(vector_pool))
    return vector_pool

# remove trailing commas at the end of each row of csv files
def remove_trailing_commas(vector):
    trimed = list()
    for i in range(len(vector)):
        trimed.append(list(vector[i][:-1]))
    return trimed

# remove empty new lines in change vector array and meta vector array
def remove_empty_line(vector, metavector, index):
    del vector[index]
    np.delete(metavector, index, axis=None)

# locate empty new lines in change vector array and meta vector file array
def locate_empty_line(vector):
    empty_line_index_list = list()
    for i in range(len(vector)):
        if len(vector[i]) <= 0:
            empty_line_index_list.append(i)
    return empty_line_index_list

# locate and remove empty lines in change vector array and meta vector array
def clean_change_vector(vector_pool, metavector):
    empty_line_index_list = locate_empty_line(vector_pool)
    for i in range(len(empty_line_index_list)):
        remove_empty_line(vector_pool, metavector, empty_line_index_list[i]-i)

# return result list of lcs length of each row from vector pool
def lcs_count(vector_pool, targetVector):
    result_list = list()
    for i in range(len(vector_pool)):
        lcs_result = lcs(vector_pool[i], targetVector)
        # print("[debug.log] lcs result #%d = %s" %(i, lcs_result))
        result_list.append(len(lcs_result))
    return result_list

# gumtreeVector.csv.trimed, lcs_count_list.csv, max = size of target cv, result_pool_size = 10% of size
def lcs_extract(vector_pool, lcs_count_list, max_lcs_size, result_pool_size):
    result_list = list()
    result_index_list = list()
    lcs_count_index_dict = dict()
    for lcs_list_index in range(len(lcs_count_list)):
        lcs_count_index_dict.setdefault(lcs_count_list[lcs_list_index], []).append(lcs_list_index)
        
    target_index = max_lcs_size
    result_pool_size_iter = result_pool_size
    while result_pool_size_iter > 0:
        if target_index in lcs_count_index_dict:
            print(f"[debug.log] iterating LCS score ({target_index}/{max_lcs_size}) = {(target_index / max_lcs_size) * 100:.2f}% ...")
            result_pool_size_iter -= len(lcs_count_index_dict[target_index])
        if(result_pool_size_iter > 0):
            target_index -= 1
    
    for i in range(max_lcs_size, target_index-1,-1):
        if i in lcs_count_index_dict:
            if ((len(result_index_list) + len(lcs_count_index_dict[i])) / result_pool_size - 1) >= 1.5:
                # limited the error rate top margin to 150 %
                print(f"[debug.log] Warning: break due to too large error rate")
                break
            result_index_list.extend(lcs_count_index_dict[i])
    
    print(f"[debug.log] collected max LCS score = {(max_lcs_size / max_lcs_size) * 100:.2f}%")
    print(f"[debug.log] collected minimum LCS score = {(target_index / max_lcs_size) * 100:.2f}%")
    print(f"[debug.log] target result pool size = {result_pool_size}")
    print(f"[debug.log] result index list size = {len(result_index_list)}")
    print(f"[debug.log] error rate = {(len(result_index_list) / result_pool_size - 1)*100:.2f}%")
    # result_index_list.sort()
    
    for index in range(len(result_index_list)):
        result_list.append(vector_pool[result_index_list[index]])

    return result_list, result_index_list

def meta_lcs_extract(result_index_list, meta_vector_pool):
    # print(f"[debug.log] result index list:\n{result_index_list}")
    meta_result_list = list()
    for i in range(len(result_index_list)):
        meta_result_list.append(meta_vector_pool[result_index_list[i]])
    return meta_result_list

def main(argv):
    try:
        opts, args = getopt.getopt(argv[1:], "h:g:t:c:r:", ["help", "gumtreeVector", "target","commitPool","resultSize"])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    gumtreeVector = ''
    commitPool = ''
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
        elif o in ("-c", "--commitPool"):
            commitPool = a
        else:
            assert False, "unhandled option"

    target_dir = "./target/"
    result_dir = "./result/"
    
    
    targetVector = target_dir+targetVector
    gumtreeVector = target_dir+gumtreeVector
    commitPool = target_dir+commitPool
    print(f"[debug.log] target: {targetVector}, gumtreeVector: {gumtreeVector}, commitPool: {commitPool}, resultSize: {result_size}")
    vector_pool = csv_to_array(gumtreeVector)
    target = csv_to_array(targetVector)
    commit_pool = csv_to_array(commitPool)
    print(f"[debug.log] original vector_pool size = {len(vector_pool)}")
    vector_pool = remove_trailing_commas(vector_pool)
    clean_change_vector(vector_pool, commit_pool)
    print(f"[debug.log] changed vector_pool size = {len(vector_pool)}")
    if result_size == 0:
        result_size = int(len(vector_pool) / 10)
    target = list(target[0])
    
    lcs_count_list = lcs_count(vector_pool, target)
    # length of longest common subsequence
    max_lcs_size = max(lcs_count_list)
    meta_lcs_count = dict()
    for i in range(max_lcs_size+1):
        meta_lcs_count[i] = lcs_count_list.count(i)
    
    print(f"[debug.log] meta result count: \n{meta_lcs_count.items()}")

    # print(f"[debug.log] LCS count list: \n{lcs_count_list}")

    array1d_to_csv(result_dir+"lcs_count_list.csv", lcs_count_list)
    result_pool, result_index_list = lcs_extract(vector_pool, lcs_count_list, max_lcs_size, result_size)

    meta_result_list = meta_lcs_extract(result_index_list, commit_pool)

    # print(f"[debug.log] commit id and file path:\n{meta_result_list}")
    # print(f"[debug.log] result pool: \n{result_pool}")

    array2d_to_csv(result_dir+"meta_resultPool.csv", meta_result_list)
    array2d_to_csv(result_dir+"resultPool.csv", result_pool)

if __name__ == '__main__':
    main(sys.argv)