# Python Automation Boilerplate

## Description:
This is a boilerplate for testing web & mobile hybrid apps on both iOS & Android.

### Dependencies:
`Node` , `XCode` , `Android Studio`

### Installation Steps
In order to get the tests to run locally, you need to install the following pieces of software:

#### MacOS
1. `homebrew` - install using `ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
2. `pyenv` - install using `brew install pyenv` This is a python version manager
3. `python 2.7.6` - install using `pyenv install 2.7.6`
4. `pyenv global 2.7.6` - Set python version 2.7.6 to be used globally
  
    Add the following to *~/.bash_profile* 
    ```# Pyenv
    export PYENV_ROOT="$HOME/.pyenv"
    export PATH="$PYENV_ROOT/bin:$PATH"
    export PATH="$PYENV_ROOT/shims:$PATH"
    export PATH="$PYENV_ROOT/completions/pyenv.bash:$PATH"
    ```
5. `pytest` - install using `pip install pytest`
6. `pytest_bdd` - install using `pip install pytest-bdd`
7. `pylint` - install using `pip install pylint`
8. `Appium-Python-Client` - install using `pip install Appium-Python-Client`
9. `carthage` - install using `brew install carthage`
10. This setup assumes that node is already installed on your system, if not please download the precompiled package from https://nodejs.org/en/download/ (select `Latest LTS Version`)
11. `appium` - install using `npm install -g appium@1.7.2` (Using v1.7.2 as this is the latest version ADF supports at this moment)
12. SKIPPED. Not working on ADF. requests[security] - install using `pip install requests[security]`    
13. `pip install Faker future gherkin-official python-dateutil pyyaml requests retry`


## Notes
### Tips and Tricks
To benefit from autocomplete please set *tests_root* folder as **Sources Root**
 - Right click on *tests_root_*
 - Click on *Mark Directory As*
 - Click on *Sources Root*

### Installation issues
In case you run in any issues with the above steps below are a set of tips for common problems:

  - chromedriver errors while installing appium use: 
    - `npm install -g appium@1.7.1 --unsafe-perm=true --allow-root`
  - If installation fails and it asks for a _sudo_, you can type following (_sudo_ is not recommended):
    - 1st reinstall _homebrew_
        ```
        brew cleanup
        brew uninstall --force
        ```
    - 2nd reinstall _appium_
        ```
        npm uninstall -g appium
        npm install -g appium-doctor
        npm install -g appium@1.7.1
        appium-doctor //checks your appium installation
        ```
    - 3rd if none of the above work then you can try the following
        ```
        sudo chown -R $USER ~/.npm
        sudo chown -R $USER /usr/lib/node_modules
        sudo chown -R $USER /usr/local/lib/node_modules
        ```  

#### Setup $JAVA_HOME
  - Install latest _Java 8_
  - use your preferred text editor (nano, vim, etc) and edit .bash_profile with the following
  - paste the following two lines:
    ``` 
    export JAVA_HOME=$(/usr/libexec/java_home)
    export PATH=$JAVA_HOME/bin:$PATH
    ```
  - save the change
  - type `source .bash_profile` to make the changes available in the current terminal session
  - To verify in console type, `echo $JAVA_HOME`. It should display `/System/Library/Java/JavaVirtualMachines/1.X.X.jdk/Contents/Home`. Second way to verify is to type `appium-doctor`

#### Setup ANDROID_HOME
  - Install _Android Studio_
  - Open _Android Studio_ and install all dependencies
  - use your preferred text editor (nano, vim, etc) and edit _.bash_profile_ with the following
  - paste the following three lines (change username on first line and Android install location if it is not the default one): 
    ```
    export ANDROID_HOME=/Users/[USERNAME]/Library/Android/sdk
    export PATH=$ANDROID_HOME/platform-tools:$PATH
    export PATH=$ANDROID_HOME/tools:$PATH
    ```
  - save the change
  - type `source .bash_profile` to make the changes available in the current terminal session
  - run `appium-doctor` to verify it looks good


## Modus Create

[Modus Create](https://moduscreate.com) is a digital product consultancy. We use a distributed team of the best talent in the world to offer a full suite of digital product design-build services; ranging from consumer facing apps, to digital migration, to agile development training, and business transformation.

[![Modus Create](https://res.cloudinary.com/modus-labs/image/upload/h_80/v1533109874/modus/logo-long-black.png)](https://moduscreate.com)

This project is part of [Modus Labs](https://labs.moduscreate.com).

[![Modus Labs](https://res.cloudinary.com/modus-labs/image/upload/h_80/v1531492623/labs/logo-black.png)](https://labs.moduscreate.com)

## Licensing

This project is [MIT licensed](./LICENSE).
