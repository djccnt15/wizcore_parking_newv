### install chrome
prep

    $ sudo apt-get update
    $ sudo apt-get install -y curl unzip xvfb libxi6 libgconf-2-4
    
chrome itself

    $ wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    $ sudo apt install ./google-chrome-stable_current_amd64.deb
    
check chrome version

    $ google-chrome --version

### install chromedriver
get chromedriver file link here(https://sites.google.com/chromium.org/driver/) and change the file link below
the version of ur ChromeDriver must match with ur Chrome version(e.g. Chrome version 90 and ChromeDriver 90)

    $ wget *file_link
    $ unzip chromedriver_linux64.zip
    $ sudo mv chromedriver /usr/bin/chromedriver
    $ sudo chown root:root /usr/bin/chromedriver
    $ sudo chmod +x /usr/bin/chromedriver
    
check chromedriver version

    $ chromedriver --version
