import os

# Caching dict.
import io

_f_cache = {}

class ConfigFile(object):
    """
    The abstract base class for a ConfigFile object. All config files extend from this.

    This provides several methods that don't need to be re-implemented in sub classes.
    For example, it automatically provides opening of the file and creating it if it doesn't exist, and provides a basic reload() method to automatically reload the files from disk.
    """

    def __init__(self, fd):
        self.loaded = False
        # Check if fd is a string
        if isinstance(fd, str):
            self.path = fd.replace('/', '.').replace('\\', '.')
            # Open the file.
            try:
                fd = open(fd)
            except FileNotFoundError:
                # Make sure the directory exists.
                if not os.path.exists('/'.join(fd.split('/')[:-1])) and '/' in fd:
                        os.makedirs('/'.join(fd.split('/')[:-1]))
                # Open it in write mode, then re-open it.
                open(fd, 'w').close()
                fd = open(fd, 'r')
        else:
            self.path = fd.name.replace('/', '.').replace('\\', '.')
        self.fd = fd

    def __new__(cls, fd, *args, **kwargs):
        if isinstance(fd, str):
            path = fd.replace('/', '.').replace('\\', '.')
        else:
            path = fd.name.replace('/', '.').replace('\\', '.')
        cached_ob = get_from_cache(path)
        if cached_ob is None:
            ob = super().__new__(cls)
            add_to_cache(ob)
            return ob
        else:
            return cached_ob


    def dump(self):
        """
        Abstract dump method.
        """
        raise NotImplementedError

    def load(self):
        """
        Abstract load method.
        """
        raise NotImplementedError

    def reload(self):
        """
        Automatically reloads the config file.

        This simply re-creates the class, copies over it's __dict__ and deletes the re-created class.
        """
        # Close the FD.
        self.fd.close()
        # Reload the file.
        newcls = self.__class__(self.fd.name)
        # Get the new class' dict.
        ndict = newcls.__dict__
        # Update our own dict.
        self.__dict__ = ndict
        # Delete the old class.
        del newcls
        del ndict
        # Reloaded.

def add_to_cache(ob: ConfigFile):
    _f_cache[ob.path] = ob

def del_from_cache(ob: ConfigFile):
    if ob.path in _f_cache:
        del _f_cache[ob.path]

def get_from_cache(path: str):
    if path in _f_cache:
        return _f_cache[path]
