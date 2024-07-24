import random
from datetime import datetime
from DrissionPage import ChromiumOptions, ChromiumPage
from .constants import *
from time import sleep
# use screenshot to detect coordinate
# fake mouse move and click coordinate

def send(self, element, text: str) -> None:
    element.clear()
    sleep(self.timeout)
    element.send_keys(text)
    sleep(self.timeout)

def click_next(self ) -> None:
    self.page.ele(NEXT_BUTTON).click()
    sleep(random(5 * 1000, self.timeout))

def not_uploaded(self) -> bool:
    s = self.page.ele(STATUS_CONTAINER).text_content()
    return s.find(UPLOADED) != -1

def not_processed(self) -> bool:
    s = self.page.ele(STATUS_CONTAINER).text_content()
    return s.find(PROCESSED) != -1

def not_copyrightchecked(self) -> bool:
    s = self.page.ele(STATUS_CONTAINER).text_content()
    return s.find(CHECKED) != -1

def get_video_id(self) -> Optional[str]:
    """Extracts the video ID from the self.page."""
    try:
        video_url_container = self.page.ele(VIDEO_URL_CONTAINER)
        video_url_element = video_url_container.ele(VIDEO_URL_ELEMENT)
        video_id = video_url_element.get_attribute(HREF)
        return video_id.split("/")[-1]
    except:
        raise VideoIDError("Could not get video ID")
def set_waitpolicy(self,wait_policy:int):
    if self.wait_policy in dict(WAIT_POLICY.WAIT_POLICY_TEXT).keys():
        if self.wait_policy == "go next after uploading success":
            self.logger.debug("we choose to skip processing and check steps")
            self.logger.debug("start to check whether upload is finished")
            while  self.not_uploaded(self.page):
                self.logger.debug("Still uploading...")
                sleep(1)
            self.logger.debug("upload is finished")

        elif self.wait_policy == "go next after processing success":
            self.logger.debug("start to check whether upload is finished")
            while  self.not_uploaded():
                self.logger.debug("Still uploading...")
                sleep(1)
            self.logger.debug("uploading is finished")

            self.logger.debug("start to check whether process is finished")
            while  self.not_processed():
                self.logger.debug("Still processing...")
                sleep(1)
            self.logger.debug("processing is finished")

        else:
            self.logger.debug("we choose to wait after copyright check steps")
            self.logger.debug("start to check whether upload is finished")
            while  self.not_uploaded():
                self.logger.debug("Still uploading...")
                sleep(1)
            self.logger.debug("start to check whether process is finished")
            while  self.not_processed():
                self.logger.debug("Still processing...")
                sleep(1)
            self.logger.debug("finished to check whether process is finished")

            self.logger.debug("start to check whether check is finished")
            while  self.not_copyrightchecked():
                self.logger.debug("Still checking...")
                sleep(1)
            self.logger.debug("copyright checking is finished")
            self.logger.debug("start to check whether copyright issue exist")
            s =  self.page.ele(STATUS_CONTAINER).text_content()
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
        self.page.ele(
            "#first-container > tp-yt-paper-radio-group"
        )
        self.page.ele(
            "#first-container > tp-yt-paper-radio-group"
        ).click()

        try:
            self.logger.debug("Trying to set video visibility to public...")
            try:
                self.logger.debug("detect getbyrole public button visible:")
                self.page.get_by_role(
                    "radio=Public"
                )
                

                # self.logger.debug(f'detect public button visible{PUBLIC_BUTTON}:',self.page.ele(PUBLIC_BUTTON))
                # self.logger.debug(f'detect public button visible:{PUBLIC_RADIO_LABEL}',self.page.ele(PUBLIC_RADIO_LABEL))
                self.page.ele("@radio=Public").click()
                self.logger.debug("public radio button clicked")
                # self.page.ele(PUBLIC_BUTTON).click()
            except:
                self.logger.debug("we could not find the public buttton...")

        except Exception as e:
            self.logger.debug(f"Trying to set video visibility to public failure due to {e}")
    elif int(publish_policy) == 3:
        self.logger.debug("Trying to set video visibility to Unlisted...")
        self.page.ele(
            "#first-container > tp-yt-paper-radio-group"
        )
        self.page.ele(
            "#first-container > tp-yt-paper-radio-group"
        ).click()

        try:
            self.page.ele("@radio=Unlisted").click()
            self.logger.debug("Unlisted radio button clicked")
            # self.page.ele(PUBLIC_BUTTON).click()
            # self.page.ele(PUBLIC_BUTTON).click()
        except:
            self.logger.debug("we could not find the public buttton...")


        
    elif int(publish_policy) == 4:
        self.logger.debug("Trying to set video visibility to public&premiere...")
        self.page.ele(
            "#first-container > tp-yt-paper-radio-group"
        )
        self.page.ele(
            "#first-container > tp-yt-paper-radio-group"
        ).click()


        try:
            self.page.get_by_role(
                "checkbox=Set as instant Premiere"
            )

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

        if release_date_hour and release_date_hour in availableScheduleTimes:
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

        self.setscheduletime( release_date, release_date_hour)
    else:
        self.logger.debug(f'you should choose a valid publish_policy from {videos}')
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
                self.page.get_by_text(playlist).click()
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
            self.page.get_by_role(
                "radio",
                name="Yes, it's made for kids . Features like personalized ads and notifications won’t be available on videos made for kids. Videos that are set as made for kids by you are more likely to be recommended alongside other kids’ videos. Learn more",
            ).click()

        else:
            self.logger.debug("keep the default setting:No, its not made for kids")
            self.page.get_by_role(
                "radio=No, it's not made for kids"
            ).click()

            # if self.page.ele(NOT_MADE_FOR_KIDS_LABEL):
            #     self.page.ele(NOT_MADE_FOR_KIDS_RADIO_LABEL).click()
            self.logger.debug("not made for kids task done")
    except:
        self.logger.debug("failed to set not made for kids")

    self.logger.debug("Trying to set video AgeRestriction...")
