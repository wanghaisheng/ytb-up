from tsup.youtube.youtube_upload import YoutubeUpload
from tsup.youtube.validate_params import VideoSetting
from datetime import datetime, date, timedelta
import asyncio
from tsup.utils.tools import load_config_from_json
import os,json

# If it is the first time you've run the utility, a browser window should popup and prompt you to provide Youtube credentials. A token will be created and stored in request.token file in the local directory for subsequent use.



wait = 0
# 0-wait uploading done
# 1-wait Processing done
# 2-wait Checking done

channelconfig = load_config_from_json('youtube-account-test.json')

# auto install requirments for user
# checkRequirments()
upload = YoutubeUpload(channelconfig)
today = date.today()


def instantpublish(upload_video,video_settings):
    """Upload video using config."""

    videosettings = {

            "video_title": video_settings.get('video_title', VideoSetting.default_values['video_title']),
            "video_description": video_settings.get('video_description', VideoSetting.default_values['video_description']),
            "wait_policy": video_settings.get('wait_policy', VideoSetting.default_values['wait_policy']),
            "thumbnail_local_path": video_settings.get('thumbnail_local_path', VideoSetting.default_values['thumbnail_local_path']),
            "publish_policy": video_settings.get('publish_policy', VideoSetting.default_values['publish_policy']),
            "tags": video_settings.get('tags', VideoSetting.default_values['tags']),
            "release_date": video_settings.get('release_date', VideoSetting.default_values['release_date']),
            "release_date_hour": video_settings.get('release_date_hour', VideoSetting.default_values['release_date_hour']),
            "playlist": video_settings.get('playlist', VideoSetting.default_values['playlist']),
            "is_age_restriction": video_settings.get('is_age_restriction', VideoSetting.default_values['is_age_restriction']),
            "is_not_for_kid": video_settings.get('is_not_for_kid', VideoSetting.default_values['is_not_for_kid']),
            "is_paid_promotion": video_settings.get('is_paid_promotion', VideoSetting.default_values['is_paid_promotion']),
            "is_automatic_chapters": video_settings.get('is_automatic_chapters', VideoSetting.default_values['is_automatic_chapters']),
            "is_featured_place": video_settings.get('is_featured_place', VideoSetting.default_values['is_featured_place']),
            "video_language": video_settings.get('video_language', VideoSetting.default_values['video_language']),
            "captions_certification": video_settings.get('captions_certification', VideoSetting.default_values['captions_certification']),
            "video_film_date": video_settings.get('video_film_date', VideoSetting.default_values['video_film_date']),
            "video_film_location": video_settings.get('video_film_location', VideoSetting.default_values['video_film_location']),
            "license_type": video_settings.get('license_type', VideoSetting.default_values['license_type']),
            "is_allow_embedding": video_settings.get('is_allow_embedding', VideoSetting.default_values['is_allow_embedding']),
            "is_publish_to_subscriptions_feed_notify": video_settings.get('is_publish_to_subscriptions_feed_notify', VideoSetting.default_values['is_publish_to_subscriptions_feed_notify']),
            "shorts_remixing_type": video_settings.get('shorts_remixing_type', VideoSetting.default_values['shorts_remixing_type']),
            "categories": video_settings.get('categories', VideoSetting.default_values['categories']),
            "comments_ratings_policy": video_settings.get('comments_ratings_policy', VideoSetting.default_values['comments_ratings_policy']),
            "is_show_howmany_likes": video_settings.get('is_show_howmany_likes', VideoSetting.default_values['is_show_howmany_likes']),
            "is_monetization_allowed": video_settings.get('is_monetization_allowed', VideoSetting.default_values['is_monetization_allowed']),
            "first_comment": video_settings.get('first_comment', VideoSetting.default_values['first_comment']),
            "subtitles": video_settings.get('subtitles', VideoSetting.default_values['subtitles'])
        }


    # Loading configuration and validating
    try:
        upload_video(videosettings)
    except ValueError as e:
        print(e)


def saveasprivatedraft():
    asyncio.run(
        upload.upload(
            video_local_path=videopath,
            video_title="private draft-test-004",
            video_description=video_description,
            thumbnail_local_path=thumbnail_local_path,
            tags=tags,
            publish_policy=0,
        )
    )


