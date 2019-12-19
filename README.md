# Overview

Dockerized Python script that will call the Keptn Quality Gate API.  

Script logic:
1. call "start evaluation" Keptn API and and save the "keptncontext"
1. while loop with 30 second wait between calls to "evaluate results" Keptn API using the "keptncontext"
1. will return value of ```pass```, ```fail```, or ```warning``` by default
1. To get the full JSON evaluation details, use the ```--evaluationdetails``` argument
1. throws python exception with errors or no result 

# Setup

1. This assumes you are using Keptn 0.6.0beta2 and have a service onboarded.  See example setup and in this [README](https://github.com/grabnerandi/keptn-qualitygate-examples/blob/master/sample/README.md).  You will need the following values as parameters to the quality gate.
    * Project
    * Service
    * Stage
    * Keptn API URL
    * Keptn Token
    * Evalation start time (UTC)
    * Evalation end time (UTC)

1. Use this command to get your Keptn API URL
    ```
    keptn status
    ```

1. Use this command to get your Keptn Token
    ```
    echo "$(kubectl get secret keptn-api-token -n keptn -ojsonpath={.data.keptn-api-token} | base64 --decode)"
    ```

# Usage

Call the ```docker run``` command with the following scenarios.  

NOTES:
  * The start and end parameters is in this format: ```2019-11-21T11:00:00.000Z```
  * Add the ```--debug``` parameter for either scenario to get additonal details
  * This pre-built image can be used if you don't want to make build your own. ```robjahn/keptn-quality-gate```

1. Short result with text value of ```pass```, ```fail```, or ```warning```. Example:

    ```
    image=robjahn/keptn-quality-gate
    keptnApiUrl=https://api.keptn.<YOUR KEPTN DOMAIN>
    keptnApiToken=<YOUR KEPTN TOKEN>
    startTime=2019-11-21T11:00:00.000Z
    endTime=2019-11-21T11:00:10.000Z
    project=keptnorders
    service=frontend
    stage=staging

    docker run -it --rm $image \
        --url $keptnApiUrl \
        --token $keptnApiToken \
        --start $startTime \
        --end $endTime \
        --project $project \
        --service $service \
        --stage $stage 
    ```

1. Full JSON evaluation details, by adding the ```--evaluationdetails``` argument.  Example:

    ```
    image=robjahn/keptn-quality-gate
    keptnApiUrl=https://api.keptn.<YOUR KEPTN DOMAIN>
    keptnApiToken=<YOUR KEPTN TOKEN>
    startTime=2019-11-21T11:00:00.000Z
    endTime=2019-11-21T11:00:10.000Z
    project=keptnorders
    service=frontend
    stage=staging

    docker run -it --rm $image \
        --url $keptnApiUrl \
        --token $keptnApiToken \
        --start $startTime \
        --end $endTime \
        --project $project \
        --service $service \
        --stage $stage \
        --evaluationdetails
    ```

# Helper scripts

* ```run.sh``` calls the ```docker run``` command. 
* ```buildrun.sh``` builds local docker image and then calls the ```run.sh``` scripts
