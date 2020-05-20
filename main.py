from pyfiglet import Figlet
from subprocess import call,STDOUT
import os
import video_steganography

if __name__ == '__main__':
    f = Figlet(font='slant')
    print(f.renderText("VideoSteganagraphy"))
    print("")

    print("Menu :")
    print("")
    print("(a) Encypt & Merge into Video")
    print("(b) Decrypt & Get the plain text")
    print("-----------------------")
    choice = input("(!) Choose option : ")

    if choice == "a":
        call(["clear"])

        print(f.renderText("Encrypt"))
        print("----------------------------------------")
        file_name = input("(1) Video file name in the data folder  ? : ")

        try:
            encode = int(input("(2) Encoding cypher n value  ? : "))
        except ValueError:
            print("-----------------------")
            print("(!) n is not an integer ")
            exit()

        try:
            open("/example_files/" + file_name)
        except IOError:
            print("-----------------------")
            print("(!) File not found ")
            exit()

        print("-----------------------")
        print("(-) Extracting Frame(s)")
        video_steganography.extract_frame(str(file_name))
        print("(-) Extracting audio")
        call(
            ["ffmpeg", "-i", "/example_files/" + str(file_name), "-q:a", "0", "-map", "a", "//temp/audio.mp3", "-y"],
            stdout=open(os.devnull, "w"), stderr=STDOUT)
        # useless
        print("(-) Reading text-to-hide.txt")
        print("(-) Encrypting & appending string into frame(s) ")
        video_steganography.encode_frame("temp", "/example_files/text-to-hide.txt", encode)
        print("(-) Merging frame(s) ")

        call(["ffmpeg", "-i", "/temp/%d.png", "-vcodec", "png", "/temp/video.mov", "-y"],
             stdout=open(os.devnull, "w"), stderr=STDOUT)

        print("(-) Optimizing encode & Merging audio ")
        call(["ffmpeg", "-i", "/temp/video.mov", "-i", "/temp/audio.mp3", "-codec", "copy",
              "/bin/Data/enc-" + str(file_name) + ".mov", "-y"], stdout=open(os.devnull, "w"), stderr=STDOUT)
        print("(!) Success , output : enc-" + str(file_name) + ".mov")

    elif choice == "b":
        call(["clear"])

        print(f.renderText("Decrypt"))
        print("----------------------------------------")
        file_name = input("(1) Video file name in the data folder  ? : ")

        try:
            encode = int(input("(2) Encoding cypher n value  ? : "))
        except ValueError:
            print("-----------------------")
            print("(!) n is not an integer ")
            exit()

        try:
            open("/bin/Data/" + file_name)
        except IOError:
            print("-----------------------")
            print("(!) File not found ")
            exit()

        print("-----------------------")
        print("(-) Extracting Frame(s)")
        video_steganography.extract_frame(str(file_name))
        print("(-) Decrypting Frame(s)")
        video_steganography.decode_frame("temp", encode)
        # useless
        print("(-) Writing to recovered-text.txt")
        print("(!) Success")

    else:
        exit()
