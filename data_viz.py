import sys
import os.path
from os import path
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends import pylab_setup
# Different methods for data visualization


def boxplot(Array, out_file_name, title):
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
    if path.exists(out_file_name):
        raise SystemExit('File already exits')

    plt.boxplot(Array)
    plt.title(title)
    plt.xlabel('Box')
    plt.ylabel('Distribution')
    plt.savefig(out_file_name, dpi=300)
    pass


