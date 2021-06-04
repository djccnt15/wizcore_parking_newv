### install Chrome
prep

    $ sudo apt-get update
    $ sudo apt-get install -y curl unzip xvfb libxi6 libgconf-2-4
    
Chrome itself

    $ wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    $ sudo apt install ./google-chrome-stable_current_amd64.deb
    
check Chrome version

    $ google-chrome --version

### install ChromeDriver
get ChromeDriver file link here(https://sites.google.com/chromium.org/driver/) and change the file link below    
the version of ur ChromeDriver must match with ur Chrome version(e.g. Chrome version 90 and ChromeDriver 90)    
and ChromeDriver should be a zip file.    
in my case, it was like this

    $ wget https://chromedriver.storage.googleapis.com/90.0.4430.24/chromedriver_linux64.zip

download, unzip, and put it in ur bin dir

    $ wget {file_link}
    $ unzip chromedriver_linux64.zip
    $ sudo mv chromedriver /usr/bin/chromedriver
    $ sudo chown root:root /usr/bin/chromedriver
    $ sudo chmod +x /usr/bin/chromedriver
    
check chromedriver version

    $ chromedriver --version
