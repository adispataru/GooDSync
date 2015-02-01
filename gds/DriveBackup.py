__author__ = 'adrian'
import os
import pprint
import Util
import mimetypes

mimetypes.init()

class DriveBackup(object):
    def __init__(self, root_dir):
        super(DriveBackup, self)
        self.root_dir = root_dir
        self.folder_dict = {}
        self.service = None


    def _visit(self, arg, dirname, names):
        rel_path = dirname.replace(arg, "")
        dir_name = dirname[dirname.rfind('/')+1:len(dirname)]
        #beware of the pythonic list splitting
        parent_name = dirname[dirname[0:dirname.rfind('/')].rfind('/')+1:dirname.rfind('/')]
        print parent_name, dir_name
        if not rel_path:
            dir = Util.createFolder(self.service, "test", self.root_dir, dir_name)
            self.folder_dict[dir_name] = dir['id']
        else:
            dir = Util.createFolder(self.service, "test", self.folder_dict[parent_name], dir_name)
            self.folder_dict[dir_name] = dir['id']

        for name in names:
            if os.path.isdir(os.path.join(dirname, name)):
                continue
            pprint.pprint(os.path.join(dirname, name))
            pprint.pprint(mimetypes.guess_type(os.path.join(dirname, name)))
            fileMeta = Util.insert_file(self.service, name, "created with GDS", self.folder_dict[dir_name],
                                        mimetypes.guess_type(os.path.join(dirname, name))[0],
                                        os.path.join(dirname, name))
            print fileMeta['title']



        pprint.pprint(names)

    def createBackup(self, service, path):
        self.service = service
        tree = os.path.walk(path, self._visit, path)



