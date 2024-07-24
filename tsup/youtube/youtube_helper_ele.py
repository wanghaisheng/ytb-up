import random
from datetime import datetime
from .constants import *
from time import sleep
from pathlib import Path
from datetime import datetime, date
from typing import Optional, Literal, Tuple, List,Dict
from .validate_params import VideoSetting
import os
import json

def send(self, element, text: str) -> None:
    element.clear()
    sleep(self.timeout)
    element.send_keys(text)
    sleep(self.timeout)


def click_next(self) -> None:
    self.page.ele(NEXT_BUTTON).click()
    sleep(random(5 * 1000, self.timeout))


def not_uploaded(self) -> bool:
    s = self.page.ele(STATUS_CONTAINER).text
    return s.find(UPLOADED) != -1


def not_processed(self) -> bool:
    s = self.page.ele(STATUS_CONTAINER).text
    return s.find(PROCESSED) != -1


def not_copyrightchecked(self) -> bool:
    s = self.page.ele(STATUS_CONTAINER).text
    return s.find(CHECKED) != -1


def get_video_id(self) -> Optional[str]:
    """Extracts the video ID from the self.page."""
    try:
        video_url_container = self.page.ele(VIDEO_URL_CONTAINER)
        video_url_element = video_url_container.ele(VIDEO_URL_ELEMENT)
        video_id = video_url_element.get_attribute(HREF)
        return video_id.split("/")[-1]
    except:
        self.logger.error("Could not get video ID")


def set_waitpolicy(self, wait_policy: int):
        if self.wait_policy == "go next after uploading success":
            self.logger.debug("we choose to skip processing and check steps")
            self.logger.debug("start to check whether upload is finished")
            while self.not_uploaded(self.page):
                self.logger.debug("Still uploading...")
                sleep(1)
            self.logger.debug("upload is finished")

        elif self.wait_policy == "go next after processing success":
            self.logger.debug("start to check whether upload is finished")
            while self.not_uploaded():
                self.logger.debug("Still uploading...")
                sleep(1)
            self.logger.debug("uploading is finished")

            self.logger.debug("start to check whether process is finished")
            while self.not_processed():
                self.logger.debug("Still processing...")
                sleep(1)
            self.logger.debug("processing is finished")

        else:
            self.logger.debug("we choose to wait after copyright check steps")
            self.logger.debug("start to check whether upload is finished")
            while self.not_uploaded():
                self.logger.debug("Still uploading...")
                sleep(1)
            self.logger.debug("start to check whether process is finished")
            while self.not_processed():
                self.logger.debug("Still processing...")
                sleep(1)
            self.logger.debug("finished to check whether process is finished")

            self.logger.debug("start to check whether check is finished")
            while self.not_copyrightchecked():
                self.logger.debug("Still checking...")
                sleep(1)
            self.logger.debug("copyright checking is finished")
            self.logger.debug("start to check whether copyright issue exist")
            s = self.page.ele(STATUS_CONTAINER).text
            if not "Checks complete. No issues found" in s:
                self.logger.debug("copyright issue exist")

                # force publish_policy to private if there is any copyright issues
                publish_policy = 0
            else:
                self.logger.debug("There is no copyright issue exist")


