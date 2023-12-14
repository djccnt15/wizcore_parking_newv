# WizcoreParking_NEWV

code for automated parking discount of Wizcore at NEWV

## Guide

1. get chrome
1. run code with scheduler such as crontab

## System Arguments

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

## How to install Chrome for linux

preparation

- apt update

```
sudo apt-get update
```

- apt update install

```
sudo apt-get install -y curl unzip xvfb libxi6 libgconf-2-4
```

get chrome

- download chrome

```
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
```

- install chrome

```
sudo apt install ./google-chrome-stable_current_amd64.deb
```

- check Chrome version

```
google-chrome --version
```
