# Overview

Dockerized Python script that will call the Keptn Quality Gate API.  

Script logic:
1. call "start evaluation" API and and save the "keptncontext"
1. while loop with 30 second wait between calls to "evaluate results" API using the "keptncontext"
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
  * Add the ```--debug``` parameter for either scenario to get additonal details.

1. Short result with text value of ```pass```, ```fail```, or ```warning```

    ```
    docker run -it --rm $image \
        --url $keptnApiUrl \
        --token $keptnApiToken \
        --start $start \
        --end $end \
        --project $project \
        --service $service \
        --stage $stage 
    ```

1. Full JSON evaluation details, by adding the ```--evaluationdetails``` argument.

    ```
    docker run -it --rm $image \
        --url $keptnApiUrl \
        --token $keptnApiToken \
        --start $start \
        --end $end \
        --project $project \
        --service $service \
        --stage $stage \
        --evaluationdetails
    ```

# Helper scripts

* ```run.sh``` called the ```docker run``` command. 
* ```buildrun.sh``` builds local docker image and then called the ```run.sh``` scripts