def set_publish_policy(self, publish_policy: int):

    if int(publish_policy) == 0:
        self.logger.debug("Trying to set video visibility to private...")

        self.page.ele(PRIVATE_RADIO_LABEL).click()

    elif int(publish_policy) == 1:
        self.logger.debug("Trying to set video visibility to unlisted...")
        self.page.ele("#first-container > tp-yt-paper-radio-group")
        self.page.ele("#first-container > tp-yt-paper-radio-group").click()

        try:
            self.logger.debug("Trying to set video visibility to public...")
            try:
                self.logger.debug("detect getbyrole public button visible:")
                self.page.ele("@radio=Public")

                # self.logger.debug(f'detect public button visible{PUBLIC_BUTTON}:',self.page.ele(PUBLIC_BUTTON))
                # self.logger.debug(f'detect public button visible:{PUBLIC_RADIO_LABEL}',self.page.ele(PUBLIC_RADIO_LABEL))
                self.page.ele("@radio=Public").click()
                self.logger.debug("public radio button clicked")
                # self.page.ele(PUBLIC_BUTTON).click()
            except:
                self.logger.debug("we could not find the public buttton...")

        except Exception as e:
            self.logger.debug(
                f"Trying to set video visibility to public failure due to {e}"
            )
    elif int(publish_policy) == 3:
        self.logger.debug("Trying to set video visibility to Unlisted...")
        self.page.ele("#first-container > tp-yt-paper-radio-group")
        self.page.ele("#first-container > tp-yt-paper-radio-group").click()

        try:
            self.page.ele("@radio=Unlisted").click()
            self.logger.debug("Unlisted radio button clicked")
            # self.page.ele(PUBLIC_BUTTON).click()
            # self.page.ele(PUBLIC_BUTTON).click()
        except:
            self.logger.debug("we could not find the public buttton...")

    elif int(publish_policy) == 4:
        self.logger.debug("Trying to set video visibility to public&premiere...")
        self.page.ele("#first-container > tp-yt-paper-radio-group")
        self.page.ele("#first-container > tp-yt-paper-radio-group").click()

        try:
            self.page.ele("@checkbox=Set as instant Premiere")

            self.page.ele("@checkbox=Set as instant Premiere").click()

        except:
            self.logger.debug(
                "we could not find the Set as instant Premiere checkbox..."
            )

    elif int(publish_policy) == 2:
        if release_date is None:
            release_date = datetime(
                date.today().year, date.today().month, date.today().day
            )
        else:
            release_date = release_date

        if release_date_hour and release_date_hour in V:
            release_date_hour = datestrptime(release_date_hour, "%H:%M")
            release_date_hour = release_date_hour.strftime("%I:%M %p")
        else:
            self.logger.debug(
                f"your specified schedule time is not supported by youtube yet{release_date_hour}"
            )
            release_date_hour = release_date_hour.strftime("%I:%M %p")

        self.logger.debug(
            f"Trying to set video schedule ..{release_date}...{release_date_hour}"
        )

        self.setscheduletime(release_date, release_date_hour)
    else:
        self.logger.debug(f"you should choose a valid publish_policy from {[]}")
    self.logger.debug("publish setting task done")

    if video_id is None:
        self.logger.debug("start to grab video id  in schedule self.page")

        video_id = self.get_video_id(self.page)
        self.logger.debug(f"finish to grab video id in schedule self.page:{video_id}")
    # self.page.click('#save-button')
    # done-button > div:nth-child(2)
    self.logger.debug("trying to click done button")


def set_playlist(self, playlist: int):

    try:
        if playlist:
            self.logger.debug(f'Trying to add video to "{playlist}" playlist...')
            self.page.ele("#basics").ele("text=Playlists")
            self.page.ele("#basics").ele("text=Playlists").click()

            self.page.ele(".ytcp-video-metadata-playlists tp-yt-iron-icon").click()

            playlists_element = self.page.ele("tp-yt-iron-list")
            playlists_element
            if playlist in playlists_element.inner_html():
                self.page.ele(playlist).click()
                self.page.ele("text=Done").click()
            else:
                self.page.keyboard.press("Escape")
                self.logger.debug(f'"{playlist}" playlist not found')
        else:
            self.logger.debug("No playlist provided")
    except:
        self.page.keyboard.press("Escape")
        self.logger.debug("failed to add video to playlist")


def set_is_not_for_kid(self, is_not_for_kid: int):

    self.logger.debug('Trying to set video to "Not made for kids"...')

    try:
        if is_not_for_kid:
            self.page.get_by_role("radio",name="Yes, it's made for kids . Features like personalized ads and notifications won’t be available on videos made for kids. Videos that are set as made for kids by you are more likely to be recommended alongside other kids’ videos. Learn more",
            ).click()

        else:
            self.logger.debug("keep the default setting:No, its not made for kids")
            self.page.ele("@radio=No, it's not made for kids").click()

            # if self.page.ele(NOT_MADE_FOR_KIDS_LABEL):
            #     self.page.ele(NOT_MADE_FOR_KIDS_RADIO_LABEL).click()
            self.logger.debug("not made for kids task done")
    except:
        self.logger.debug("failed to set not made for kids")

    self.logger.debug("Trying to set video AgeRestriction...")


def set_is_age_restriction(self, is_age_restriction: int):

    try:
        if is_age_restriction:
            self.page.get_by_role("radio=Yes, restrict my video to viewers over 18"
            ).click()
        else:
            # keep the default

            self.logger.debug(
                "keep the default setting:No, dont restrict my video to viewers over 18 only"
            )
    except:
        self.logger.debug("failed to set not made for kids")


