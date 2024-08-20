""" Put a file called captions.sbv in this directory, run the script, and a transcript will be printed. """

from file_io import get_file_contents


def main():
    print("[Auto-generated transcript:] ", end='')
    sbv_contents = get_file_contents('captions.sbv')
    for i, line in enumerate(sbv_contents.split('\n')):
        if i % 3 == 1:
            print(line, end=' ')


if __name__ == '__main__':
    main()
