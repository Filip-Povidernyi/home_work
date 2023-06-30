from os import rename, makedirs, listdir, rmdir
from pathlib import Path
from shutil import move, unpack_archive
import sys



def check_rename_dir(p):
    '''Itering folders in Path folder. Recursing folders and check files. Rename folders'''

    for object in p.iterdir():
        
        if object.is_file():

            obj_suf = object.suffix
            check_file(obj_suf, object)
        
        else:

            name = normalize(object)
            new_fd = str(p) + '/' + name
            rename(object, new_fd)
            check_rename_dir(Path(new_fd))

    


def check_file(obj_suf, object):
    '''Checking file suffixes and sorting file"s names by lists '''
    

    if obj_suf.lower() in ('.jpeg', '.png', '.jpg', '.svg', '.tif'):
        images.append(object)
        
    elif obj_suf.lower() in ('.avi', '.mp4', '.mov', '.mkv', '.vob'):
        videos.append(object)

    elif obj_suf.lower() in ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx', '.json'):
        docs.append(object)

    elif obj_suf.lower() in ('.mp3', '.ogg', '.wav', '.amr'):
        audio.append(object)

    elif obj_suf.lower() in ('.zip', '.gztar', '.bztar', '.xztar', '.tar'):
        archives.append(object)

    else:
        other.append(object)

    


def normalize(obj, flag=False):
    
    #Translate and change unknows symbols in names folders and files
    # if you need translate string use flag=True, for Path-name - flag=False

    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    SYMB_DIGIT = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '/', ':', '\\')
    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):  

        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
        
    if not flag:
        obj_name = (obj.name).translate(TRANS)

    else:
        obj_name = obj.translate(TRANS)

    trans_name = ''
    for char in obj_name:

        if char  in SYMB_DIGIT or  'a' <= char <= 'z' or 'A' <= char <= 'Z':
            trans_name += char

        else:
            trans_name += '_'       
        
    return trans_name


def move_files(images, videos, docs, audio, archives, other, p):

    # Create new folders. Sort and move files in this folders

    fd_path_images = str(p) + '/' + 'images'
    fd_path_videos = str(p) + '/' + 'videos'
    fd_path_docs = str(p) + '/' + 'documents'
    fd_path_audio = str(p) + '/' + 'audio'
    fd_path_archives = str(p) + '/' + 'archives'
    fd_path_other = str(p) + '/' + 'other'

    makedirs(fd_path_images, exist_ok=True)
    makedirs(fd_path_videos, exist_ok=True)
    makedirs(fd_path_docs, exist_ok=True)
    makedirs(fd_path_audio, exist_ok=True)
    makedirs(fd_path_archives, exist_ok=True)
    makedirs(fd_path_other, exist_ok=True)
    

    for video in videos:

        trans_name = normalize(video)
        new_path = str(fd_path_videos) + '/' + str(trans_name)
        move(video, new_path)

    for image in images:

        trans_name = normalize(image)
        new_path = str(fd_path_images) + '/' + str(trans_name)
        move(image, new_path)

    for doc in docs:

        trans_name = normalize(doc)
        new_path = str(fd_path_docs) + '/' + str(trans_name)
        move(doc, new_path)

    for track in audio:

        trans_name = normalize(track)
        new_path = str(fd_path_audio) + '/' + str(trans_name)
        move(track, new_path)


    for archive in archives:

        trans_name = normalize(archive)
        new_path = str(fd_path_archives) + '/' + str(trans_name)
        unpack_archive(archive, new_path)

    for file in other:

        trans_name = normalize(file)
        new_path = str(fd_path_other) + '/' + str(trans_name)
        move(file, new_path)

def main():
         
    arg = sys.argv[1]
    p = Path(arg)
    
    check_rename_dir(p)
    move_files(images, videos, docs, audio, archives, other, p)
    remove_empty_dirs(p)

def remove_empty_dirs(p):

    #Removing empty folders

    for object in p.iterdir():

        if object.is_dir():
                
            empty = listdir(object)
                
            if (not empty and object.name != 'images' and object.name != 'videos' and object.name != 'documents' and 
                object.name != 'audio' and object.name != 'archives' and object.name != 'other'):

                rmdir(object)

            else:
                remove_empty_dirs(object)

                


images, videos, docs, audio, archives, other = [], [], [], [], [], []



if __name__ == "__main__":
    main()


