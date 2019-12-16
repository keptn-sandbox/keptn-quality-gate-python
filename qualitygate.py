import argparse
import json
import requests
import time

DEBUG_OUTPUT = False

def debugMessage(message):
    if DEBUG_OUTPUT:
        print(message)

# ensures the right API endpoint is called
def getApiEndPoint(url):
    if url.endswith('/v1/event'):
        return url
    elif url.endswith('/v1/event/'):
        return url[:-1]
    elif url.endswith('/'):
        return url + "v1/event"
    else:
        return url + "/v1/event"

# Returns the API Header
def getHeader(token):
    return {"x-token": token, "accept": "application/json", "Content-Type": "application/json"}

# see the the quality gate is complete for the passed in Keptn context
def getEvaluation(url, token, keptnContext):

    debugMessage("DEBUG - getEvaluation() " + url + " - keptnContext: " + str(keptnContext))    
    apiResponse = requests.get(url, headers=getHeader(token), params={"keptnContext": keptnContext, "type": "sh.keptn.events.evaluation-done"}, verify=False)
    debugMessage("DEBUG - getEvaluation() http status code: " + str(apiResponse.status_code) + " " + apiResponse.text)
    
    # For successful API call, response code will be 200 (OK)
    if (apiResponse.status_code != 200):     
        if apiResponse.status_code == 500:
            if "No Keptn" in apiResponse.text:
                debugMessage("DEBUG - startEvaluation() Results not ready yet")
                return None
        else:
            raise Exception("Error", "getEvaluation() API Failed. " + str(apiResponse.status_code) + " " + apiResponse.text)

    return apiResponse

# start the quality gate processing for the passed in body
# returns the keptn context string or None if there was an error
def startEvaluation(url, token, start, end, project, service, stage):

    keptnDataBody = ' { "start": "' + start + '", \
        "end":"' + end + '", \
        "project":"' + project + '", \
        "service":"' + service + '", \
        "stage":"' + stage + '", \
        "teststrategy":"manual"}'

    keptnEvaluationBody = '{ "data": ' + keptnDataBody + ',"type": "sh.keptn.event.start-evaluation" }'
    debugMessage("DEBUG - startEvaluation() " + url + " - keptnEvaluationBody: " + str(keptnEvaluationBody))

    apiResponse = requests.post(url, headers=getHeader(token), data=keptnEvaluationBody, verify=False)
    debugMessage("DEBUG - startEvaluation() http status code: " + str(apiResponse.status_code) + " " + apiResponse.text)

    # For successful API call, response code will be 200 (OK)
    if (apiResponse.status_code == 200):
        if (len(apiResponse.text) > 0):
            jsonContent = apiResponse.json()
            return jsonContent['keptnContext']
        else:
            raise Exception("Error", "startEvaluation() API Failed. " + str(apiResponse.status_code) + " " + apiResponse.text)
    else:
        raise Exception("Error", "startEvaluation() API Failed. " + str(apiResponse.status_code) + " " + apiResponse.text)

    return jsonContent

# main processing logic that will start the evaluation and loop to test if it is complete
def process(keptnApiUrl, keptnApiToken, start, end, project, service, stage, evaluationdetails):

    keptnContext = startEvaluation(keptnApiUrl, keptnApiToken, start, end, project, service, stage)
    if keptnContext:
        numRetries=6
        waitSeconds=30
        retryCount=0
        # loop until get a result or run out of attempts
        apiResponse = None
        while (retryCount < numRetries):
            debugMessage("getEvaluation() attempt number: " + str(retryCount+1) + " of " + str(numRetries))
            apiResponse = getEvaluation(keptnApiUrl, keptnApiToken, keptnContext)
            if apiResponse:
                break
            debugMessage("DEBUG - getEvaluation() waiting " + str(waitSeconds) + " seconds before re-trying")
            time.sleep(waitSeconds)
            retryCount += 1

        if not apiResponse:
            raise Exception("Error", "getEvaluation() API Failed to get result")
            return
    else:
        raise Exception("Error", "getEvaluation() API Failed. "+ str(apiResponse.status_code) + " " + apiResponse.text)
        return

    # For successful API call, response code will be 200 (OK)
    if (apiResponse.status_code == 200):
        if (len(apiResponse.text) > 0):
            jsonContent = apiResponse.json()
            debugMessage("DEBUG - getEvaluation() result: " + jsonContent['data']['evaluationdetails']['result'])
            debugMessage("DEBUG - getEvaluation() score: " + str(jsonContent['data']['evaluationdetails']['score']))
            debugMessage("DEBUG - getEvaluation() data: " + json.dumps(jsonContent['data']))
            if evaluationdetails:
                print(json.dumps(jsonContent['data']['evaluationdetails']))
            else:
                print(jsonContent['data']['evaluationdetails']['result'])
        else:
            raise Exception("Error", "getEvaluation() API Failed to get evaluationdetails. " + str(apiResponse.status_code) + " " + apiResponse.text)

    else:
        raise Exception("Error", "getEvaluation() API Failed to get result. " + str(apiResponse.status_code) + " " + apiResponse.text)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True, help="Keptn API URL")
    ap.add_argument("--token", required=True, help="Keptn API token")
    ap.add_argument("--start", required=True, help="Evaluation Start Time")
    ap.add_argument("--end", required=True, help="Evaluation End Time")
    ap.add_argument("--project", required=True, help="Keptn project")
    ap.add_argument("--service", required=True, help="Keptn service")
    ap.add_argument("--stage", required=True, help="Keptn stage")
    ap.add_argument("--evaluationdetails", help="Use this option to get all JSON evaluation data", action='store_true')
    ap.add_argument('--debug', help='debugMessage more data', action='store_true')
    args = vars(ap.parse_args())

    # this will supress the insecure SSL warnings in the output
    requests.packages.urllib3.disable_warnings()

    keptnApiUrl = getApiEndPoint(args["url"])
    keptnApiToken = args["token"]
    start = args["start"]
    end = args["end"]
    project = args["project"]
    service = args["service"]
    stage = args["stage"]
    evaluationdetails = args["evaluationdetails"]

    if args["debug"]:
        DEBUG_OUTPUT = True

    debugMessage("DEBUG - main() =====================================================")
    debugMessage("DEBUG - main() keptnApiUrl: " + keptnApiUrl)
    debugMessage("DEBUG - main() keptnApiToken: "+ keptnApiToken)
    debugMessage("DEBUG - main() start: "+ start)
    debugMessage("DEBUG - main() end: "+ end)
    debugMessage("DEBUG - main() project: "+ project)
    debugMessage("DEBUG - main() service: "+ service)
    debugMessage("DEBUG - main() stage: "+ stage)
    debugMessage("DEBUG - main() =====================================================")

    # process the quality gate
    process(keptnApiUrl, keptnApiToken, start, end, project, service, stage, evaluationdetails)