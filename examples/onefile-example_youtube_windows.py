from tsup.youtube.youtube_upload import YoutubeUpload
from tsup.youtube.validate_params import VideoSetting
from datetime import datetime, date, timedelta
import asyncio
from tsup.utils.tools import load_config_from_json
import os,json

# If it is the first time you've run the utility, a browser window should popup and prompt you to provide Youtube credentials. A token will be created and stored in request.token file in the local directory for subsequent use.



channelconfig = load_config_from_json(os.path.join(os.getcwd(),'examples/youtube-account-one.json'))

# auto install requirments for user
# checkRequirments()
uploader = YoutubeUpload(channelconfig)
today = date.today()


def instantpublish(video_settings):
    """Upload video using config."""



    # Loading configuration and validating
    try:
        uploader.upload_video(video_settings)
    except ValueError as e:
        print(e)


def saveasprivatedraft(video_settings):
    video_settings['publish_policy']=0
    # Loading configuration and validating
    try:
        uploader.upload_video(video_settings)
    except ValueError as e:
        print(e)



def scheduletopublish_tomorrow(video_settings):
    # mode a:release_offset exist,publishdate exist will take date value as a starting date to schedule videos
    # mode b:release_offset not exist, publishdate exist , schedule to this specific date
    # mode c:release_offset not exist, publishdate not exist,daily count to increment schedule from tomorrow
    # mode d: offset exist, publish date not exist, daily count to increment with specific offset schedule from tomorrow
    date_to_publish = datetime(today.year, today.month, today.day)
    hour_to_publish = "10:15"
    # if you want more delay ,just change 1 to other numbers to start from other days instead of tomorrow
    date_to_publish += timedelta(days=1)
    video_settings['release_date']=date_to_publish
    video_settings['publish_policy']=2
    # Loading configuration and validating
    try:
        uploader.upload_video(video_settings)
    except ValueError as e:
        print(e)


def checkfilebroken(path):
    print(f"check whether file exist{path}")
    if (os.path.exists(path)
        and os.path.getsize(path) > 0
    ):
        print(f'{path} is exist')
        return True
    else:
        print(f'{path} is not  exist')
        
        return False
def scheduletopublish_every7days(video_settings):
    # mode a:release_offset exist,publishdate exist will take date value as a starting date to schedule videos
    # mode b:release_offset not exist, publishdate exist , schedule to this specific date
    # mode c:release_offset not exist, publishdate not exist,daily count to increment schedule from tomorrow
    # mode d: offset exist, publish date not exist, daily count to increment with specific offset schedule from tomorrow
    date_to_publish = datetime(today.year, today.month, today.day)
    hour_to_publish = "17:15"
    # if you want more delay ,just change 1 to other numbers to start from other days instead of tomorrow
    date_to_publish += timedelta(days=7)
    # hour_to_publish=datetime.strptime(hour_to_publish, "%H:%M")

    # print('after convert',hour_to_publish.strftime("%I:%M %p").strip("0"))
    video_settings['release_date']=date_to_publish
    video_settings['publish_policy']=2
    # Loading configuration and validating
    try:
        uploader.upload_video(video_settings)
    except ValueError as e:
        print(e)

def scheduletopublish_at_specific_date(video_settings):
    # mode a:release_offset exist,publishdate exist will take date value as a starting date to schedule videos
    # mode b:release_offset not exist, publishdate exist , schedule to this specific date
    # mode c:release_offset not exist, publishdate not exist,daily count to increment schedule from tomorrow
    # mode d: offset exist, publish date not exist, daily count to increment with specific offset schedule from tomorrow
    date_to_publish = datetime(today.year, today.month, today.day)
    hour_to_publish = "10:15"
    # if you want tomorrow ,just change 7 to 1
    date_to_publish += timedelta(days=3)
    # date_to_publish = datetime.strftime(date_to_publish, "%Y-%m-%d %H:%M:%S")
    video_settings['release_date']=date_to_publish
    video_settings['publish_policy']=2

    # Loading configuration and validating
    try:
        uploader.upload_video(video_settings)
    except ValueError as e:
        print(e)

video_settings = load_config_from_json(os.path.join(os.getcwd(),'examples/youtube-test-video.json'))

# checkfilebroken(channel_cookie_path)
# checkfilebroken(thumbnail_local_path)
# checkfilebroken(videopath)
scheduletopublish_tomorrow(video_settings)
scheduletopublish_at_specific_date(video_settings)
scheduletopublish_every7days(video_settings)
saveasprivatedraft(video_settings)
instantpublish(video_settings)
# friststart()