def set_is_paid_promotion(self, is_paid_promotion: int):
    if is_paid_promotion:
        self.logger.debug("Trying to set video Paid promotion...")

        self.page.ele("text=Paid promotion")
        self.page.ele("text=Paid promotion").click()
        self.page.get_by_role("checkbox",name="My video contains paid promotion like a product placement, sponsorship, or endorsement",
        ).click()
        self.logger.debug("Trying to set video Paid promotion done")


def set_is_automatic_chapters(self, is_automatic_chapters: int):

    if is_automatic_chapters == False:
        self.logger.debug("Trying to set video Automatic chapters...")

        self.page.get_by_role("checkbox=Allow automatic chapters and key moments"
        ).click()

        self.logger.debug("Trying to set video Automatic chapters done")


def set_is_automatic_chapters(self, is_featured_place: int):
    # Featured places
    if is_featured_place == False:
        self.logger.debug("Trying to set video Featured places...")

        self.page.ele("text=Featured places").click()
        self.page.ele("@checkbox=Allow automatic places").click()
        self.logger.debug("Trying to set video Featured places done")


def set_tags(self, tags: int):

    if tags is None or tags == "" or len(tags) == 0:
        pass
    else:
        self.logger.debug(f"tags you give:{tags}")
        if type(tags) == list:
            tags = ",".join(str(tag) for tag in tags)
            tags = tags[:500]
        else:
            tags = tags
        self.logger.debug("overwrite prefined channel tags")
        if len(tags) > TAGS_COUNTER:
            self.logger.debug(
                f"Tags were not set due to exceeding the maximum allowed characters ({len(tags)}/{TAGS_COUNTER})"
            )
            tags = tags[:TAGS_COUNTER]
        self.logger.debug(f'Trying to set "{tags}" as tags...')

        try:
            # self.page.ele(TAGS_CONTAINER).ele(TEXT_INPUT).click()
            self.page.ele("text=Tags").click()
            self.page.get_by_placeholder("Add tag").click()
            # self.page.get_by_placeholder("Add tag").fill("babala,")
            self.page.ele("Tags").click()

            self.logger.debug("clear existing tags")
            self.page.keyboard.press("Backspace")
            self.page.keyboard.press("Control+KeyA")
            self.page.keyboard.press("Delete")
            self.page.ele("Tags").fill(tags)
            self.logger.debug("finishing set   tags")
        except:
            self.logger.debug("failed to set tags")


def set_video_language(self, video_language: int):

    # input language str and get index in the availableLanguages list
    if video_language is not None:
        self.page.ele("text=Language and captions certification").click()
        self.page.ele("#language-input tp-yt-iron-icon").click()


def set_captions_certification(self, captions_certification: int):

    if captions_certification is not None and not captions_certification == 0:
        if self.page.ele(
            "#uncaptioned-reason > ytcp-select:nth-child(1) > ytcp-text-dropdown-trigger:nth-child(1) > ytcp-dropdown-trigger:nth-child(1) > div:nth-child(2)"
        ):
            self.page.ele(
                "#uncaptioned-reason > ytcp-select:nth-child(1) > ytcp-text-dropdown-trigger:nth-child(1) > ytcp-dropdown-trigger:nth-child(1) > div:nth-child(2)"
            ).click()
            self.page.get_by_role("option={captions_certification}"
            ).ele("div").nth(1 + int(captions_certification)).click()


def set_video_film_date(self, video_film_date: int):

    if video_film_date is not None:
        # parse from video metadata  using ffmpeg
        # if none, set to uploading day
        video_film_date = (
            datetime(date.today().year, date.today().month, date.today().day),
        )
        video_film_date = video_film_date.strftime("%b %d, %Y")

        self.page.ele("#recorded-date tp-yt-iron-icon").click()
        self.page.ele("#input-1").ele("@textbox")
        self.page.ele("#input-1").ele("@textbox").fill(video_film_date)


def set_video_film_location(self, video_film_location: int):

    if video_film_location is not None:
        self.page.ele("text=Video location").click()
        self.page.get_by_placeholder("Search").click()
        self.page.get_by_placeholder("Search").dblclick()
        self.page.get_by_placeholder("Search").fill(video_film_location)


