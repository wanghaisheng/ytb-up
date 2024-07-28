"""setup script for installing python dependencies in youtube-auto-upload toolkit"""


import time,os
from tsup.utils.webdriver.DPhelper import DPHelper


def getCookie(
    browserType: str = "chrome",
    proxyserver: str = "",
    channelname: str = "tk-channel",
    url: str = None,
):
    browser=DPHelper(browser_path=None,HEADLESS=False,proxy_server=proxyserver)
    browser.get(url)
    while True:
        # www.tiktok.com/tiktokstudio/upload?lang=en
        if 'tiktokstudio/upload?lang=en' in browser.url:
            browser.saveCookie(outfilepath=channelname+'.txt')
            if os.path.exists(channelname+'.txt'):

                print("just check your cookie file", channelname + ".txt")
                break
            else:
                print(f"failed to save cookie file")
        print('if you input username and password,please go to upload page to finish cookie save process')
        time.sleep(10)
    browser.close()



if __name__ == "__main__":

    sites = [
        "https://www.tiktok.com/login?lang=en"
    ]
# channelname is your account name or something else
# for youtube
getCookie(proxyserver='socks5://127.0.0.1:1080',channelname='fastlane',url=sites[0])
