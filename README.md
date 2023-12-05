# WizcoreParking_NEWV
code for automated and scheduled parking discount of Wizcore at NEWV

## windows
### guide
1. get chrome
2. get chromedriver of ur chrome version
3. run code

### sys args

- `--headless`
    - int, default value is 1
    - whether to hide window of browser or not
- `--log_level`
    - int, default value is 20
    - set log level for python
    - you can choice between [0, 10, 20, 30, 40, 50], check the [Python official manual for Logging Level](https://docs.python.org/3/library/logging.html#logging-levels)
- `--info_path`
    - path to JSON file for system usage information, not recommend to input or change

```json
{
    "auth": {
        "id": "asdf",
        "pw": "asdf"
    },
    "url": "http://220.75.173.245/",
    "car_num": "123하1234"
}
```

## linux
### install Chrome
prep apt
apt update

    sudo apt-get update

apt update install

    sudo apt-get install -y curl unzip xvfb libxi6 libgconf-2-4

get chrome
download chrome

    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

install chrome

    sudo apt install ./google-chrome-stable_current_amd64.deb

check Chrome version

    google-chrome --version

### install ChromeDriver
get ChromeDriver file link here(https://sites.google.com/chromium.org/driver/) and change the file link below
the version of ur ChromeDriver must match with ur Chrome version(e.g. Chrome version 90 and ChromeDriver 90)
and ChromeDriver should be a zip file.
in my case, it was like this

    wget https://chromedriver.storage.googleapis.com/90.0.4430.24/chromedriver_linux64.zip

download

    wget {file_link}

unzip

    unzip chromedriver_linux64.zip

move to bin dir

    sudo mv chromedriver /usr/bin/chromedriver

chose owner of chromedriver

    sudo chown root:root /usr/bin/chromedriver

change mode of chromedriver

    sudo chmod +x /usr/bin/chromedriver

check chromedriver version

    chromedriver --version

## Reference
* https://www.selenium.dev/documentation/en/
* https://www.selenium.dev/selenium/docs/api/py/index.html
* https://greeksharifa.github.io/references/2020/10/30/python-selenium-usage/
* https://gracefulprograming.tistory.com/128
* https://www.gregbrisebois.com/posts/chromedriver-in-wsl2/
* https://peter.sh/experiments/chromium-command-line-switches/