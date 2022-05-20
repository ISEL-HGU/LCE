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
    lcs_count_list = list()
    for i in range(len(result_array)):
        commit_id_before_list.append(result_array[i][0])
        commit_id_after_list.append(result_array[i][1])
        file_path_before_list.append(result_array[i][2])
        file_path_after_list.append(result_array[i][3])
        lcs_count_list.append(result_array[i][4])
    return commit_id_before_list, commit_id_after_list, file_path_before_list, file_path_after_list, lcs_count_list

def top_n_to_diffs(project, commit_id_before_list, commit_id_after_list, file_path_before_list, file_path_after_list, lcs_count_list, git_dir, n, candidate_result_dir=None):
    pwd = os.getcwd()
    candidate_dir = candidate_result_dir
    if candidate_dir == None or candidate_dir == '':
        candidate_dir = pwd+"/candidates/"
    for i in range(n):
        if file_path_before_list[i] == file_path_after_list[i]:
            try:
                print(f"[debug.log] Generating patch candidate #{i}")
                print(f"[debug.log] Extracting git diff files ...")
                call(f"cd {git_dir}\ngit diff --output={pwd}/result/diff_{lcs_count_list[i]}_{i+1}.txt --unified=0 {commit_id_before_list[i]} {commit_id_after_list[i]} -- {file_path_before_list[i]}",shell=True)

                print(f"[debug.log] > Project           : {project}")
                print(f"[debug.log] > CommitID before   : {commit_id_before_list[i]}")
                print(f"[debug.log] > Path              : {file_path_before_list[i]}")
                call(f"cd {git_dir}\ngit checkout -f {commit_id_before_list[i]}; cp {git_dir}/{file_path_before_list[i]} {candidate_dir}{project}_rank_{i}_old.java", shell=True)

                print(f"[debug.log] > CommitID after    : {commit_id_after_list[i]}")
                print(f"[debug.log] > Path              : {file_path_after_list[i]}")
                call(f"cd {git_dir}\ngit checkout -f {commit_id_after_list[i]}; cp {git_dir}/{file_path_before_list[i]} {candidate_dir}{project}_rank_{i}_new.java", shell=True)
                print(f"[debug.log] resetting the git header to current HEAD ...")
                call(f"cd {git_dir}\ngit reset --hard HEAD\n")

            except:
                print(f"[debug.log] exception occured: {sys.exc_info()[0]}")
        else:
            print(f"[debug.log] file path different : {file_path_before_list[i]} -> {file_path_after_list[i]}")
    return

def main(argv):
    try:
        opts, args = getopt.getopt(argv[1:], "h:f:d:n:r:i:", ["help", "file", "directory", "number","resultDirectory", "hashID"])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    file = ''
    gitdir = ''
    n = 0
    candidates = ''
    hash = ''
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
        elif o in ("-r", "--resultDirectory"):
            candidates = a
        elif o in ("-h", "--hashID")
            hash = a
        else:
            assert False, "unhandled option"

    result_dir = "result/"
    pool_dir = "pool/"

    file = result_dir + file
    project = gitdir
    git_dir = os.getcwd() + "/" + pool_dir + gitdir

    result_array = csv_to_array(file)
    print(f"[debug.log] result array length : {len(result_array)}")
    commit_id_before_list, commit_id_after_list, file_path_before_list, file_path_after_list, lcs_count_list = seperate_commit_id_and_path(result_array)
    top_n_to_diffs(project, commit_id_before_list, commit_id_after_list, file_path_before_list, file_path_after_list, lcs_count_list, git_dir, n, candidates)
    # print(f"[debug.log] commit_id_before_list length : {len(commit_id_before_list)}")
    # print(f"[debug.log] commit_id_after_list length : {len(commit_id_after_list)}")
    # print(f"[debug.log] file_path_before_list length : {len(file_path_before_list)}")
    # print(f"[debug.log] file_path_after_list length : {len(file_path_after_list)}")    

if __name__ == '__main__':
    main(sys.argv)
