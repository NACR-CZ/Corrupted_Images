import os
import PIL.Image
from PIL import Image
import csv


def get_path(dirs_to_check):
    """Checks path input"""
    input_path = input(wh + 'Specify path to folder/s containing images: ')
    try:
        os.path.exists(input_path)
    except NotADirectoryError:
        print('Path is not valid, quitting')
        quit()
    return input_path


def get_dirs(input_path, dirs_to_check):
    """Lists dirs from input"""
    image_path = input_path
    for root, dirs, files in os.walk(image_path):
        dirs_to_check.append(root)
        for i in dirs:
            dir_path = root + i
            dirs_to_check.append(dir_path)


def get_images(dirs_to_check):
    """Lists images to a set"""
    images_set = set()
    for i in dirs_to_check:
        for root, dirs, files in os.walk(i):
            for f_name in files:
                if (not f_name.lower().endswith('.jp2')
                        and not f_name.lower().endswith('.jpg')
                        and not f_name.lower().endswith('.jpeg')
                        and not f_name.lower().endswith('.tif')
                        and not f_name.lower().endswith('.tiff')
                        and not f_name.lower().endswith('.png')
                        and not f_name.lower().endswith('.jxl')):
                    continue
                else:
                    file = os.path.normpath(root) + '/' + f_name
                    images_set.add(file)
    if len(images_set) == 0:
        print('None image has been found, quitting.')
        quit()
    return images_set


def is_corrupted(image, decomp_bomb):
    """Checks images"""
    try:
        with Image.open(image) as img:
            img.verify()
        return False
    except PIL.Image.DecompressionBombError:
        decomp_bomb.append(image)
        return False
    except PIL.Image.DecompressionBombWarning:
        decomp_bomb.append(image)
        return False
    except:
        return True


def corrupted(images_set):
    """Appends corrupted images to the set"""
    corrupted = []
    for image in images_set:
        if is_corrupted(image, decomp_bomb):
            corrupted.append(image)
    return corrupted


def check_nums(images_set, corrupted, decomp_bomb, path, dirs_to_check):
    """Returns numbers of corrupted images grouped by formats"""
    jpg = []
    png = []
    tif = []
    jp2 = []
    jxl = []
    for i in corrupted:
        if '.jp2' in str(i):
            jp2.append(i)
        elif '.jxl' in str(i):
            jxl.append(i)
        elif '.png' in str(i):
            png.append(i)
        elif '.tif' in str(i) or '.tiff' in str(i):
            tif.append(i)
        elif '.jpeg' in str(i) or '.jpg' in str(i):
            jpg.append(i)
        else:
            pass
    if len(corrupted) == 0:
        print('Result: ' + str(len(images_set) - len(decomp_bomb)) + ' images inside ' + str(dirs_to_check[0]) + ' were'
                                                                     ' checked succesfully.'
              '\n        Images with Decompression Error/Warnings found: ' + (str(len(decomp_bomb))))

    else:
        print('Result:\nImages with Errors found in total: ' + str(len(corrupted) - len(jxl)))
        print('From which: \nCorrupted JPEGs: ' + (str(len(jpg))), '\nCorrupted JPEG2000s: ' + (str(len(jp2))),
              '\nCorrupted PNGs: ' + (str(len(png))), '\nCorrupted TIFFs: ' +
              (str(len(tif))), '\nImages with Decompression Error/Warnings: ' + (str(len(decomp_bomb))),
              '\nJXLs (Note: JXLs can´t be checked using PIL module): ' + (str(len(jxl))))
        csv_file = (path + '/reports/corrupted_list.csv')
        if len(corrupted) > 0 or len(decomp_bomb) > 0:
            print(rd + "Result with details can be found inside /reports/")
        else:
            pass
        with open(csv_file, 'w', encoding='utf8') as f:
            writer = csv.writer(f)
            f.write('Images checked by Python Pillow Module - Corrupted_Images_Script by NACR' +
                    '\n-------------------------------------------------------------------------\n' +
                    '\nNumb. of images checked in total: ' + str(len(images_set))
                    + '\n\n-------------------------------------------------------------------------\n'
                    + 'Corrupted:\n')
            for i in corrupted:
                f.write(str(i) + '\n')
            f.write('\n-------------------------------------------------------------------------\n' +
                    'Images which can not be checked due to DecompressionBombError/Warning:')
            for i in decomp_bomb:
                f.write(str(i) + '\n')
        f.close()
    return jpg, png, tif, jp2, jxl


if __name__ == '__main__':
    logo_small = """
                                       NNN    NN   AAAAA    CCCCC  RRRR
                                       NN NN  NN  AA   AA  CCC     RR  RR
                                       NN  NN NN  AAAAAAA  CCC     RRRRR
                                       NN    NNN  AA   AA   CCCCC  RR  RR
    """
    bl = '\033[1;34;40m'
    cy = '\033[96m'
    wh = '\33[97m'
    rd = '\33[91m'

    print(bl + logo_small)
    user = (os.getlogin())
    user = user.title()

    separator = '='
    padding = str('\/' * 10)
    welcome = padding + ' Dear user "' + str(user) + '", welcome to Corrupted_Images by NAČR. ' + padding
    print(cy + welcome)
    print((len(welcome) * separator))
    path = (os.path.dirname(__file__))
    try:
        os.makedirs(path + '/reports/')
    except FileExistsError:
        pass
    dirs_to_check = []
    input_path = get_path(dirs_to_check)
    get_dirs(input_path, dirs_to_check)
    images_set = get_images(dirs_to_check)
    unidentified = []
    decomp_bomb = []
    if len(images_set) == 1:
        print('One image has been found.')
    else:
        print('Images have been found in total: ' + str(len(images_set)))
    corrupted = corrupted(images_set)
    jpg, png, tif, jp2, jxl = check_nums(images_set, corrupted, decomp_bomb, path, dirs_to_check)
    
