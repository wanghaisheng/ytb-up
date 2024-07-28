"""setup script for installing python dependencies in youtube-auto-upload toolkit"""


import time,os
from tsup.utils.webdriver.DPhelper import DPHelper


def getCookie(
    browserType: str = "chrome",
    proxyserver: str = "",
    channelname: str = "youtube-channel",
    url: str = "www.youtube.com",
):
    browser=DPHelper(browser_path=None,HEADLESS=False,proxy_server=proxyserver)
    browser.get(url)
    while True:
        if 'studio.youtube.com' in browser.url:
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
    # checkRequirments("firefox")
    # checkRequirments("webkit")
    # checkRequirments("chromium")
    sites = [
        "https://www.youtube.com/upload?persist_gl=1"
    ]
# channelname is your account name or something else
# for youtube
getCookie(proxyserver='socks5://127.0.0.1:1080',channelname='fastlane',url=sites[0])

# for tiktok
# i7SNiSG8V7jND^
# offloaddogsboner@outlook.com
# getCookie(
#     browserType="firefox",
#     proxyserver="socks5://127.0.0.1:1080",
#     channelname="offloaddogsboner",
#     url=sites[3],
# )
# unboxdoctor@outlook.com
# 95Qa*G*za5Gb
# getCookie(
#     browserType="firefox",
#     proxyserver="socks5://127.0.0.1:1080",
#     channelname="",
#     url=sites[0],
# )


# for douyin
# getCookie(browserType='firefox',proxyserver='socks5://127.0.0.1:1080',channelname='',url=sites[2])
