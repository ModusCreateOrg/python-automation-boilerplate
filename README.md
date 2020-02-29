# Selenium & Appium Pytest Web, Mobile and Hybrid App Testing Boilerplate

## Description:
This is a boilerplate for testing mobile hybrid apps on Web, iOS & Android.

## Dependencies:
`Python` `pip` `pyenv` `virtualenv`

## Installation Steps
In order to get the tests to run locally, you need to install the following pieces of software.<br />
**NOTE: **All commands shall be executed from Automation Project root directory:<br />
```../[PROJECT_DIR]/tests/```.

### MacOS
1. Install Homebrew with `ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
 1.1. Fix commandline `sudo installer -pkg /Library/Developer/CommandLineTools/Packages/macOS_SDK_headers_for_macOS_10.14.pkg -target /`
2. Install Pyenv with `brew install pyenv` This is a python version manager.<br />
   Add the following to *~/.bash_profile* 
   ```# Pyenv
   export PYENV_ROOT="$HOME/.pyenv"
   export PATH="$PYENV_ROOT/bin:$PATH"
   export PATH="$PYENV_ROOT/shims:$PATH"
   export PATH="$PYENV_ROOT/completions/pyenv.bash:$PATH"
    ```
3. Install python 3.7.3 with `pyenv install 3.7.3`
4. Set python version 3.7.3 to be used globally with `pyenv global 3.7.3`
5. Install virtualenv with `python3 -m pip install --user virtualenv`
6. Create new virtual env with `python3 -m virtualenv .venv`
7. Activate new virtual env with `source ./.venv/bin/activate`
8. Install all project dependencies with `pip install -r requirements.txt`
9. Check python version used with `which python`. <br />
   Shall be `[PROJECT_DIR]/tests/UI/.venv_boilerplate/bin/python`

### Windows
1. Install GitBash
2. Uninstall any previous python version
3. Install python 3.7.5 using official installation file
4. Install virtualenv with `python -m pip install --user virtualenv`
5. Create new virtual env with `python -m virtualenv .venv`
6. Activate new virtual env with `source ./.venv/Scripts/activate`
7. Install all project dependencies with `pip install -r requirements.txt`
8. Check python version used with `which python`. <br />
   Shall be `[PROJECT_DIR]/tests/UI/.venv_boilerplate/Scripts/python`

## Test execution

### Local Terminal run
 - Chrome example:
  ```
  python -m pytest -vv --gherkin-terminal-reporter --driver Chrome --driver-path ./selenium_drivers/chromedriver_mac --base-url http://localhost:3001 --variables webdriver/capabilities_web.json --variables i18n.json --variables variables.json --tags=""
  ```
 - Appium example:
  ```
  python -m pytest -vv --gherkin-terminal-reporter --driver Appium --appium-capability app ./[APP_NAME].apk --appium-capability platformName Android --appium-capability platformVersion '7.0' --appium-capability deviceName device --capability env Android --capability os_version 7.0 --tags="" --variables variables.json --variables i18n.json
  python -m pytest -vv --gherkin-terminal-reporter --driver Appium --appium-capability browserName Chrome --appium-capability base_url https://beep.modus.app --appium-capability platformName Android --appium-capability platformVersion '7.0' --appium-capability deviceName device --tags="" --variables variables.json --variables i18n.json
 ```
 
### Browserstack run 
Please read BS documentation for more details on configurations:
 - https://www.browserstack.com/automate/python
 - https://www.browserstack.com/app-automate/appium-python
  
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
 Android App: -vv --gherkin-terminal-reporter --driver Appium --host '[BS_USERNAME]:[BS_KEY]@hub-cloud.browserstack.com' --port 80 --variables webdriver/capabilities_android_app.json --variables i18n.json --variables variables.json --tags=""
 Android Web: -vv --gherkin-terminal-reporter --driver Browserstack --capability build '[NAME_OF_BUILD_APP_OR_FEATURE]' --base-url [BASE_URL] --variables webdriver/capabilities_android_web.json --variables i18n.json --variables variables.json --tags=""
 
 iOS App: -vv --gherkin-terminal-reporter --driver Appium --host '[BS_USERNAME]:[BS_KEY]@hub-cloud.browserstack.com' --port 80 --variables webdriver/capabilities_ios_app.json --variables i18n.json --variables variables.json --tags=""
 iOS Web: -vv --gherkin-terminal-reporter --driver BrowserStack --capability device 'iPad Pro 12.9 2018' --capability os_version '12.0' --base-url [BASE_URL] --variables variables.json --variables i18n.json
 
IE: -vv --gherkin-terminal-reporter --driver BrowserStack --capability browser 'IE' --capability browser_version '11' --base-url http://localhost:3001 --variables webdriver/capabilities_web.json --variables i18n.json --variables variables.json --tags=""
 Edge: -vv --gherkin-terminal-reporter --driver BrowserStack --capability browser 'Edge' --capability browser_version '18.0' --base-url http://localhost:3001 --variables webdriver/capabilities_web.json --variables i18n.json --variables variables.json --tags=""
 Chrome: -vv --gherkin-terminal-reporter --driver Browserstack --capability build '[NAME_OF_BUILD_APP_OR_FEATURE]' --base-url [BASE_URL] --variables webdriver/capabilities_web.json --variables webdriver/capabilities_web.json --variables i18n.json --variables variables.json --tags=""
 Safari: -vv --gherkin-terminal-reporter --driver BrowserStack --capability browser 'Safari' --capability browser_version '12.0' --base-url [BASE_URL] --variables webdriver/capabilities_web.json --variables i18n.json --variables variables.json --tags=""
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
Add BrowserStack API credentials to `./.browserstack` file

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
