import requests
import time
import threading
import webbrowser

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

current_version = '1.2.0'

adidas_host = None

marketDomains = {
    'AT': 'adidas.at',
    'AU': 'adidas.com.au',
    'BE': 'adidas.be',
    'BR': 'adidas.com.br',
    'CA': 'adidas.ca',
    'CF': 'adidas.ca',
    'CH': 'adidas.ch',
    'CL': 'adidas.cl',
    'CN': 'adidas.cn',
    'CO': 'adidas.co',
    'CZ': 'adidas.cz',
    'DE': 'adidas.de',
    'DK': 'adidas.dk',
    'EE': 'baltics.adidas.com',
    'ES': 'adidas.es',
    'FI': 'adidas.fi',
    'FR': 'adidas.fr',
    'GB': 'adidas.co.uk',
    'GR': 'adidas.gr',
    'HK': 'adidas.com.hk',
    'HU': 'adidas.hu',
    'IE': 'adidas.ie',
    'ID': 'adidas.co.id',
    'IN': 'adidas.co.in',
    'IT': 'adidas.it',
    'JP': 'japan.adidas.com',
    'KR': 'adidas.co.kr',
    'KW': 'mena.adidas.com',
    'MX': 'adidas.mx',
    'MY': 'adidas.com.my',
    'NG': 'global.adidas.com',
    'NL': 'adidas.nl',
    'NO': 'adidas.no',
    'NZ': 'adidas.co.nz',
    'OM': 'adidas.com.om',
    'PE': 'adidas.pe',
    'PH': 'adidas.com.ph',
    'PL': 'adidas.pl',
    'PT': 'adidas.pt',
    'QA': 'adidas.com.qa',
    'RU': 'adidas.ru',
    'SE': 'adidas.se',
    'SG': 'adidas.com.sg',
    'SK': 'adidas.sk',
    'TH': 'adidas.co.th',
    'TR': 'adidas.com.tr',
    'TW': 'adidas.com.tw',
    'US': 'adidas.com',
    'VE': 'latin-america.adidas.com',
    'VN': 'adidas.com.vn',
    'ZA': 'adidas.co.za'
}


def main():
    print(
        """
              _ _     _              ____   Twitter - https://twitter.com/hunter_bdm
     /\      | (_)   | |            / __ \  Github - https://github.com/hunterbdm
    /  \   __| |_  __| | __ _ ___  | |  | |_   _  ___ _   _  ___ _ __
   / /\ \ / _` | |/ _` |/ _` / __| | |  | | | | |/ _ \ | | |/ _ \ '__|
  / ____ \ (_| | | (_| | (_| \__ \ | |__| | |_| |  __/ |_| |  __/ |
 /_/    \_\__,_|_|\__,_|\__,_|___/  \___\_\\\\__,_|\___|\__,_|\___|_|
        """
    )

    global adidas_host

    check_updates()

    country_code = input('Enter country code: ').upper()

    while not (country_code in marketDomains):
        print("Invalid country code. Example: 'US' 'MX' 'AU' 'CA' ect.")
        country_code = input('Enter country code: ').upper()

    adidas_host = 'http://www.' + marketDomains[country_code]
    print('Adidas url: ', adidas_host)

    try:
        url = input('Splash page url: ')
        proxies_txt = open('proxies.txt')
        proxies = proxies_txt.readlines()
        if len(proxies) == 0:
            print('No proxies found in proxies.txt, starting without proxies.')
            start(url)
        else:
            print(str(len(proxies)) + ' proxies found.')
            start(url, proxies=proxies)
    except:
        print('Unable to read proxies.txt')
        x = input('Start without proxies? (Y/N)').upper()
        while not x == 'Y' and not x == 'N':
            print('Invalid input.')
            x = input('Start without proxies? (Y/N)').upper()
        if x == 'Y':
            print('Starting without proxies.')
            start(url)
        else:
            quit()

    while True:
        time.sleep(5)


def check_updates():
    # Check if the current version is outdated
    try:
        response = requests.get('https://raw.githubusercontent.com/hunterbdm/AdidasQueuer/master/README.md')
    except:
        print('Unable to check for updates.')
        return

    # If for some reason I forget to add the version to readme I dont want it to fuck up
    if 'Latest Version' in response.text:
        # Grab first line in readme. Will look like this 'Latest Version: 1.0.0.0'
        latest = (response.text.split('\n')[0])
        # Will remove 'Latest Version: ' from string so we just have the version number
        latest = latest[(latest.index(':') + 2):]
        if not latest == current_version:
            print('You are not on the latest version.')
            print('Your version:', current_version)
            print('Latest version:', latest)
            x = input('Would you like to download the latest version? (Y/N) ').upper()
            while not x == 'Y' and not x == 'N':
                print('Invalid input.')
                x = input('Would you like to download the latest version? (Y/N) ').upper()
            if x == 'N':
                return
            print('You can find the latest version here https://github.com/hunterbdm/AdidasQueuer/')
            webbrowser.open('https://github.com/hunterbdm/AdidasQueuer/')
            exit()
        print('No updates currently available. Version:', current_version)
        return
    print('Unable to check for updates.')
    return


