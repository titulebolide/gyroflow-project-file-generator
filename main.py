import json
import click
import os
import sys
import traceback
from pathlib import Path
import subprocess
import re

def process_one_file(input, video):
    output = os.path.splitext(video)[0] + '.gyroflow'
    if (output == input):
         return
    video = Path(video).resolve().as_posix()
    with open(input, "r") as f:
        data = json.load(f)

    metadata = subprocess.check_output(f"ffprobe -select_streams v -show_streams \"{video}\" 2>/dev/null", shell=True).decode()

    fps = round(eval(re.findall("avg_frame_rate=(.*)\n", metadata)[0]),4)
    frame_count = int(re.findall("nb_frames=(.*)\n", metadata)[0])
    duration = round(float(re.findall("duration=(.*)\n", metadata)[0])*1000)

    output_video = "_stabilized".join(os.path.splitext(video))

    data["videofile"] = video
    data['video_info']['num_frames'] = frame_count
    data['video_info']['fps'] = fps
    data['video_info']['vfr_fps'] = fps
    data['video_info']['duration_ms'] = duration
    data['video_info']['vfr_duration_ms'] = duration
    data["gyro_source"]['filepath'] = video
    data['output']['output_path'] = output_video

    with open(output, 'w') as f:
        f.write(
            json.dumps(data, indent=2)
        )

@click.command()
@click.option('-i', "--input")
@click.argument("video", nargs=-1)
def main(input, video):
    for vid in video:
        try:
            process_one_file(input, vid) 
        except Exception as e:
            print(f"An error happened while treating {vid}, skipping :")
            print("".join(traceback.format_exception(*sys.exc_info())))




    

if __name__ == '__main__':
    main()
