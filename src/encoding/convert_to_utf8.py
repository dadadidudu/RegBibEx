import os

# currently unused

def get_encoding_with_chardet(file):
    """ get file encoding type """
    with open(file, 'rb') as f:
        rawdata = f.read()
    from chardet import detect
    return detect(rawdata)['encoding']


def convert_to_utf8(srcfile):
    """ This will convert srcfile of unknown encoding to utf-8. """
    from_codec = get_encoding_with_chardet(srcfile)
    trgfile = "temp.tmp"

    try:
        with open(srcfile, 'r', encoding=from_codec) as f, open(trgfile, 'w', encoding='utf-8') as e:
            text = f.read()  # for small files, for big use chunks
            e.write(text)

        os.remove(srcfile)  # remove old encoding file
        os.rename(src=trgfile, dst=srcfile)  # rename new encoding
    except UnicodeDecodeError:
        print('Decode Error')
    except UnicodeEncodeError:
        print('Encode Error')

def convert_string_to_utf8(srcstring) -> str:
    pass