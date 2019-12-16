# Overview

Dockerized Python script that will call the Keptn Quality Gate API.

See example API calls in this [README](https://github.com/grabnerandi/keptn-qualitygate-examples/blob/master/sample/README.md)

# Setup

This assumes you are using Keptn 0.6.0beta2 and have a service onboarded.

Use this command for Keptn URL
```
keptn status
```

Use this command for Keptn Token
```
KEPTN_API_TOKEN=$(kubectl get secret keptn-api-token -n keptn -ojsonpath={.data.keptn-api-token} | base64 --decode)
echo $KEPTN_API_TOKEN
```

# Usage example

See the ```build.run``` script to build docker image and run it.

The syntax is as follows:

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

The result will be a text value of ```pass```, ```fail```, or ```warning```

To get the full JSON evaluation details, use the ```--evaluationdetails``` argument.