def scheduletopublish_tomorrow():
    # mode a:release_offset exist,publishdate exist will take date value as a starting date to schedule videos
    # mode b:release_offset not exist, publishdate exist , schedule to this specific date
    # mode c:release_offset not exist, publishdate not exist,daily count to increment schedule from tomorrow
    # mode d: offset exist, publish date not exist, daily count to increment with specific offset schedule from tomorrow
    date_to_publish = datetime(today.year, today.month, today.day)
    hour_to_publish = "10:15"
    # if you want more delay ,just change 1 to other numbers to start from other days instead of tomorrow
    date_to_publish += timedelta(days=1)
    # asyncio.get_event_loop().run_until_complete(
    #     upload.upload(
    #         videopath=videopath,
    #         video_title="tomorrow-test-001",
    #         video_description=video_description,
    #         thumbnail_local_path=thumbnail_local_path,
    #         tags=tags,
    #         publishpolicy=2,
    #         date_to_publish=date_to_publish,
    #         hour_to_publish=hour_to_publish,
    #     )
    # )
    asyncio.run(
        upload.upload(
            video_local_path=videopath,
            video_title="tomorrow-test-001",
            video_description=video_description,
            thumbnail_local_path=thumbnail_local_path,
            tags=tags,
            publish_policy=2,
            release_date=date_to_publish,
            release_date_hour=hour_to_publish,
        )
    )

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
def scheduletopublish_every7days():
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

    asyncio.run(
        upload.upload(
            video_local_path=videopath,
            video_title="7days later-test-003",
            video_description=video_description,
            thumbnail_local_path=thumbnail_local_path,
            tags=tags,
            publish_policy=2,
            release_date=date_to_publish,
            release_date_hour=hour_to_publish,
        )
    )


def scheduletopublish_at_specific_date():
    # mode a:release_offset exist,publishdate exist will take date value as a starting date to schedule videos
    # mode b:release_offset not exist, publishdate exist , schedule to this specific date
    # mode c:release_offset not exist, publishdate not exist,daily count to increment schedule from tomorrow
    # mode d: offset exist, publish date not exist, daily count to increment with specific offset schedule from tomorrow
    date_to_publish = datetime(today.year, today.month, today.day)
    hour_to_publish = "10:15"
    # if you want tomorrow ,just change 7 to 1
    date_to_publish += timedelta(days=3)
    # date_to_publish = datetime.strftime(date_to_publish, "%Y-%m-%d %H:%M:%S")
    asyncio.run(
        upload.upload(
            video_local_path=videopath,
            video_title="four days later-test-002",
            video_description=video_description,
            thumbnail_local_path=thumbnail_local_path,
            tags=tags,
            publish_policy=2,
            release_date=date_to_publish,
            release_date_hour=hour_to_publish,
        )
    )
    # mode a:release_offset exist,publish_data exist will take date value as a starting date to schedule videos
    # mode b:release_offset not exist, publishdate exist , schedule to this specific date
    # mode c:release_offset not exist, publishdate not exist,daily count to increment schedule from tomorrow
    # mode d: offset exist, publish date not exist, daily count to increment with specific offset schedule from tomorrow

    #  if release_offset and not release_offset == "0-1":
    #             print('mode a sta',release_offset)
    #             if not int(release_offset.split('-')[0]) == 0:
    #                 offset = timedelta(months=int(release_offset.split(
    #                     '-')[0]), days=int(release_offset.split('-')[-1]))
    #             else:
    #                 offset = timedelta(days=1)
    #             if date_to_publish is None:
    #                 date_to_publish =datetime(
    #                     date.today().year,  date.today().month,  date.today().day, 10, 15)
    #             else:
    #                 date_to_publish += offset
video_settings = json.loads('youtube-test-video.json')

checkfilebroken(channel_cookie_path)
checkfilebroken(thumbnail_local_path)
checkfilebroken(videopath)
scheduletopublish_tomorrow()
scheduletopublish_at_specific_date()
scheduletopublish_every7days()
saveasprivatedraft()
instantpublish(video_settings)
# friststart()
