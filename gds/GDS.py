__author__ = 'adrian'


import Util
import DriveBackup
import Session
import DriveRecovery
import argparse

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-b", "--backup", action="store_true", help='create a backup in google drive')
    group.add_argument('-r', '--recover', help='recover from google drive backup', action="store_true")
    parser.add_argument('local_dir', type=str, help='local directory (for backup or recovery)')
    parser.add_argument('--remote_dir', type=str, help='remote directory for recovery')
    args = parser.parse_args()
    if args.backup:
        backup(args.local_dir)
    elif args.recover:
        recover(args.remote_dir, args.local_dir)

def backup(local_dir):
    session = Session.Session()
    drive_service = session.getService()

    files = Util.retrieve_all_files(drive_service)
    root_dir = Util.get_root_id(files)
    backup_service = DriveBackup.DriveBackup(root_dir)
    backup_service.createBackup(drive_service, local_dir)


def recover(remote_dir, local_dir):
    session = Session.Session()
    drive_service = session.getService()

    files = Util.retrieve_all_files(drive_service)
    root_dir = Util.get_dir_id(files, remote_dir)
    print root_dir
    recovery_service = DriveRecovery.DriveRecovery(local_dir)
    recovery_service.restore_from_backup(drive_service, root_dir)