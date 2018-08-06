# Python Automation Boilerplate

## TestRail integration
This repository serves as a boilerplate for testing web and hybrid applications using pytest-bdd.
Branch `pytest-bdd_testrail_integration` contains the integration between automated tests and TestRail, as Test Management Tool.

Note: TestRail Python wrapper sources from: [testrail-python](https://github.com/travispavek/testrail-python) repository. Updates were added for missing implementations.

### Configuration:
Add TestRail API credentials to `./tests_root/tests/constants.json` file

```
"testrail": {
  "user_email": "",
  "user_key": "",
  "url": "http://moduscreateinc.testrail.io",
  "verify_ssl": "true"
}
```

Note: Please follow instructions from [here](http://docs.gurock.com/testrail-api2/accessing) for generating user_key.

**!DO NOT PUSH your credentials into git repo**
  
### Publish test cases to TestRail
- Go to *tests_root/*
- Run: 
  - ```py.test -vv --not_publish_results True --publish True --object_path "tests/features"```
    - To import/update test Scenarios for ALL feature files
  - ```py.test -vv --not_publish_results True --publish True --object_path "tests/features/[FILE_NAME].feature"``` 
    - To import/update test Scenarios for INDIVIDUAL **.feature* file
  
#### Implementation details
- Each **.feature* file is a product functionality
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
    ```
  - Properties detail:
    - **id** = *mandatory*, taken from TestRail, is the id of the project. Make sure id is correct.
    - **name** = *mandatory*, taken from TestRail, name of the project you will publish to.
    - **test_plan** = *mandatory*, taken from TestRail, title of the test plan created manually
    - **env** = *mandatory*, device name that will be displayed upon published test run result
    - **suites** = can contain a list of Test Suites (.feature files) to be added to the run and results publish. If empty all tests will be executed.
    - **tags** = further filtering of executed tests
    - **language** = *mandatory*, taking application strings from *i18n.json* for selected language 
    - **market** = *mandatory*, in order to know for which market to trigger tests

#### Run test locally and publish to TestRail
- Go to *tests_root/*
- Run: 
    - ```py.test -vv --gherkin-terminal-reporter``` - this will run and publish tests results

**NOTE:** To avoid publishing results (for development scope) run the following:
- ```py.test -vv --gherkin-terminal-reporter --not_publish_results True```


## Modus Create

[Modus Create](https://moduscreate.com) is a digital product consultancy. We use a distributed team of the best talent in the world to offer a full suite of digital product design-build services; ranging from consumer facing apps, to digital migration, to agile development training, and business transformation.

[![Modus Create](https://res.cloudinary.com/modus-labs/image/upload/h_80/v1533109874/modus/logo-long-black.png)](https://moduscreate.com)

This project is part of [Modus Labs](https://labs.moduscreate.com).

[![Modus Labs](https://res.cloudinary.com/modus-labs/image/upload/h_80/v1531492623/labs/logo-black.png)](https://labs.moduscreate.com)

## Licensing

This project is [MIT licensed](./LICENSE).
