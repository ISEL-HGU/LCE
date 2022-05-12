import os
import sys
import csv
import numpy as np
import getopt

def csv_to_array(csv_file):
    f_csv_file = open(csv_file, 'r')
    result_array = csv.reader(f_csv_file)

    result_array = np.asarray(list(result_array))
    return result_array

def top_diff_to_text(vec):
    return

def main(argv):
    try:
        opts, args = getopt.getopt(argv[1:], "h:f:d:", ["help", "file", "directory"])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    file = ''
    gitdir = ''
    for o, a in opts:
        if o in ("-H", "--help") or o in ("-h", "--hash"):
            print("")
            sys.exit()
        elif o in ("-f", "--file"):
            file = a
        elif o in ("-d", "--directory"):
            gitdir = a
        else:
            assert False, "unhandled option"

    result_dir = "./result/"
    pool_dir = "./pool/"

    file = result_dir + file
    git_dir = pool_dir + gitdir

    result_array = csv_to_array(file)
    

if __name__ == '__main__':
    main(sys.argv)