import sys
import os.path
from os import path
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends import pylab_setup
# Different methods for data visualization


def boxplot(Array, out_file_name, title, box_names):
    """ Boxplot of numerical array and give specified name
    Parameters
    --------
    L :  Parallel array
        Parallel array contains lists of integers or floats
    out_file_name : file name
        File name of the output file
    title : Title of figure
    Returns
    --------
        Generate file with specified name containing boxplot
        , tile and labeled axist
    Raises
    --------
    NameError
        No output file name
    SystemExit
        File exits
    """
    # Check input
    if out_file_name is None:
        raise NameError('Out_file_name required')
        sys.exit(1)

    plt.boxplot(Array)
    plt.title(title)
    plt.xlabel('Box')
    plt.ylabel('Distribution')
    plt.xticks(range(1, len(box_names)+1), box_names, rotation='vertical')
    plt.savefig(out_file_name, dpi=300)
    sys.exit(0)
