
# coding: utf-8

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import pympi
import os
import re
from fnmatch import fnmatch
import argparse



parser = argparse.ArgumentParser(description='Extract video parts based on annotations')
parser.add_argument('-gloss','--g', type=str, help='annotation to be extracted')
parser.add_argument('-video', '--v', type=str, help='video name / optional', default="default")
args = parser.parse_args()


def check_folders():
    directory1 = "./Extracted_videos"
    if not os.path.exists(directory1):
        os.makedirs(directory1)


root = './'
pattern = "*.eaf"
for root, dirs, files in os.walk(root, topdown=False):
    for name in files:
        if fnmatch(name, pattern):
            if args.v == "default":
                video_name = re.sub('\.eaf$', '', name)+".mp4"
            else:
                video_name = args.v
            file = pympi.Eaf(file_path=name)
            tier_names = file.get_tier_names()
            gloss = args.g
            check_folders()
            for tier_name in tier_names:
                annotations = file.get_annotation_data_for_tier(tier_name)
                count = 0
                for annotation in annotations:
                    if annotation[2] == gloss:
                        start = annotation[0]
                        end = annotation[1]
                        print(start/1000,end/1000)
                        ffmpeg_extract_subclip(video_name, start/1000, end/1000, targetname="Extracted_videos/"+"%#05d.mp4" % (count+1))
                        count = count+1
                if count == 0:
                    print("No annotation found with this name")