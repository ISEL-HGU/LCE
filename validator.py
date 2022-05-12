import csv
import getopt
import os
import sys
import numpy as np
from subprocess import call

def csv_to_array(csv_file):
    f_csv_file = open(csv_file, 'r')
    result_array = csv.reader(f_csv_file)

    result_array = np.asarray(list(result_array))
    return result_array

def seperate_commit_id_and_path(result_array):
    commit_id_before_list = list()
    commit_id_after_list = list()
    file_path_before_list = list()
    file_path_after_list = list()
    for i in range(len(result_array)):
        commit_id_before_list.append(result_array[i][0])
        commit_id_after_list.append(result_array[i][1])
        file_path_before_list.append(result_array[i][2])
        file_path_after_list.append(result_array[i][3])
    return commit_id_before_list, commit_id_after_list, file_path_before_list, file_path_after_list

def top_n_to_diffs(commit_id_before_list, commit_id_after_list, file_path_before_list, file_path_after_list, git_dir, n):
    pwd = os.getcwd()
    for i in range(n):
        if file_path_before_list[i] == file_path_after_list[i]:
            try:
                call(f"cd {git_dir}\ngit diff --output={pwd}\\result\\diff_{i+1}.txt {commit_id_before_list[i]} {commit_id_after_list[i]} {file_path_before_list[i]} >> result_{i+1}.txt",shell=True)
                print(f"\n[execution.log] cd {git_dir}\n[execution.log] git diff {commit_id_before_list[i]} {commit_id_after_list[i]} {file_path_before_list[i]} > {pwd}\\result\\diff_{i+1}.txt")
            except:
                print(f"[debug.log] exception occured: {sys.exc_info()[0]}")
        else:
            print(f"[debug.log] file path different : {file_path_before_list[i]} -> {file_path_after_list[i]}")
    return

def main(argv):
    try:
        opts, args = getopt.getopt(argv[1:], "h:f:d:n:", ["help", "file", "directory", "number"])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    file = ''
    gitdir = ''
    n = 0
    for o, a in opts:
        if o in ("-H", "--help") or o in ("-h", "--hash"):
            print("")
            sys.exit()
        elif o in ("-f", "--file"):
            file = a
        elif o in ("-d", "--directory"):
            gitdir = a
        elif o in ("-n", "--number"):
            n = int(a)
        else:
            assert False, "unhandled option"

    result_dir = "result\\"
    pool_dir = "pool\\"

    file = result_dir + file
    git_dir = os.getcwd() + "\\" + pool_dir + gitdir

    result_array = csv_to_array(file)
    print(f"[debug.log] result array length : {len(result_array)}")
    commit_id_before_list, commit_id_after_list, file_path_before_list, file_path_after_list = seperate_commit_id_and_path(result_array)
    top_n_to_diffs(commit_id_before_list, commit_id_after_list, file_path_before_list, file_path_after_list, git_dir, n)
    # print(f"[debug.log] commit_id_before_list length : {len(commit_id_before_list)}")
    # print(f"[debug.log] commit_id_after_list length : {len(commit_id_after_list)}")
    # print(f"[debug.log] file_path_before_list length : {len(file_path_before_list)}")
    # print(f"[debug.log] file_path_after_list length : {len(file_path_after_list)}")    

if __name__ == '__main__':
    main(sys.argv)