def set_license_type(self, license_type: int):

    if license_type == 1:
        self.page.ele("#license tp-yt-iron-icon").click()
        self.page.ele("text=Creative Commons - Attribution").click()


def set_is_allow_embedding(self, is_allow_embedding: int):

    if is_allow_embedding == False:
        self.page.ele("@checkbox=Allow embedding").click()


def set_is_publish_to_subscriptions_feed_notify(
    self, is_publish_to_subscriptions_feed_notify: int
):

    if is_publish_to_subscriptions_feed_notify == False:
        self.page.get_by_role("checkbox=Publish to subscriptions feed and notify subscribers"
        ).click()


def set_shorts_remixing_type(self, shorts_remixing_type: int):

    if shorts_remixing_type is None:
        shorts_remixing_type = 0
    if shorts_remixing_type == 0:
        pass
    elif shorts_remixing_type == 1:
        self.page.ele("@radio=Allow only audio remixing").click()
    elif shorts_remixing_type == 2:
        self.page.ele("@radio=Don’t allow remixing").click()


def set_categories(self, categories: int):

    if categories:
        index = int(categories)
        self.page.ele("text=Category").click()
        self.page.ele("#category tp-yt-iron-icon").click()
        self.page.ele("@option=categories").ele("div").nth(index).click()


def set_comments_ratings_policy(self, comments_ratings_policy: int):

    if comments_ratings_policy == 0:
        self.page.ele("@radio=Allow all comments").click()

    elif comments_ratings_policy == 1:
        pass
    elif comments_ratings_policy == 2:
        self.page.ele("@checkbox=Increase strictness").click()

    elif comments_ratings_policy == 3:
        self.page.ele("@radio=Hold all comments for review").click()
    elif comments_ratings_policy == 4:
        self.page.ele("@radio=Disable comments").click()


def set_is_show_howmany_likes(self, is_show_howmany_likes: int):

    if is_show_howmany_likes == False:
        self.page.ele("@radio=Show how many viewers like this video").click()


def detect_verify_dialog(self, page):
    try:
        self.log.debug(f"Trying to detect verify...")

        # verifyvisible =self.page.ele("text=Verify it's you")
        verifyvisible = page.ele("#confirmation-dialog")
        # verifyvisible1 =page.ele("ytcp-dialog.ytcp-confirmation-dialog > tp-yt-paper-dialog:nth-child(1) > div:nth-child(1)")
        # verifyvisible =page.ele("#dialog-title")
        if verifyvisible:
            # fix google account verify
            self.log.debug("verify its you")
            # page.click('text=Login')
            # sleep(60)
            # page.ele('#confirm-button > div:nth-child(2)').click()
            page.goto(
                "https://accounts.google.com/signin/v2/identifier?service=youtube&uilel=3&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26next%3Dhttps%253A%252F%252Fstudio.youtube.com%252Freauth%26feature%3Dreauth%26authuser%3D3%26pageid%3D106691143538188646876%26skip_identity_prompt%3Dtrue&hl=en&authuser=3&rart=ANgoxcd6AUvx_ynaUmq5M6nROFwTagKglTZqT8c97xb1AEzoDasGeJ14cNlvYfH1_mJsl7us_sFLNGJskNrJyjMaIE2KklrO7Q&flowName=GlifWebSignIn&flowEntry=ServiceLogin"
            )
            page.ele("#identifierId")
            self.log.debug("input username or email")

            # <div class="rFrNMe N3Hzgf jjwyfe QBQrY zKHdkd sdJrJc Tyc9J" jscontroller="pxq3x" jsaction="clickonly:KjsqPd; focus:Jt1EX; blur:fpfTEe; input:Lg5SV" jsshadow="" jsname="Vsb5Ub"><div class="aCsJod oJeWuf"><div class="aXBtI Wic03c"><div class="Xb9hP"><input type="email" class="whsOnd zHQkBf" jsname="YPqjbf" autocomplete="username" spellcheck="false" tabindex="0" aria-label="Email or phone" name="identifier" autocapitalize="none" id="identifierId" dir="ltr" data-initial-dir="ltr" data-initial-value=""><div jsname="YRMmle" class="AxOyFc snByac" aria-hidden="true">Email or phone</div></div><div class="i9lrp mIZh1c"></div><div jsname="XmnwAc" class="OabDMe cXrdqd Y2Zypf"></div></div></div><div class="LXRPh"><div jsname="ty6ygf" class="ovnfwe Is7Fhb"></div><div jsname="B34EJ" class="dEOOab RxsGPe" aria-atomic="true" aria-live="assertive"></div></div></div>

            page.fill('input[name="identifier"]', self.username)

            page.ele(".VfPpkd-LgbsSe-OWXEXe-k8QpJ > span:nth-child(4)").click()
            sleep(10)

            page.fill('input[name="password"]', self.password)
            sleep(10)

            page.ele(".VfPpkd-LgbsSe-OWXEXe-k8QpJ > span:nth-child(4)").click()
            # page.click('text=Submit')

            Stephint = page.ele(
                ".bCAAsb > form:nth-child(1) > span:nth-child(1) > section:nth-child(1) > header:nth-child(1) > div:nth-child(1)"
            ).text
            self.log.debug(Stephint)
            if "2-Step Verification" in Stephint:
                # <div class="L9iFZc" role="presentation" jsname="NjaE2c"><h2 class="kV95Wc TrZEUc"><span jsslot="" jsname="Ud7fr">2-Step Verification</span></h2><div class="yMb59d" jsname="HSrbLb" aria-hidden="true"></div></div>
                # <span jsslot="" jsname="Ud7fr">2-Step Verification</span>
                self.log.debug("you need google auth and sms very code")
                sleep(60)
            # page.ele('#confirm-button > div:nth-child(2)').click()

    except:
        self.log.debug("there is no verification at all")
    self.log.debug(f"Finishing detect verification...")


