"""
Matt's Own Version of pickle
Author: Matthew R. Ware (mrware91@gmail.com)
Description: Tools to save and load python variables fast and efficiently.
"""
import pickle

def load_obj(filename ):
    """
    Loads object from name.pkl and returns its value

    Args:
        filename: String designating directory and name of file, ie. /Folder/Filename, where Filename.pkl is the object

    Returns:
        The value of the object in filename
    """
    try:
        with open(filename + '.pkl', 'rb') as f:
            print filename+" remembered!"
            return pickle.load(f)
    except IOError as e:
        print "IOError: Did you load the correct file? %s" % filename
        raise e


def save_obj(obj, filename ):
    """
    Saves object from filename.pkl

    Args:
        obj: The python object to save
        filename: String designating directory and name of file, ie. /Folder/Filename, where Filename.pkl is the object
    """
    with open(filename + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