def set_is_age_restriction(self, is_age_restriction: int):

    try:
        if is_age_restriction:
            self.page.get_by_role(
                "radio=Yes, restrict my video to viewers over 18"
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
        self.page.get_by_role(
            "checkbox",
            name="My video contains paid promotion like a product placement, sponsorship, or endorsement",
        ).click()
        self.logger.debug("Trying to set video Paid promotion done")
def set_is_automatic_chapters(self, is_automatic_chapters: int):

    if is_automatic_chapters == False:
        self.logger.debug("Trying to set video Automatic chapters...")

        self.page.get_by_role(
            "checkbox=Allow automatic chapters and key moments"
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
            self.page.get_by_role(
                "option", name=CaptionsCertificationOptions[captions_certification]
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
        self.page.ele("#input-1").ele("@textbox").fill(
            video_film_date
        )
def set_video_film_location(self, video_film_location: int):

    if video_film_location is not None:
        self.page.ele("text=Video location").click()
        self.page.get_by_placeholder("Search").click()
        self.page.get_by_placeholder("Search").dblclick()
        self.page.get_by_placeholder("Search").fill(
            video_film_location
        )
def set_license_type(self, license_type: int):

    if license_type == 1:
        self.page.ele("#license tp-yt-iron-icon").click()
        self.page.ele("text=Creative Commons - Attribution").click()
def set_is_allow_embedding(self, is_allow_embedding: int):

    if is_allow_embedding == False:
        self.page.ele("@checkbox=Allow embedding").click()
def set_is_publish_to_subscriptions_feed_notify(self, is_publish_to_subscriptions_feed_notify: int):

    if is_publish_to_subscriptions_feed_notify == False:
        self.page.get_by_role(
            "checkbox=Publish to subscriptions feed and notify subscribers"
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
        index=int(categories)
        self.page.ele("text=Category").click()
        self.page.ele("#category tp-yt-iron-icon").click()
        self.page.ele("@option", name=categories).ele("div").nth(
            index
        ).click()
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
        self.page.get_by_role(
            "radio=Show how many viewers like this video"
        ).click()

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

            page.ele(
                ".VfPpkd-LgbsSe-OWXEXe-k8QpJ > span:nth-child(4)"
            ).click()
            sleep(10)

            page.fill('input[name="password"]', self.password)
            sleep(10)

            page.ele(
                ".VfPpkd-LgbsSe-OWXEXe-k8QpJ > span:nth-child(4)"
            ).click()
            # page.click('text=Submit')

            Stephint = page.ele(
                ".bCAAsb > form:nth-child(1) > span:nth-child(1) > section:nth-child(1) > header:nth-child(1) > div:nth-child(1)"
            ).text_content()
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

        if (
            not "English"
            in self.page.ele(truelangMenuItemSelector).text_content()
        ):
            self.logger.debug("choose the language or location you like to use.")
            if self.page.ele(selector_en_path):
                self.page.ele(selector_en_path).click()
        else:
            self.logger.debug("your youtube homepage language setting is already in English")


def check_login_status(self) -> bool:
    """Checks if the user is logged in."""
    return self.confirm_logged_in(self)

def navigate_to_upload_studiopage(self):
    """Navigates to the YouTube upload self.page."""
    self.logger.debug("Navigating to YouTube Studio upload self.page.")
    self.logger.debug("check whether  home page is English")
    self.set_channel_language_english( )
    self.logger.debug("go to youtube studio home page")
    try:
        self.page.goto(YOUTUBE_STUDIO_URL, timeout=self.timeout)
    except:
        self.logger.debug(
            "failed to youtube studio home page due to network issue,pls check your speed"
        )

    self.logger.debug("double check youtube studio home page display language")

    if not self.page.ele("@heading=Channel dashboard"):
        # page.ele('.page-title').text_content()=='Channel content':
        self.logger.debug(
            "It seems studio home page is not English,start change locale to english again"
        )
        self.set_channel_language_english( )
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
            .text_content()
        )
        if "Daily upload limit reached" in hint:
            self.logger.debug(f"you have reached daily upload limit pls try tomorrow")

            self.close()

        else:
            pass
    except:
        self.logger.debug(f"Finishing detect daily upload limit...")

