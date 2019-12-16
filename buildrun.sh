#!/bin/bash

image=$1           # e.g. robjahn/keptn-quality-gate
keptnApiUrl=$2     # e.g. https://api.keptn.<YOUR VALUE>.xip.io
keptnApiToken=$3
start=$4           # e.g. 2019-11-21T11:00:00.000Z
end=$5             # e.g. 2019-11-21T11:00:10.000Z
project=$6         # e.g. keptnorders
service=$7         # e.g. frontend
stage=$8           # e.g. staging

echo "==============================================="
echo "build"
echo "==============================================="
docker build -t $image .

clear
echo ""
echo "==============================================="
echo "run"
echo "==============================================="

docker run -it --rm $image \
    --url $keptnApiUrl \
    --token $keptnApiToken \
    --start $start \
    --end $end \
    --project $project \
    --service $service \
    --stage $stage #--evaluationdetails #--debug

exit