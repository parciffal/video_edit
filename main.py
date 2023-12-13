from src.models.record_video import VideoRecorder
from src.models.add_loom_to_video import MergeVideos


def record():
    email = "Mariam@hopperhq.com"
    password = "jLJL]^x{U2E@_x^e2"
    linkedin_email = "georgemamajanyan97@gmail.com"
    linkedin_pass = ">bxPVuv[9Q@3tz:p"
    file_name = "data/inputs/scenar - BK30.csv"
    video_recorder = VideoRecorder(email, password, linkedin_email, linkedin_pass, file_name)
    video_recorder.run()


def canva():
    email = "film2015trailers@gmail.com"
    password = "edgar0147"
    merge_videos = MergeVideos(email, password)
    merge_videos.run()


if __name__ == "__main__":
    record()