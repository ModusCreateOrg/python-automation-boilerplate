# Python Automation Boilerplate

## Description:
This is a boilerplate for testing apps on Web, iOS & Android.

## Dependencies:
`Python` `pip` `pyenv` `virtualenv`

## Installation Steps
In order to get the tests to run locally, you need to install the following pieces of software.<br />
**NOTE: **All commands shall be executed from Automation Project root directory:<br />
```./```.

### MacOS
1. Install Homebrew with `ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
 1.1. Fix commandline `sudo installer -pkg /Library/Developer/CommandLineTools/Packages/macOS_SDK_headers_for_macOS_10.14.pkg -target /`
2. Install Pyenv with `brew install pyenv` This is a python version manager.<br />
   Add the following to *~/.bash_profile* 
   ```
   # pyenv
   export PYENV_ROOT="$HOME/.pyenv"
   export PATH="$PYENV_ROOT/bin:$PATH"
   export PATH="$PYENV_ROOT/shims:$PATH"
   export PATH="$PYENV_ROOT/completions/pyenv.bash:$PATH"
   if command -v pyenv 1>/dev/null 2>&1; then
       eval "$(pyenv init -)"
   fi

   # pyenv-virtualenv
   if which pyenv-virtualenv-init > /dev/null; then
       eval "$(pyenv virtualenv-init -)"
   fi
   ```
3. Install python 3.7.1 with `pyenv install 3.7.1`
5. Install pyenv-virtualenv with `brew install pyenv-virtualenv`
6. Run the following commands: `eval "$(pyenv init -)"` and `eval "$(pyenv virtualenv-init -)"`
8. Set Python virtual env: `pyenv virtualenv 3.7.1 .venv_local`
7. Python virtual env local: `pyenv local .venv_local`
9. Activate virtual env: `pyenv activate .venv_local`
10. Install all project dependencies with `pip install -r requirements.txt`

To delete a venv you can run: `pyenv virtualenv-delete my-virtual-env`

### Windows
1. TODOs

## Test execution

### Execution prerequisites
- Start BrowserStack local (only for BrowserStack execution) ```./BrowserStackLocal --daemon start --key  [ACCESS_KEY]```<br />
  For more info please see: https://www.browserstack.com/local-testing#command-line
- Upload app to BrowserStack:
  curl -u "USERNAME:ACCESS_KEY" -X POST https://api-cloud.browserstack.com/app-automate/upload -F "file=@/path/to/app/file/Application-debug.apk" -F 'data={"custom_id": "MyApp"}'
  curl -u "sergiupopescu1:JnSVjFH4yXDtLfQdEZqz" -X POST https://api-cloud.browserstack.com/app-automate/upload -F "file=@/Users/sergiupopescu/ModusCreate/Python-Automation-Boilerplate/test_root/scripts/Beep.ipa" -F 'data={"custom_id": "MyApp"}'
  curl -u "sergiupopescu1:JnSVjFH4yXDtLfQdEZqz" -X POST https://api-cloud.browserstack.com/app-automate/upload -F "file=@/Users/sergiupopescu/ModusCreate/Python-Automation-Boilerplate/test_root/scripts/Beep.apk" -F 'data={"custom_id": "MyApp"}'
  ipa: bs://5459a0d547c6b81cb4da3b8253a4235d50a981a8
  apk: bs://3795e0d92ebf94fe3ac92a0db04565b891a1e864
  
### Local Terminal run
 - Chrome example:
  ```
  python -m pytest -vv --gherkin-terminal-reporter --driver Chrome --driver-path ./selenium_drivers/chromedriver_mac --capability base_url http://localhost:8100 --tags="" --variables variables.json --variables i18n.json
  ```
 - Appium example:
  ```
  python -m pytest -vv --gherkin-terminal-reporter --driver Appium --appium-capability app ./[APP_NAME].apk --appium-capability platformName Android --appium-capability platformVersion '7.0' --appium-capability deviceName device --capability env Android --capability os_version 7.0 --tags="" --variables variables.json --variables i18n.json
  ```
 - Custom Driver example:
  ```
  python -m pytest -vv --gherkin-terminal-reporter --driver Custom_Driver --driver-impl appium --appium-capability app ./[APP_NAME].apk --appium-capability platformName Android --appium-capability platformVersion '7.0'--appium-capability deviceName device --capability env Android --capability os_version 7.0 --tags="" --variables variables.json --variables i18n.json
  python -m pytest -vv --gherkin-terminal-reporter --driver Appium --appium-capability browserName Chrome --appium-capability base_url https://beep.modus.app --appium-capability platformName Android --appium-capability platformVersion '7.0' --appium-capability deviceName device --tags="" --variables variables.json --variables i18n.json
  ```
  
### Parallel testing
 - Just add the `-n=3 --dist=loadscope` args and remove `--gherkin-terminal-reporter` as this reporting type is not compatible with parallel testing
  NOTE: 
   `n=3` means 3 parallel tests
   `dist=loadscope` means that parallelism is done at *.feature*s file level

### Create PyCharm Run Configurations
1. Edit Configurations > + > Python Tests > pytest
- Chrome
```
Script Path = [UI_TESTS_PATH]
Additional Arguments = -vv --gherkin-terminal-reporter --driver Chrome --driver-path ./selenium_drivers/chromedriver_mac --variables variables.json --variables i18n.json
Python Interpreter = 'Previously created virtualenv'
Working Directory = [UI_TESTS_PATH]
```
- Firefox
```
Script Path = [UI_TESTS_PATH]
Additional Arguments = -vv --gherkin-terminal-reporter --driver Firefox --driver-path ./selenium_drivers/geckodriver_mac --variables variables.json --variables i18n.json
Python Interpreter = 'Previously created virtualenv'
Working Directory = [UI_TESTS_PATH]
```
 - BrowserStack execution arguments based on env (just replace 'Additional Arguments' with correct value:
 ```
 Android App: -vv --gherkin-terminal-reporter --driver BrowserStack --capability device 'Google Pixel 3 XL' --capability os_version '9.0' --capability app 'bs://[app_ID]' --capability browserstack.appium_version '1.10.0' --variables variables.json --variables i18n.json
 Android Web: -vv --gherkin-terminal-reporter --driver BrowserStack --capability device 'Google Pixel 3 XL' --capability os_version '9.0' --capability base_url http://localhost:9002 --variables variables.json --variables i18n.json
 iOS App: -vv --gherkin-terminal-reporter --driver BrowserStack --capability device 'iPhone XS' --capability os_version '12.0' --capability app 'bs://[app_ID]' --capability browserstack.appium_version '1.10.0' --variables variables.json --variables i18n.json
 iOS Web: -vv --gherkin-terminal-reporter --driver BrowserStack --capability device 'iPad Pro 12.9 2018' --capability os_version '12.0' --capability base_url http://bs-local.com:8080 --variables variables.json --variables i18n.json
 IE: -vv --gherkin-terminal-reporter --driver BrowserStack --capability os 'Windows' --capability os_version '10' --capability browser 'IE' --capability browser_version '11' --capability base_url http://localhost:8080 --variables variables.json --variables i18n.json
 Edge: -vv --gherkin-terminal-reporter --driver BrowserStack --capability os 'Windows' --capability os_version '10' --capability browser 'Edge' --capability browser_version '18.0' --capability base_url http://localhost:8080 --variables variables.json --variables i18n.json
 Chrome: -vv --gherkin-terminal-reporter --driver BrowserStack --capability os 'Windows' --capability os_version '10' --capability browser 'Chrome' --capability browser_version '72' --capability base_url http://localhost:8080 --variables variables.json --variables i18n.json
 Safari: -vv --gherkin-terminal-reporter --driver BrowserStack --capability os 'OS X' --capability os_version 'Mojave' --capability browser 'Safari' --capability browser_version '12.0' --capability base_url http://bs-local.com:8080 --variables variables.json --variables i18n.json
 ```
2. Run or Debug with the above configurations
  
## Code Quality
Linting = the process of analyzing the source code to flag programming errors, bugs, stylistic errors, and suspicious constructs.

**IMPORTANT:** Lint your code before any commit

  - Go to _tests_root_ folder
  - Run `pylint ./**/**.py`
  - There should be only one Error: `E:  4, 0: invalid syntax (<string>, line 4) (syntax-error)`
    - This is due to a _pylint_ issue: root files or folders cannot be ignored from linting. Will follow the fix
    - A rating above 9.00 should be kept for the code

## Package tests for AWS CI
TODO


# Browserstack Configuration:
Add TestRail API credentials to `./.browserstack` file

```
[credentials]
username=TODO
key=TODO
```


# TestRail Integration
This is HOW TO guide for TestRail integration of this project 

## Configuration:
Add TestRail API credentials to `./.testrailapi` file

```
[credentials]
email=TODO
key=TODO
url=https://moduscreateinc.testrail.io
verify_ssl=True
```
Note: Please follow instructions for generating user_key: http://docs.gurock.com/testrail-api2/accessing

**!DO NOT PUSH your credentials into git repo**
  
## Export test cases to TestRail
- From project root directory
- Run: 

**To import/update test Scenarios for ALL feature files**
- ```python -m pytest -vv --export_tests_path "features" --variables variables.json --variables i18n.json```
 
**To import/update test Scenarios for INDIVIDUAL .feature file**
- ```python -m pytest -vv --export_tests_path "features/[DIR_NAME]/[FILE_NAME].feature" --variables variables.json --variables i18n.json``` 

## Implementation details
- Each *.feature* file is a product functionality
  - Unique key is the pair of **Feature Name - Functionality** + **feature description**
  ```gherkin
   Feature: Create User - Email registration
     As an anonymous user
     I open the app for the first time
     I want to be able to register with email
  ```
  - It will create a new **Test Suite** for each unique *Feature Name* file published
  - It will create a new **Section** within the **Test Suite** for each unique **Functionality**
  - If **test suite** was previously imported it will update all the tests within
- Each *Scenario* is a TestRail *Case*
  - Unique key is pair of **scenario name** + **data set** (The Examples line in json format)
  ```gherkin
  Scenario: Add two numbers
    Given I have powered calculator on
    When I enter <50> into the calculator
    When I enter <70> into the calculator
    When I press add
    Then The result should be <120> on the screen
    Examples:
      | number_1 | number_2 | result |
      | 10       | 20       | 30     |
      | 50       | 60       | 120    |
  ```
  - It will create a new **case** for each *Scenario* published
  - If **case** was imported it will update it with latest changes
  - Scenario *tags*:
    - **@automation** = **case** is automated
    - **@JIRA-1** = **case ref** to Jira ticket (the feature ticket)
    - **@smoke** / **@sanity** / **@regression** / **None** = **case priority** Critical / High / Medium / Low
    - **@market_us** = **case** is for USA market
    - **@not_market_ca** = **case** is not for Canada market
  - *Steps* are imported as separate ones with empty *Expected Results*
  - Do **NOT** use *And* and *But* keys as it will fail the match of test cases during results publishing
  
## Publish test results to TestRail
###Prerequisites: 
#### 1. Create Test Plan in TestRail
- You have to manually create the test plan in TestRail
  - Naming convention: [JIRA_PROJECT_NAME]_[SPRINT_NAME]_[MARKET] - MARKET only if applied
    - eg: *JIRA_Sprint-1_us* or *JIRA_Regression_us*
  - Test Plan shall contain all Cases that you want to execute within the session
  - The correct configuration shall be present. This is described by *variables.json* in *env*
  - Test results are published to TestRail at the end of testing
    - The reason of failure is also added to the test step

#### 2. Test run details in `project`
- Go to *variables.json*
  - Edit *project* with corresponding data. eg:
  - ```
    "project": {
      "id": 1,
      "name": "JIRA",
      "language": "en",
      "tags":"",
      "test_plan": "JIRA_Sprint_1",
      "market": "us"
    }
  
  - Info
    - **id** = **mandatory**, taken from TestRail, is the id of the project. Can be picked up from url in TestRail. Make sure id is correct.
    - **name** = **mandatory**, name of the project you will publish to.
    - **tags** = **optional**, filtering scenarios by required parameters
    - **test_plan** = **mandatory**, title of the test plan created manually in TestRail
    - **language** = **mandatory**, taking string from i18n.json for selected language  
    - **market** = **optional**, in order to know for which market to trigger tests

### Run tests and publish results to TestRail
- Add the following argument to CLI
   - ```--export_results``` - this will run and publish tests results


# Notes
## Tips and Tricks
To benefit from autocomplete please set *UI* folder as **Sources Root**
 - Right click on *UI_*
 - Click on *Mark Directory As*
 - Click on *Sources Root*

## Installation issues
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

### Setup $JAVA_HOME
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

### Setup ANDROID_HOME
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


# Modus Create

[Modus Create](https://moduscreate.com) is a digital product consultancy. We use a distributed team of the best talent in the world to offer a full suite of digital product design-build services; ranging from consumer facing apps, to digital migration, to agile development training, and business transformation.

[![Modus Create](https://res.cloudinary.com/modus-labs/image/upload/h_80/v1533109874/modus/logo-long-black.png)](https://moduscreate.com)

This project is part of [Modus Labs](https://labs.moduscreate.com).

[![Modus Labs](https://res.cloudinary.com/modus-labs/image/upload/h_80/v1531492623/labs/logo-black.png)](https://labs.moduscreate.com)

## Licensing

This project is [MIT licensed](./LICENSE).
