__author__ = 'adrian'

import os
import Util

class DriveRecovery(object):

    def __init__(self, path):
        super(DriveRecovery, self)
        self.path = path
        self.folder_dict = {}

    def restore_from_backup(self, service, drive_backup):
        try:
            os.mkdir(self.path)
        except OSError:
            pass
        children = Util.print_files_in_folder(service, drive_backup)
        self.folder_dict[drive_backup] = self.path
        while children:
            child = children.pop()
            parent_id = Util.get_parent_id(service, child['id'])
            print 'Working with child:', child['title'], child['id']
            if child['mimeType'] == 'application/vnd.google-apps.folder':
                os.mkdir(os.path.join(self.folder_dict[parent_id],child['title']))
                children.extend(Util.print_files_in_folder(service, child['id']))
                self.folder_dict[child['id']] = os.path.join(self.folder_dict[parent_id],child['title'])
            else:
                fileContent = Util.download_file(service, child)
                Util.fileWrite(self.folder_dict[parent_id], child['title'], fileContent)

        return None