def start(url, proxies=None):
    """
    :param url: Adidas Queue page url
    :param proxies: Array of proxies
    :return: none
    """

    if proxies:
        for proxy in proxies:
            # \n gets left behind and will fuck up the requests later on
            proxy = proxy.replace('\n', '')
            #proxy_split = proxy.split(':')
            #if len(proxy_split) > 2:
            #    proxy = 'http://' + proxy_split[2] + ':' + proxy_split[3] + '@' + proxy_split[0] + ':' + proxy_split[1]

            t = threading.Thread(target=_start, args=(url, proxy,))
            t.daemon = True
            t.start()
            time.sleep(1)
    else:
        t = threading.Thread(target=_start, args=(url, None,))
        t.daemon = True
        t.start()


def _start(url, proxy):
    """
    :param url: Adidas Queue page url
    :param proxies: Array of proxies, or None if no proxies
    :return: none
    """
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    if proxy is not None:
        proxy_split = proxy.split(':')
        if len(proxy_split) > 2:
            service_args = [
                '--proxy=' + 'http://' + proxy_split[2] + ':' + proxy_split[3] + '@' + proxy_split[0] + ':' + proxy_split[1],
                '--proxy-auth=' + proxy_split[2] + ':' + proxy_split[3]
            ]
        else:
            service_args = [
                '--proxy=' + proxy
            ]
        print('Entering queue with proxy ' + proxy)
        driver = webdriver.PhantomJS(desired_capabilities=dcap, service_args=service_args)
    else:
        print('Entering queue without proxy.')
        driver = webdriver.PhantomJS(desired_capabilities=dcap)

    while True:
        time.sleep(10)
        driver.get(url)
        # If captcha is on page then we got through splash.
        if 'data-sitekey' in driver.page_source:
            if proxy:
                print('Proxy ' + proxy + ' got through queue. Transferring session.')
            else:
                print('Got through queue. Transferring session.')

            fixed_source = driver.page_source
            fixed_source = fixed_source.replace('= "/', ('= "' + adidas_host + '/'))
            fixed_source = fixed_source.replace('="/', ('="' + adidas_host + '/'))

            transfer_session(driver.current_url, driver.get_cookies(), fixed_source, proxy=(None if proxy is None else service_args[0]))
            return


def transfer_session(url, cookies, page_source, proxy=None):
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1280,720')
    if proxy:
        options.add_argument('--proxy-server=' + proxy)

    browser = webdriver.Chrome(chrome_options=options)

    # Must be on adidas to set cookies for adidas, so just go to a 404 page and set cookies first.
    browser.get(adidas_host + '/404settingcookies')
    browser.delete_all_cookies()
    [browser.add_cookie(cookie) for cookie in cookies]
    browser.get(url)

    # None if this currently in use, but it may be needed in the future.
    """
    # Go to splash page url so that the referral will show it
    url = 'http://www.adidas.com/com/apps/dqg2cs/vp_assets/images/350-v2/red2/adidas_YEEZY_350_V2_RB_Lateral_' \
          'Left-red2.jpg?env=&v=16.05'
    browser.get(url)

    # Setup script to change the HTML to that of the passed splash page.
    script = """"""
        function setHTML (html) {
            document.body.insertAdjacentHTML('beforeEnd', html);
            var range = document.createRange();
            range.setStartAfter(document.body.lastChild);
            document.documentElement.innerHTML = '';
            var docFrag = range.createContextualFragment(html);
            document.body.appendChild(docFrag);
        }
        html = `{{ html }}`
        setHTML(html)"""
    """
    script = script.replace("{{ html }}", page_source)

    browser.execute_script(script)

    try:
        while True:
            # If for some reason the html gets reset, set it again.
            if (browser.current_url == url) and not ('data-sitekey' in browser.page_source):
                browser.execute_script(script)
            time.sleep(1)
    except:
        # If we get error here then browser was closed.
        return
    """


if __name__ == '__main__':
    main()