def set_channel_language_english(self):

    try:
        self.page.goto(YoutubeHomePageURL, timeout=self.timeout)
    except:
        self.logger.debug(
            "failed to youtube studio home page due to network issue,pls check your speed"
        )

    try:
        self.logger.debug("detect your account profile icon .")

        if self.page.ele("Account"):
            self.page.ele("Account").click()

        else:
            if self.page.ele(avatarButtonSelector):
                self.page.ele(avatarButtonSelector).click()

    except Exception:
        self.logger.debug("Avatar/Profile picture button not found : ")
    truelangMenuItemSelector = ""

    try:
        self.logger.debug("detect language setting .")

        if self.page.ele(langMenuItemSelector):
            self.page.ele(langMenuItemSelector).click()
            truelangMenuItemSelector = langMenuItemSelector
        else:
            langMenuItemSelector2 = "yt-multi-page-menu-section-renderer.style-scope:nth-child(3) > div:nth-child(2) > ytd-compact-link-renderer:nth-child(2)"
            if self.page.ele(langMenuItemSelector2):
                self.page.ele(langMenuItemSelector2).click()
                truelangMenuItemSelector = langMenuItemSelector2

    except:
        self.logger.debug('Language menu item selector/button(">") not found : ')

        if not "English" in self.page.ele(truelangMenuItemSelector).text:
            self.logger.debug("choose the language or location you like to use.")
            if self.page.ele(selector_en_path):
                self.page.ele(selector_en_path).click()
        else:
            self.logger.debug(
                "your youtube homepage language setting is already in English"
            )


def check_login_status(self) -> bool:
    """Checks if the user is logged in."""
    return self.confirm_logged_in(self)


def navigate_to_upload_studiopage(self):
    """Navigates to the YouTube upload self.page."""
    self.logger.debug("Navigating to YouTube Studio upload self.page.")
    self.logger.debug("check whether  home page is English")
    self.set_channel_language_english()
    self.logger.debug("go to youtube studio home page")
    try:
        self.page.goto(YOUTUBE_STUDIO_URL, timeout=self.timeout)
    except:
        self.logger.debug(
            "failed to youtube studio home page due to network issue,pls check your speed"
        )

    self.logger.debug("double check youtube studio home page display language")

    if not self.page.ele("@heading=Channel dashboard"):
        # page.ele('.page-title').text=='Channel content':
        self.logger.debug(
            "It seems studio home page is not English,start change locale to english again"
        )
        self.set_channel_language_english()
        self.logger.debug("finish change locale to English")
    else:
        self.logger.debug("your dashborad is in English")

    try:
        self.page.goto(YOUTUBE_UPLOAD_URL, timeout=self.timeout)
    except:
        self.logger.debug(
            f"failed to load youtube studio upload page:{YOUTUBE_UPLOAD_URL} due to network issue,pls check your speed"
        )


