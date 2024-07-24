from enum import Enum
from typing import Dict
from datetime import datetime, date
from typing import Optional, Literal


class VideoSetting:
    def __init__(self, logger=None):
        self.logger = logger

    class WaitPolicyOptions(Enum):
        GO_NEXT_COPYRIGHT_CHECK_SUCCESS = "go next after uploading success"
        GO_NEXT_PROCESSING_SUCCESS = "go next after processing success"
        GO_NEXT_COPYRIGHT_CHECK_SUCCESS = "go next after copyright check success"

    class PublishPolicyOptions(Enum):
        PRIVATE = 0
        PUBLISH = 1
        SCHEDULE = 2
        UNLISTED = 3
        PUBLIC_PREMIERE = 4

    class CaptionsCertificationOptions(Enum):
        NONE = 0
        NEVER_AIRED_US = 1
        AIRED_NO_CAPTIONS_US = 2
        NOT_AIRED_CAPTIONS_SINCE_2012 = 3
        NOT_REQUIRE_CAPTIONS = 4
        EXEMPTION_FROM_CAPTIONS = 5

    class LicenseTypeOptions(Enum):
        STANDARD_YOUTUBE_LICENSE = 0
        CREATIVE_COMMONS_ATTRIBUTION = 1

    class ShortsRemixingTypeOptions(Enum):
        ALLOW_VIDEO_AUDIO_REMIXING = 0
        ALLOW_ONLY_AUDIO_REMIXING = 1
        DONT_ALLOW_REMIXING = 2

    class CommentsRatingsPolicyOptions(Enum):
        ALLOW_ALL_COMMENTS = 0
        HOLD_POTENTIALLY_INAPPROPRIATE_COMMENTS = 1
        INCREASE_STRICTNESS = 2
        HOLD_ALL_COMMENTS_FOR_REVIEW = 3
        DISABLE_COMMENTS = 4

    # New options added
    AVAILABLE_SCHEDULE_TIMES = [
        "0:00",
        "0:15",
        "0:30",
        "0:45",
        "1:00",
        "1:15",
        "1:30",
        "1:45",
        "2:00",
        "2:15",
        "2:30",
        "2:45",
        "3:00",
        "3:15",
        "3:30",
        "3:45",
        "4:00",
        "4:15",
        "4:30",
        "4:45",
        "5:00",
        "5:15",
        "5:30",
        "5:45",
        "6:00",
        "6:15",
        "6:30",
        "6:45",
        "7:00",
        "7:15",
        "7:30",
        "7:45",
        "8:00",
        "8:15",
        "8:30",
        "8:45",
        "9:00",
        "9:15",
        "9:30",
        "9:45",
        "10:00",
        "10:15",
        "10:30",
        "10:45",
        "11:00",
        "11:15",
        "11:30",
        "11:45",
        "12:00",
        "12:15",
        "12:30",
        "12:45",
        "13:00",
        "13:15",
        "13:30",
        "13:45",
        "14:00",
        "14:15",
        "14:30",
        "14:45",
        "15:00",
        "15:15",
        "15:30",
        "15:45",
        "16:00",
        "16:15",
        "16:30",
        "16:45",
        "17:00",
        "17:15",
        "17:30",
        "17:45",
        "18:00",
        "18:15",
        "18:30",
        "18:45",
        "19:00",
        "19:15",
        "19:30",
        "19:45",
        "20:00",
        "20:15",
        "20:30",
        "20:45",
        "21:00",
        "21:15",
        "21:30",
        "21:45",
        "22:00",
        "22:15",
        "22:30",
        "22:45",
        "23:00",
        "23:15",
        "23:30",
        "23:45",
    ]

    VIDEO_LANGUAGE_OPTIONS = [
        "Not applicable",
        "Abkhazian",
        "Afar",
        "Afrikaans",
        "Akan",
        "Akkadian",
        "Albanian",
        "American Sign Language",
        "Amharic",
        "Arabic",
        "Aramaic",
        "Armenian",
        "Assamese",
        "Aymara",
        "Azerbaijani",
        "Bambara",
        "Bangla",
        "Bashkir",
        "Basque",
        "Belarusian",
        "Bhojpuri",
        "Bislama",
        "Bodo",
        "Bosnian",
        "Breton",
        "Bulgarian",
        "Burmese",
        "Cantonese",
        "Cantonese (Hong Kong)",
        "Catalan",
        "Cherokee",
        "Chinese",
        "Chinese (China)",
        "Chinese (Hong Kong)",
        "Chinese (Simplified)",
        "Chinese (Singapore)",
        "Chinese (Taiwan)",
        "Chinese (Traditional)",
        "Choctaw",
        "Coptic",
        "Corsican",
        "Cree",
        "Croatian",
        "Czech",
        "Danish",
        "Dogri",
        "Dutch",
        "Dutch (Belgium)",
        "Dutch (Netherlands)",
        "Dzongkha",
        "English",
        "English (Canada)",
        "English (India)",
        "English (Ireland)",
        "English (United Kingdom)",
        "English (United States)",
        "Esperanto",
        "Estonian",
        "Ewe",
        "Faroese",
        "Fijian",
        "Filipino",
        "Finnish",
        "French",
        "French (Belgium)",
        "French (Canada)",
        "French (France)",
        "French (Switzerland)",
        "Fula",
        "Galician",
        "Ganda",
        "Georgian",
        "German",
        "German (Austria)",
        "German (Germany)",
        "German (Switzerland)",
        "Greek",
        "Guarani",
        "Gujarati",
        "Gusii",
        "Haitian Creole",
        "Hakka Chinese",
        "Hakka Chinese (Taiwan)",
        "Haryanvi",
        "Hausa",
        "Hawaiian",
        "Hebrew",
        "Hindi",
        "Hindi (Latin)",
        "Hiri Motu",
        "Hungarian",
        "Icelandic",
        "Igbo",
        "Indonesian",
        "Interlingua",
        "Interlingue",
        "Inuktitut",
        "Inupiaq",
        "Irish",
        "Italian",
        "Japanese",
        "Javanese",
        "Kalaallisut",
        "Kalenjin",
        "Kamba",
        "Kannada",
        "Kashmiri",
        "Kazakh",
        "Khmer",
        "Kikuyu",
        "Kinyarwanda",
        "Klingon",
        "Konkani",
        "Korean",
        "Kurdish",
        "Kyrgyz",
        "Ladino",
        "Lao",
        "Latin",
        "Latvian",
        "Lingala",
        "Lithuanian",
        "Luba-Katanga",
        "Luo",
        "Luxembourgish",
        "Luyia",
        "Macedonian",
        "Maithili",
        "Malagasy",
        "Malay",
        "Malayalam",
        "Maltese",
        "Manipuri",
        "Māori",
        "Marathi",
        "Masai",
        "Meru",
        "Min Nan Chinese",
        "Min Nan Chinese (Taiwan)",
        "Mixe",
        "Mizo",
        "Mongolian",
        "Mongolian (Mongolian)",
        "Nauru",
        "Navajo",
        "Nepali",
        "Nigerian Pidgin",
        "North Ndebele",
        "Northern Sotho",
        "Norwegian",
        "Occitan",
        "Odia",
        "Oromo",
        "Papiamento",
        "Pashto",
        "Persian",
        "Persian (Afghanistan)",
        "Persian (Iran)",
        "Polish",
        "Portuguese",
        "Portuguese (Brazil)",
        "Portuguese (Portugal)",
        "Punjabi",
        "Quechua",
        "Romanian",
        "Romanian (Moldova)",
        "Romansh",
        "Rundi",
        "Russian",
        "Russian (Latin)",
        "Samoan",
        "Sango",
        "Sanskrit",
        "Santali",
        "Sardinian",
        "Scottish Gaelic",
        "Serbian",
        "Serbian (Cyrillic)",
        "Serbian (Latin)",
        "Serbo-Croatian",
        "Sherdukpen",
        "Shona",
        "Sicilian",
        "Sindhi",
        "Sinhala",
        "Slovak",
        "Slovenian",
        "Somali",
        "South Ndebele",
        "Southern Sotho",
        "Spanish",
        "Spanish (Latin America)",
        "Spanish (Mexico)",
        "Spanish (Spain)",
        "Spanish (United States)",
        "Sundanese",
        "Swahili",
        "Swati",
        "Swedish",
        "Tagalog",
        "Tajik",
        "Tamil",
        "Tatar",
        "Telugu",
        "Thai",
        "Tibetan",
        "Tigrinya",
        "Tok Pisin",
        "Toki Pona",
        "Tongan",
        "Tsonga",
        "Tswana",
        "Turkish",
        "Turkmen",
        "Twi",
        "Ukrainian",
        "Urdu",
        "Uyghur",
        "Uzbek",
        "Venda",
        "Vietnamese",
        "Volapük",
        "Võro",
        "Welsh",
        "Western Frisian",
        "Wolaytta",
        "Wolof",
        "Xhosa",
        "Yiddish",
        "Yoruba",
        "Zulu",
    ]

    CATEGORY_OPTIONS = [
        "Autos & Vehicles",
        "Comedy",
        "Education",
        "Entertainment",
        "Film & Animation",
        "Gaming",
        "Howto & Style",
        "Music",
        "News & Politics",
        "Nonprofits & Activism",
        "People & Blogs",
        "Pets & Animals",
        "Science & Technology",
        "Sports",
        "Travel & Events",
    ]
    default_values = {
        "video_title": None,
        "video_description": None,
        "wait_policy": "go next after copyright check success",
        "thumbnail_local_path": None,
        "publish_policy": 0,
        "tags": [],
        "release_date": datetime(
            date.today().year, date.today().month, date.today().day
        ),
        "release_date_hour": "10:15",
        "playlist": None,
        "is_age_restriction": False,
        "is_not_for_kid": False,
        "is_paid_promotion": False,
        "is_automatic_chapters": True,
        "is_featured_place": True,
        "video_language": None,
        "captions_certification": 0,
        "video_film_date": None,
        "video_film_location": None,
        "license_type": 0,
        "is_allow_embedding": True,
        "is_publish_to_subscriptions_feed_notify": True,
        "shorts_remixing_type": 0,
        "categories": None,
        "comments_ratings_policy": 1,
        "is_show_howmany_likes": True,
        "is_monetization_allowed": True,
        "first_comment": None,
        "subtitles": None,
    }

    def validate_upload_options(self, **kwargs: Dict[str, int]) -> Dict[str, int]:
        validated_kwargs = {}

        for key, value in kwargs.items():
            if key == "wait_policy":
                if not isinstance(value, VideoSetting.WaitPolicyOptions):
                    self.logger.error(
                        f"Invalid value '{value}' for 'wait_policy'. Using default."
                    )
                    validated_kwargs[key] = VideoSetting.default_values.get(key)
                else:
                    validated_kwargs[key] = value
            elif key == "publish_policy":
                if not isinstance(value, VideoSetting.PublishPolicyOptions):
                    self.logger.error(
                        f"Invalid value '{value}' for 'publish_policy'. Using default."
                    )
                    validated_kwargs[key] = VideoSetting.default_values.get(key)
                else:
                    validated_kwargs[key] = value
            elif key == "captions_certification":
                if not isinstance(value, VideoSetting.CaptionsCertificationOptions):
                    self.logger.error(
                        f"Invalid value '{value}' for 'captions_certification'. Using default."
                    )
                    validated_kwargs[key] = VideoSetting.default_values.get(key)
                else:
                    validated_kwargs[key] = value
            elif key == "license_type":
                if not isinstance(value, VideoSetting.LicenseTypeOptions):
                    self.logger.error(
                        f"Invalid value '{value}' for 'license_type'. Using default."
                    )
                    validated_kwargs[key] = VideoSetting.default_values.get(key)
                else:
                    validated_kwargs[key] = value
            elif key == "shorts_remixing":
                if not isinstance(value, VideoSetting.ShortsRemixingTypeOptions):
                    self.logger.error(
                        f"Invalid value '{value}' for 'shorts_remixing'. Using default."
                    )
                    validated_kwargs[key] = VideoSetting.default_values.get(key)
                else:
                    validated_kwargs[key] = value
            elif key == "comments_ratings_policy":
                if not isinstance(value, VideoSetting.CommentsRatingsPolicyOptions):
                    self.logger.error(
                        f"Invalid value '{value}' for 'comments_ratings_policy'. Using default."
                    )
                    validated_kwargs[key] = VideoSetting.default_values.get(key)
                else:
                    validated_kwargs[key] = value
            elif key == "available_schedule_time":
                if value not in VideoSetting.AVAILABLE_SCHEDULE_TIMES:
                    self.logger.error(
                        f"Invalid value '{value}' for 'available_schedule_time'. Using default."
                    )
                    validated_kwargs[key] = VideoSetting.default_values.get(key)
                else:
                    validated_kwargs[key] = value
            elif key == "video_language":
                if value not in VideoSetting.VIDEO_LANGUAGE_OPTIONS:
                    self.logger.error(
                        f"Invalid value '{value}' for 'video_language'. Using default."
                    )
                    validated_kwargs[key] = VideoSetting.default_values.get(key)
                else:
                    validated_kwargs[key] = value
            elif key == "categories":
                if (
                    not isinstance(value, str)
                    or value not in VideoSetting.CATEGORY_OPTIONS
                ):
                    self.logger.error(
                        f"Invalid value '{value}' for 'categories'. Using default."
                    )
                    validated_kwargs[key] = VideoSetting.default_values.get(key)
                else:
                    validated_kwargs[key] = value
            elif key == "release_date":
                if not isinstance(value, datetime):
                    self.logger.error(
                        f"Invalid value '{value}' for 'release_date'. Using default."
                    )
                    validated_kwargs[key] = VideoSetting.default_values.get(key)
                else:
                    validated_kwargs[key] = value
            elif key == "release_date_hour":
                if (
                    not isinstance(value, str)
                    or value not in VideoSetting.AVAILABLE_SCHEDULE_TIMES
                ):
                    self.logger.error(
                        f"Invalid value '{value}' for 'release_date_hour'. Using default."
                    )
                    validated_kwargs[key] = VideoSetting.default_values.get(key)
                else:
                    validated_kwargs[key] = value
            else:
                # Check if the key exists in the default_values and if the value matches its type
                if key in VideoSetting.default_values and not isinstance(
                    value, type(VideoSetting.default_values[key])
                ):
                    self.logger.error(
                        f"Invalid type for '{key}'. Expected {type(VideoSetting.default_values[key])}. Using default."
                    )
                    validated_kwargs[key] = VideoSetting.default_values.get(key)
                else:
                    validated_kwargs[key] = value

        return validated_kwargs

    # # Example usage:
    # kwargs = {
    #     'wait_policy': VideoSetting.WaitPolicyOptions.UPLOAD_SUCCESS,
    #     'publish_policy': VideoSetting.PublishPolicyOptions.PUBLISH,
    #     'captions_certification': VideoSetting.CaptionsCertificationOptions.NONE,
    #     'license_type': VideoSetting.LicenseTypeOptions.STANDARD_YOUTUBE_LICENSE,
    #     'shorts_remixing': VideoSetting.ShortsRemixingTypeOptions.ALLOW_VIDEO_AUDIO_REMIXING,
    #     'comments_ratings_policy': VideoSetting.CommentsRatingsPolicyOptions.ALLOW_ALL_COMMENTS,
    #     'available_schedule_time': "12:30",
    #     'video_language': "English",
    #     'category': "Education"
    # }

    # isinputok = validate_upload_options(**kwargs)
    # print(isinputok)  # Output: True
