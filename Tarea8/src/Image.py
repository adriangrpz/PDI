from PIL import Image as TkImage

class Image():

    """
    Constructor
    Given a file path, stores two copies of the image stored in the file
    """
    def __init__(self, path):
        size = 500, 500
        self.original = TkImage.open(path)
        self.modified = TkImage.open(path)
        self.original.thumbnail(size,TkImage.ANTIALIAS)
        self.modified.thumbnail(size,TkImage.ANTIALIAS)
