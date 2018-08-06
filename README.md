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

### Windows
1. TODOs

### Run all the tests locally
In order to start the tests, you have to start Appium in another terminal window. To do that run ```appium```

The mobile application needs to be built (follow the steps from your project)

_Note_
  - for iOS builds take the _.app_ folder, and zip it, then enter the path to the zipped file in _conf_driver.py_
  - for Android builds, you should have the _.apk_ file available after running the _ionic cordova build android_ command

Then simply go to the _tests_root_ folder and run - `py.test -vv --gherkin-terminal-reporter --not_publish_results True`

Flag ```--not_publish_results True``` will make it sure that test runned locally will not be published to TestRail 

### Run specific tests(feature) file
Difference here is in listing *.feature* file, which will afterwards run only tests of those feature files listed.
- Go to *tests_root/tests/constants.json*
- Edit *suites* with feature file(s) you would like to run. eg:

  - ```
    "project": {
      "id": 1,
      "name": "MC",
      "test_plan": "MC_Sprint_1",
      "env": "Apple iPhone 8Plus_iOS-11.0",
      "suites": {
          "calculator": "Calculator",
          "eula_welcome_screen": "EULA - Welcome Screen"
      },
      "tags":"",
      "language": "en",
      "market": "us"
    }
    
 - After setting this up, you can run: `py.test -vv --gherkin-terminal-reporter --not_publish_results True`. But before that, read all of the below explained.    
 - *suites* can contain a list of Test Suites (.feature files) to be added to the run and results publish

- Info:
    - **suites** = if empty all tests will be executed. 
    - **tags** = further filtering
    - **language** = **mandatory**, taking string from i18n.json for selected language  
    - **market** = **mandatory**, in order to know for which market to trigger tests
### Run on real devices:
#### iOS
- `brew install libimobiledevice`
- `npm install -g ios-deploy`

### Lint code
Linting = the process of analyzing the source code to flag programming errors, bugs, stylistic errors, and suspicious constructs.

**IMPORTANT:** Lint your code before any commit

  - Go to _tests_root_ folder
  - Run `pylint ./tests`
  - There should be only one Error: `E:  4, 0: invalid syntax (<string>, line 4) (syntax-error)`
    - This is due to a _pylint_ issue: root files or folders cannot be ignored from linting. Will follow the fix
    - A rating above 9.00 should be kept for the code

### Package tests for ADF
**Prerequisites for ADF**: `constants.json` filled (See `Publish test results to TestRail` section and see `TestRail-Integration, Dependencies` section)
1. Install Docker Community Edition from https://docker.com
2. Go to _ubuntu_docker_ folder
3. Create Docker from _ubuntu_docker_ folder
    1. `docker build -t ubuntu_01:v0.1 ./` - builds the docker image with name _ubuntu_01_
    2. `docker image ls -a` - lists all docker images
        - this should output 2 images one being _ubuntu_01_
        - to save the image `docker save ubuntu_01 > ubuntu_01.tar`
        - to load a saved image `docker load --input ubuntu_01.tar`
    3. `docker create -v [ABSOLUTE_PATH]/tests_root:/media/tests_root --name ubuntu_01 [DOCKER_IMAGE_ID]` - create docker container based on image
    4. `docker container ls -a` - lists all docker containers
    4. `docker start [DOCKER_CONTAINER_ID]` - starts docker container with id
    5. `docker exec -it [DOCKER_CONTAINER_ID] sh` - opens sh terminal within running docker container
    6. `cd media/tests_root`
    7. `sh package_tests.sh`

### TODOs
  - run pytest with parameters - tags

 
# TestRail-Integration
This is HOW TO guide for TestRail integration of this project 

### Configuration:
Add TestRail API credentials to `./tests_root/tests/constants.json` file

```
"testrail": {
  "user_email": "",
  "user_key": "",
  "url": "https://[SUBDOMAIN].testrail.io",
  "verify_ssl": "true"
}
```

Note: Please follow instructions for generating user_key: http://docs.gurock.com/testrail-api2/accessing

**!DO NOT PUSH your credentials into git repo**
  
### Publish test cases to TestRail
- Go to *tests_root/*
- Run: 

**To import/update test Scenarios for ALL feature files**
- ```py.test -vv --not_publish_results True --publish True --object_path "tests/features"```
 
 **To import/update test Scenarios for INDIVIDUAL .feature file**
- ```py.test -vv --not_publish_results True --publish True --object_path "tests/features/[FILE_NAME].feature"``` 

### Implementation details
- Each *.feature* file is a product functionality
  - Unique key is the pair of **feature name** + **feature description**
  ```gherkin
   Feature: End User License Agreement (EULA)
     As a Quitter
     I open the app for the first time
     I want to be able to view and accept the terms and conditions and privacy policy.
  ```
  - It will create a new **test suite** for each *.feature* file published
  - If **test suite** was imported it will update all the tests within
- Each *Scenario* is a TestRail *case*
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
    - **@LWH-1** = **case ref** to Jira ticket (the feature ticket)
    - **@smoke** / **@sanity** / **@regression** / **None** = **case priority** Critical / High / Medium / Low
    - **@market_us** = **case** is for USA market
    - **@not_market_ca** = **case** is not for Canada market
  - *Steps* are imported as separate ones with empty *Expected Results*
  - Do **NOT** use *And* and *But* keys as it will fail the match of test cases during results publishing
  
### Publish test results to TestRail
####Prerequisites: 
##### 1. Create Test Plan in TestRail
- You have to manually create the test plan in TestRail
  - Naming convention: [JIRA_PROJECT_NAME]_[SPRINT_NAME]_[MARKET]
    - eg: *LWH_Sprint-1_us* or *LWH_Regression_us*
  - Test Plan can be empty
    - Automated tests will create Test Runs for each Test Suite that exists and is in scope of testing: See: *project.suites*
    - Test Run name: [TEST_SUITE_NAME] [ENV]
      - eg: *EULA - Welcome Screen iPhone8_iOS-11.4*
    - If Test Run is present it will only add a new set of results with the current timestamp
  - Test results are published to TestRail at the end of testing
    - The reason of failure is also added to the test step

##### 2. Test run details in `project`
- Go to *tests_root/tests/constants.json*
  - Edit *project* with corresponding data. eg:
  - ```
    "project": {
      "id": 1,
      "name": "LWH",
      "test_plan": "LWH_Sprint_1",
      "env": "Apple iPhone 8Plus_iOS-11.0",
      "suites": {
          "calculator": "Calculator",
          "eula_welcome_screen": "EULA - Welcome Screen"
      },
      "tags":"",
      "language": "en",
      "market": "us"
    }
  - *suites* can contain a list of Test Suites (.feature files) to be added to the run and results publish
  - If *suites* is left empty then all the available suites (.feature files) will be ran and results published for that environment
  
  - Info
    - **id** = **mandatory**, taken from TestRail, is the id of the project. Can be picked up from url in TestRail. Make sure id is correct.
    - **name** = **mandatory**, name of the project you will publish to.
    - **test_plan** = **mandatory**, title of the test plan created manually in TestRail
    - **env** = **mandatory**, device name that will be displayed upon published test run result
    - **suites** = if empty all tests will be executed. 
    - **tags** = further filtering
    - **language** = **mandatory**, taking string from i18n.json for selected language  
    - **market** = **mandatory**, in order to know for which market to trigger tests

##### Run test locally and publish to TestRail
- Go to *tests_root/*
- Run: 
 - ```py.test -vv --gherkin-terminal-reporter``` - this will run and publish tests results
- **NOTE:** To avoid publishing results (for local scope) ```py.test -vv --gherkin-terminal-reporter --not_publish_results True```


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


> Modus Create team members should refer to [ModusCreateOrg GitHub Guidelines](https://docs.google.com/document/d/1eBFta4gP3-eZ4Gcpx0ww9SHAH6GrOoPSLmTFZ7R8foo/edit#heading=h.sjyqpqnsjmjl)

[![Modus Create](./images/modus.logo.svg)](https://moduscreate.com)
