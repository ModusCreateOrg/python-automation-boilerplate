# Python Automation Boilerplate

## Amazon Device Farm integration
This repository serves as a boilerplate for testing web and hybrid applications using pytest-bdd.
Branch `pytest-bdd_adf_integration` contains the integration between automated tests and Amazon Device Farm, as Test Run environment.

## Package tests for ADF
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
4. The result is a `test_bundle.zip` file that can be manually uploaded to ADF console to run tests or added to a CI server

### Run all the tests on ADF
Use the Device Farm console to upload your tests.
1. Sign in to the Device Farm console at https://console.aws.amazon.com/devicefarm.
2. If you see the AWS Device Farm console home page, choose Get started.
3. If you already have a project, you can upload your tests to an existing project or choose Create a new project.
    - Tip: If the list of projects is not displayed, then on the secondary navigation bar, for Projects, choose the name of the project where you want to upload your tests. To create a project, follow the instructions in Create a Project.
4. If the Create a new run button is displayed, choose it.
5. On the Choose your application page, choose Native Application (the Android and Apple logos).
6. Next, choose Upload to upload your .apk file. Device Farm processes your .apk file before continuing.
7. In the Run name field, type a name for your run.
    - Tip: Give the run a name that will help you identify a specific build of your app (for example, Beta-0.1). For more information, see Working with Test Runs.
8. Choose Appium Python to configure your test,
9. To add your Appium test scripts to the test run, choose Upload.
10. Choose the Appium version you are using from the Appium version dropdown list.
11. Choose Next step, and then complete the instructions to select devices and start the run.
    
#### To run specific tests(feature file):
Difference here is in listing *.feature* file, which will afterwards run only tests of those feature files listed.
- Go to *tests_root/tests/constants.json*
- Edit *suites* with feature file(s) you would like to run. eg:
  - ```
    "project": {
      "suites": {
          "calculator": "Calculator",
          "eula_welcome_screen": "EULA - Welcome Screen"
      },
      "tags":"",
      "language": "en",
      "market": "us"
    }
 - After setting this up, you can run: 
    - `py.test -vv --gherkin-terminal-reporter --not_publish_results True`. But before that, read all of the below explained.    
 - *suites* can contain a list of Test Suites (.feature files) to be added to the run and results publish
- Info:
    - **suites** = if empty all tests will be executed. 
    - **tags** = further filtering
    - **language** = **mandatory**, taking string from i18n.json for selected language  
    - **market** = **mandatory**, in order to know for which market to trigger tests


## Modus Create

[Modus Create](https://moduscreate.com) is a digital product consultancy. We use a distributed team of the best talent in the world to offer a full suite of digital product design-build services; ranging from consumer facing apps, to digital migration, to agile development training, and business transformation.

[![Modus Create](https://res.cloudinary.com/modus-labs/image/upload/h_80/v1533109874/modus/logo-long-black.png)](https://moduscreate.com)

This project is part of [Modus Labs](https://labs.moduscreate.com).

[![Modus Labs](https://res.cloudinary.com/modus-labs/image/upload/h_80/v1531492623/labs/logo-black.png)](https://labs.moduscreate.com)

## Licensing

This project is [MIT licensed](./LICENSE).
