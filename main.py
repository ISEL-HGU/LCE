import csv
import getopt
import sys

def main(argv):
    try:
        opts, args = getopt.getopt(argv[1:], "H:t:k:p:c:h:", ["help", "train", "k_neighbors", "predict", "cutoff", "hash"])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)

if __name__ == '__main__':
    main(sys.argv)