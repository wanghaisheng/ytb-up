import json
import os
import random
from time import sleep

from datetime import datetime, date
from typing import Optional, Literal, Tuple, List
from tsup.utils.constants import *
from loguru import logger
from tsup.utils.tools import print_dict_diff
from tsup.utils.exceptions import *
from tsup.youtube.youtube_helper_ele import *
from tsup.utils.webdriver import DPhelper
from tsup.youtube.validate_params import VideoSetting


class YoutubeUpload:
    def __init__(self, config) -> None:

        self.timeout = config.get("timeout", 200 * 1000)
        self.username = config.get("username", None)
        self.password = config.get("password", None)
        self.channel_cookie_path = config.get("channel_cookie_path", None)
        self.root_profile_directory = config.get("root_profile_directory", None)
        self.proxy_option = config.get("proxy_option", None)
        self.is_open_browser = config.get("is_open_browser", True)
        self.is_record_video = config.get("is_record_video", False)
        self.is_debug = config.get("is_debug", True)
        self.page = None
        # Configure logger level depending on the debug mode
        if self.is_debug == "debug":
            logger.add(
                "debug.log",
                level="DEBUG",
                rotation="1 MB",
                backtrace=True,
                diagnose=True,
            )
            logger.info("Debug mode is enabled.")
        elif self.is_debug == "info":
            logger.add(
                "debug.log",
                level="INFO",
                rotation="1 MB",
                backtrace=True,
                diagnose=True,
            )
            logger.info("Debug mode is enabled.")
        else:
            logger.add("info.log", level="ERROR", rotation="1 MB")
            logger.info("Running in production mode.")

        logger.debug(
            f"Initialized YoutubeUpload with the following parameters: {self.__dict__}"
        )
        self.logger = logger

    def initialize_driver(self):
        """Initialize the Playwright driver."""
        self.page = DPhelper(
            proxy=self.proxy_option,
            timeout=3000,
        )

    def cookielogin(self):
        """Handles user login to YouTube."""
        if self.channel_cookie_path and os.path.exists(self.channel_cookie_path):
            self.logger.debug(f"Loading cookies from {self.channel_cookie_path}")
            with open(self.channel_cookie_path, "r") as f:
                cookies = json.load(f)["cookies"]
            self.context.clear_cookies()
            self.context.add_cookies(cookies)
            self.logger.debug("Cookies loaded successfully.")
        else:
            self.logger.debug("Cookies not provided. Attempting login.")
            login_success = self.youtube_login(self.username, self.password)
            if login_success:
                self.logger.debug("Login successful, saving cookie.")
                cookie_file = f"{self.username}_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.json"
                self.page.context.storage_state(path=cookie_file)
            else:
                self.logger.warning("Login failed. You may need to login manually.")

    def upload_video(self, video_settings) -> Tuple[bool, Optional[str]]:
        """Main method for uploading a video."""
        # Assuming VideoSetting.default_values and video_settings are already defined as shown in the previous example
        # "video_id": video_settings.get('video_id', VideoSetting.default_values['video_id']),
        video_path = video_settings.get("video_local_path", None)
        if not video_path:
            logger.error("please provide a video locale path")
            return
        if os.path.exists(video_settings.get("video_local_path")) == False:
            logger.error(f"{video_path} is not found on the disk")
            return

        if os.path.getsize(video_settings.get("video_local_path")) == 0:
            logger.error(f"{video_path}  filesize is 0")
            return

        videosettings = VideoSetting(self.logger).validate_upload_options(videosettings)
        if not video_settings == videosettings:
            self.logger.info(
                f"video setting to be upload is changed:{print_dict_diff(video_settings,videosettings)}"
            )
        self.page.goto(YoutubeHomePageURL, timeout=self.timeout)

        # Check login status
        if not check_login_status(self):
            self.cookielogin()

        navigate_to_upload_studiopage(self)
        self.perform_upload(videosettings)

        video_id = get_video_id(self)
        finalize_upload(self)
        return True, video_id

    def perform_upload(
        self, video_local_path: str, video_title: str, video_description: str, **kwargs
    ):
        """Uploads the video and sets metadata."""

        self.logger.debug(f"Uploading video from {video_local_path}")
        set_videofile(self, INPUT_FILE_VIDEO, video_local_path)

        # Set title and description
        set_title(self, video_title)
        set_description(self, video_description)

        # Add additional upload logic here (tags, thumbnail, etc.)
        add_additional_video_info(self, **kwargs)