def detect_dailylimit(self) -> bool:

    try:
        self.logger.debug(f"Trying to detect daily upload limit...")
        hint = (
            self.page.ele("#error-short style-scope ytcp-uploads-dialog")
            .waitfor()
            .text
        )
        if "Daily upload limit reached" in hint:
            self.logger.debug(f"you have reached daily upload limit pls try tomorrow")

            self.close()

        else:
            pass
    except:
        self.logger.debug(f"Finishing detect daily upload limit...")


def youtube_login(self):
    """Log into YouTube using Gmail credentials."""
    url = "https://accounts.google.com/ServiceLogin?hl=en-US"

    if self.page:
        self.log.info(
            f"Initializing Chrome... {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        try:
            self.page.goto(url)

            for attempt in range(10):
                current_url = self.page.url
                self.log.info(f"Attempt {attempt}: Current URL is {current_url}")

                if "signin/identifier" in current_url:
                    self.handle_signin_identifier()
                    break
                elif "challenge/pwd" in current_url:
                    self.handle_password_challenge(attempt)
                    break
                elif "signin/rejected" in current_url:
                    self.handle_signin_rejected()
                    break
                else:
                    self.log.warning(
                        f"Attempt {attempt}: Unable to find password input box."
                    )
                    self.page.wait_for_timeout(random.uniform(1000, 2000))

            return self.check_login_success()

        except Exception as e:
            self.log.error(f"Encountered an error while logging in: {e}")
            return None
    else:
        self.log.error("Failed to initialize Chrome.")
        return None


def handle_signin_identifier(self):
    """Handle sign-in identifier page."""
    self.log.info("Handling sign-in identifier...")

    try:
        self.page.ele("@combobox")
        language_options = self.page.ele("@combobox").texts()
        if "English" not in "".join(language_options):
            self.page.ele("@combobox").click()
            self.page.ele("@option=English (United States)").click()
            self.log.info("Changed language to English.")

        self.page.ele("#identifierId")
        self.page.ele("#identifierId").fill(self.username)

        self.page.ele("@button=Next").click()
        self.page.wait_for_timeout(random.uniform(3000, 5000))
        self.log.info("Filled email and clicked Next.")

    except Exception as e:
        self.log.error(f"Error in handle_signin_identifier: {e}")


def handle_password_challenge(self, attempt):
    """Handle the password challenge page."""
    self.log.info("Handling password challenge...")

    try:
        password_field = self.page.ele('//input[@type="password"]')
        if password_field:
            password_field.fill(self.password)
            self.log.info(f"Entered password on attempt {attempt}.")

            self.page.ele('//*[@id="passwordNext"]//button').click()
            self.page.wait_for_timeout(random.uniform(2000, 4000))
            self.log.info("Clicked Next after password entry.")
            self.page.goto("https://studio.youtube.com/channel/")
        else:
            self.log.warning(f"Password input not visible on attempt {attempt}.")

    except Exception as e:
        self.log.error(f"Error handling password challenge: {e}")


def handle_signin_rejected(self):
    """Handle a rejected sign-in attempt."""
    self.log.warning("Sign-in rejected, attempting to restart Chrome...")

    self.page.close()
    self.restart_chrome()


def restart_chrome(self):
    """Restart the Chrome browser."""
    for i in range(3):
        port = f"{random.randint(6000, 6999)}"
        self.log.info(f"Attempting to restart Chrome on port {port}...")
        try:
            # Assume initialize_chrome is a function that initializes a browser instance.
            self.initialize_chrome(port)
            break
        except Exception as e:
            self.log.error(f"Error restarting Chrome: {e}")


def check_login_success(self) -> bool:
    """Check if the login was successful."""
    current_url = self.page.url
    if "/studio.youtube.com/" in current_url:
        self.log.info(f"Successfully logged into YouTube! Current URL: {current_url}")
        return True
    else:
        self.log.warning(f"Failed to log into YouTube. Current URL: {current_url}")
        return False


def get_path(self, file_path: str) -> str:
    # no clue why, but this character gets added for me when running
    # return str(os.path(file_path)).replace("\u202a", "")
    # return file_path.replace("\u202a", "")
    return str(Path(file_path)).replace("\u202a", "")


def set_videofile(self, video_local_path: str):
    self.logger.debug(f'Trying to upload "{video_local_path}" to YouTube...')
    if os.path.exists(self.get_path(video_local_path)):
        self.page.ele(INPUT_FILE_VIDEO)
        self.page.set_input_files(INPUT_FILE_VIDEO, self.get_path(video_local_path))
        self.logger.debug(
            f'Trying to upload "{self.get_path(video_local_path)}" to YouTube...'
        )

    else:
        if os.path.exists(video_local_path.encode("utf-8")):
            self.logger.debug(f"file found: {video_local_path}")
            self.page.ele(INPUT_FILE_VIDEO)
            self.page.set_input_files(
                INPUT_FILE_VIDEO, video_local_path.encode("utf-8")
            )
        self.logger.debug(
            f'Trying to upload "{video_local_path.encode("utf-8")}" to YouTube...'
        )


def set_title(self, video_title: str):
    """Sets the video title."""
    self.page.ele(TITLE_CONTAINER).click()
    self.page.keyboard.type(video_title)


def set_description(self, video_description: str):
    """Sets the video description."""
    self.page.ele(DESCRIPTION_CONTAINER).click()
    self.page.keyboard.type(video_description)


def add_additional_video_info(self, **kwargs):
    """Handles additional video information such as tags, thumbnails, etc."""
    # Implement additional settings like thumbnails, tags, etc.
    if "thumbnail_local_path" in kwargs:
        self.set_thumbnail(kwargs["thumbnail_local_path"])

    # Continue with tags, publish policy, etc.


def set_thumbnail(self, thumbnail_local_path: str):
    """Sets the video thumbnail."""
    self.page.ele(INPUT_FILE_THUMBNAIL).set_input_files(thumbnail_local_path)


def finalize_upload(self):
    """Click the done button to finalize the upload."""
    self.page.ele('//*[@id="done-button"]').click()
    self.logger.debug("Upload process is completed.")

def domain_to_url(domain: str) -> str:
    """Converts a (partial) domain to valid URL"""
    if domain.startswith("."):
        domain = "www" + domain
    return "http://" + domain


def format_cookie_file(cookie_file: str):
    """Restore auth cookies from a file. Does not guarantee that the user is logged in afterwards.
    Visits the domains specified in the cookies to set them, the previous page is not restored.
    """
    domain_cookies: Dict[str, List[object]] = {}
    # cookie_file=r'D:\Download\audio-visual\make-reddit-video\auddit\assets\cookies\aww.json'
    with open(cookie_file) as file:
        cookies: List = json.load(file)
        # Sort cookies by domain, because we need to visit to domain to add cookies
        for cookie in cookies:
            if (
                cookie["sameSite"] != "no_restriction"
                or cookie["sameSite"].lower() != "no_restriction"
            ):
                cookie.update(sameSite="None")
            try:
                domain_cookies[cookie["domain"]].append(cookie)
            except KeyError:
                domain_cookies[cookie["domain"]] = [cookie]
    # print(str(domain_cookies).replace(",", ",\n"))

    # cookie.pop("sameSite", None)  # Attribute should be available in Selenium >4
    # cookie.pop("storeId", None)  # Firefox container attribute
    # print("add cookies", domain_cookies[cookie["domain"]])
    # self.context.add_cookies(cookies)
    return domain_cookies[cookie["domain"]]


def confirm_logged_in(self) -> bool:
    """Confirm that the user is logged in. The browser needs to be navigated to a YouTube page."""
    try:
        expect(
            self.page.ele(
                "yt-img-shadow.ytd-topbar-menu-button-renderer > img:nth-child(1)"
            )
        ).to_be_visible()

        # WebDriverWait(page, 10).until(EC.element_to_be_clickable("avatar-btn")))
        return True
    except TimeoutError:
        return False


def confirm_logged_in_douyin(self) -> bool:
    try:
        self.page.ele(".avatar--1lU_a")
        return True
    except:
        return False


def confirm_logged_in_tiktok(self) -> bool:
    """Confirm that the user is logged in. The browser needs to be navigated to a YouTube page."""
    try:
        self.page.ele(
            "yt-img-shadow.ytd-topbar-menu-button-renderer > img:nth-child(1)"
        )

        return True
    except TimeoutError:
        return False



def passwordlogin(self, page):
    page.goto(YoutubeHomePageURL)
    self.log.debug("try to login in from youtube homepage")

    try:
        page.ele("@link=Sign in")
        page.ele("@link=Sign in").click()
        self.log.debug("detected  sign in button")s

    except:
        self.log.debug("could not find sign in button")
    # change sign in language
    if 'hl=en' in page.url:
        self.log.debug(" sign in display language is already english")
        
    else:
        self.log.debug("change sign in display language to english")

        try:
            page.ele("@combobox")
            s = page.ele("@combobox").texts()
            s = "".join(s)
            if not "English" in s:
                page.ele("@combobox").click()
                page.ele("@option=English (United States)").click()
            self.log.debug("changed to english display language")
                
        except:
            self.log.debug("could not find language option ")
        sleep(random.uniform(5, 6))
        try:
            self.log.debug(f"Trying to detect Verify it’s you...")         
            hint = self.page.ele(".tCpFMc > form").texts()
            hint = "".join(hint)
            print(f'hints:{hint}')

            if  'Verify it’s you' in hint:
                self.log.debug(f"To help keep your account secure, Google needs to verify it’s you. Please sign in again to continue to YouTube.")
                self.log.debug(f"for this situation you need a fresh new cookie file")

                self.quit()
            else:
                pass

        except:
            self.log.debug(f"Finishing detect insecure browser...")
    self.log.debug("start to detect  Email or phone textbox")
    try:
        page.ele("@textbox=Email or phone")
        self.log.debug("detected  Email or phone textbox")
        self.log.debug("start to fill in   Email or phone textbox")

        page.ele("@textbox=Email or phone").fill(self.username)

    except:
        self.log.debug(f"could not find email or phone input textbox {page.url}")
        
    self.log.debug("start to detect Next button")
    sleep(random.uniform(5, 6))
    page.ele("@button=Next").click()
    # sleep(random.uniform(5, 6))
    self.log.debug("detected  Next button")

    sleep(random.uniform(5, 6))
    self.log.debug(f"start to detect  password textbox {page.url}")

    try:
        page.ele("@textbox=Enter your password")

        self.log.debug("detected  password textbox")
        self.log.debug("start to fill in password textbox")
        
        page.ele("@textbox=Enter your password").fill(
            self.password
        )
    except:
        self.log.debug(f"could not find password input textbox {page.url}")
    #     page.ele("text=We noticed unusual activity in your Google Account. To keep your account safe, y").click()
        if 'rejected' in page.url:
            self.pl.quit()
                
        # sleep(random.uniform(5, 6))
        # try:
        #     self.log.debug(f"Trying to detect insecure browser...")         
        #     hint = self.page.ele(".tCpFMc > form").texts()
        #     hint = "".join(hint)
        #     print(f'hints:{hint}')

        #     if  'This browser or app may not be secure' in hint:
        #         self.log.debug(f"you have detect insecure browser")

        #         if self.page:
        #             self.page.close()
        #         if self.context:
        #             self.context.close()
        #         if self.browser:
        #             self.browser.close()
        #         if self.driver:
        #             self.driver.stop()

        #     else:
        #         pass

        # except:
        #     self.log.debug(f"Finishing detect insecure browser...")
    self.log.debug("start to detect Next button")
   

    page.ele("@button=Next").click()
    self.log.debug("detected  Next button")
    sleep(random.uniform(5, 6))
 
    try:
        page.ele("#headingText").ele("text=2-Step Verification").click()
        page.ele("text=Google Authenticator").click()
        page.ele("Get a verification code from the Google Authenticator app"
        ).click()
        page.ele("@textbox=Enter code").click()
        sleep(6000)
    except:
        self.log.debug("failed to input code")
    page.ele("@button=Next").click()

    # page.ele("text=选择频道").click()
    # page.ele("@checkbox=不再询问").click()
    # page.ele("ytd-identity-prompt-footer-renderer").click()
    # page.ele("ytd-simple-menu-header-renderer").click()

    current_url = page.url
    if "/studio.youtube.com/" in current_url:
        print(f"studio.youtube.com in current_url: {current_url}")

        print(
            f"youtube 登录成功!!!",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        if not self.CHANNEL_COOKIES:
            self.CHANNEL_COOKIES = self.username
        state = self.context.storage_state(path=self.CHANNEL_COOKIES)
        self.log.debug("we auto save your channel cookies to file:", self.CHANNEL_COOKIES)

        if self.pl.page:
            try:
                self.pl.quit()

            except:
                pass
        return True
    else:
        print(
            f"youtube 登录失败!!!",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        if self.page:
            try:
                self.page.close()
            except:
                pass
        return None