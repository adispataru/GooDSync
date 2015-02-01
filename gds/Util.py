__author__ = 'adrian'
from googleapiclient import errors
from googleapiclient.discovery import MediaFileUpload
import pprint
import os

FILE_DICT = {}

def retrieve_all_files(service):
    """Retrieve a list of File resources.

    Args:
    service: Drive API service instance.
    Returns:
    List of File resources.
    """
    result = []
    page_token = None
    while True:
        try:
            param = {}
            if page_token:
                param['pageToken'] = page_token
            files = service.files().list(**param).execute()
            for f in files['items']:
                FILE_DICT[f['id']] = f

            result.extend(files['items'])
            page_token = files.get('nextPageToken')
            if not page_token:
                break
        except errors.HttpError, error:
          print 'An error occurred: %s' % error
          break
    return result


def print_files_in_folder(service, folder_id):
    """Print files belonging to a folder.

    Args:
    service: Drive API service instance.
    folder_id: ID of the folder to print files from.
    """
    page_token = None
    result = []
    while True:
        try:
            param = {}
            if page_token:
                param['pageToken'] = page_token
            children = service.children().list(
                      folderId=folder_id, **param).execute()

            for child in children.get('items', []):
                result.append(FILE_DICT[child['id']])
            page_token = children.get('nextPageToken')
            if not page_token:
                break
        except errors.HttpError, error:
          print 'An error occurred: %s' % error
          break
    return result


def download_file(service, drive_file):
    """Download a file's content.

    Args:
    service: Drive API service instance.
    drive_file: Drive File instance.

    Returns:
    File's content if successful, None otherwise.
    """
    download_url = drive_file.get('downloadUrl')
    if download_url:
        resp, content = service._http.request(download_url)
        if resp.status == 200:
          print 'Status: 200'
          return content
        else:
          print 'An error occurred: %s' % resp
          return None
    else:
        print "The file doesn't have any content stored on Drive."
        return None




def fileWrite(path, title, fileContent):
    file = open(os.path.join(path, title), "w")
    file.write(fileContent)
    file.close()

def extract_folders(service, files):
    queue = []
    result = []
    for file in files:
        if file['mimeType'] == 'application/vnd.google-apps.folder':
            for parent in file['parents']:
                if parent['isRoot']:
                    result.append(file)
                    queue.append(file)
    # for folder in queue:
    # 	files = print_files_in_folder(service, folder['id'])
    # 	while files:
    # 		file = files.pop()
    # 		if file['id'] in FILEDICT.keys() and FILEDICT[file['id']]['mimeType'] == 'application/vnd.google-apps.folder':
    # 			result.append(FILEDICT[file['id']])
    # 			pprint.pprint(FILEDICT[file['id']]['title'])
    # 		 	queue.append(FILEDICT[file['id']])
    return result


def get_root_id(files):
    for file in files:
        if file['mimeType'] == 'application/vnd.google-apps.folder':
            for parent in file['parents']:
                if parent['isRoot']:
                    return parent['id']

def get_dir_id(files, dirname):
    for file in files:
        if file['mimeType'] == 'application/vnd.google-apps.folder':
            if file['title'] == dirname:
                return file['id']


def createFolder(service, description, parent_id, name):
    return insert_file(service, name, description, parent_id, "application/vnd.google-apps.folder", None)

def insert_file(service, title, description, parent_id, mime_type, filename):
    """Insert new file.

    Args:
    service: Drive API service instance.
    title: Title of the file to insert, including the extension.
    description: Description of the file to insert.
    parent_id: Parent folder's ID.
    mime_type: MIME type of the file to insert.
    filename: Filename of the file to insert.
    Returns:
    Inserted file metadata if successful, None otherwise.
    """

    body = {
    'title': title,
    'description': description,
    'mimeType': mime_type
    }
    media_body= None
    if not filename is None:
        media_body = MediaFileUpload(filename, mimetype=mime_type)
    pprint.pprint(body)
    pprint.pprint(media_body)
    # Set the parent folder.
    if parent_id:
        body['parents'] = [{'id': parent_id}]

    try:
        file = None
        if filename == None:
            file = service.files().insert(body=body).execute()
        else:
            file = service.files().insert(
            body=body,
            media_body=media_body).execute()

        # Uncomment the following line to print the File ID
        # print 'File ID: %s' % file['id']

        return file
    except errors.HttpError, error:
        print 'An error occured: %s' % error
        return None


def get_parent_id(service, file_id):
    parents = service.parents().list(fileId=file_id).execute()
    p_id = None
    for parent in parents['items']:
        p_id = parent['id']

    return p_id