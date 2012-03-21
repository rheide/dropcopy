"""
    Copies all files from a given directory into another directory recursively,
    and deletes the original files.
    
    The use case of this is to be able to put files into your dropbox folder on one computer,
    and then run this script automatically/periodically on another computer to get a local backup
    of the files without your dropbox quota running out.
    
    Note that putting files into the dropbox folder is still a manual task. In the future I might
    write a script that can synchronize a folder automatically, only copying new files to the
    dropbox-folder-to-sync.
"""
import os
import shutil
import datetime

def safe_delete(fn):
    try:
        os.unlink(source_file)
    except IOError, e:
        # It's not fatal if we cannot delete the original file
        print "Warning: could not delete %s: %s" % (source_file, e)
    except WindowsError, e:
        print "Warning: could not delete %s: %s" % (source_file, e)


SOURCE_PATH = "C:\\Users\\randy\Dropbox\\photodump" # The path of a folder inside your dropbox. Files will be deleted from here!
TARGET_PATH = "P:\\photodump" # The path where your files should be copied to.

file_count = 0
for root, dirnames, filenames in os.walk(SOURCE_PATH):

    relative_path = root[len(SOURCE_PATH)+1:]
    target_path = os.path.join(TARGET_PATH, relative_path)
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    for fn in filenames:
        source_file = os.path.join(root, fn)
        target_file = os.path.join(target_path, fn)
        if os.path.exists(target_file):
            print "%s already exists. Skipping" % target_file
        else:
            print "Copying %s to %s" % (source_file, target_file)
            try:
                shutil.copyfile(source_file, target_file)
                file_count += 1
            except IOError, e:
                print "Error: %s" % e
                raise e
                exit(1)

        safe_delete(source_file)

# If we reach this point then all files copied successfully.
# We can let the user know that it's safe to delete them.
# Save the last sync time to dropbox
if file_count:
    # Only write timestamp if actually stuff copied,
    # otherwise dropbox will keep bothering us about file updates.
    ts = open(os.path.join(SOURCE_PATH, 'timestamp.txt'), 'w')
    ts.write("Synced at %s" % datetime.datetime.now())
    ts.close()

print "Complete. %s files copied." % file_count
exit(0)
