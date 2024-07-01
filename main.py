import json
import time
import requests

token = ''
with open('token', 'r', encoding='utf-8') as f:
    token = f.read()

url = 'https://www.duolingo.com/2017-06-30/sessions'

def sendPost():

    headers = {"Content-Type": "application/json",
               "authorization": "",
               "accept": "*/*",
               "user-agent": "insomnia/2023.1.0",
               "cookie": "wuuid=4a80506c-a1a3-4edb-8953-f877379c9fac; wuuid=6b5c4128-cbb4-45ce-8b29-9f97b871fbdb"
               }

    data = {"challengeTypes": ["assist", "characterIntro", "characterMatch", "characterPuzzle", "characterSelect", "characterTrace", "completeReverseTranslation", "definition", "dialogue", "form", "freeResponse", "gapFill", "judge", "listen", "listenComplete", "listenMatch", "match", "name", "listenComprehension", "listenIsolation", "listenTap", "partialListen", "partialReverseTranslate", "readComprehension", "select", "selectPronunciation", "selectTranscription", "syllableTap", "syllableListenTap", "tapCloze", "tapClozeTable", "tapComplete", "tapCompleteTable", "tapDescribe", "translate",
                               "typeCloze", "typeClozeTable", "typeCompleteTable"], "fromLanguage": "en", "isFinalLevel": "true", "isV2": "true", "juicy": "true", "learningLanguage": "de", "smartTipsVersion": 2, "levelSessionIndex": 0, "skillIds": ["bf2403268325de8457fc601643a1ea80"], "type": "LEGENDARY"}

    json_data = json.dumps(data)
    headers['authorization'] = token
    response = requests.post(url, headers=headers, data=json.dumps(data, ensure_ascii=False).encode('utf8'))

    return response


def sendPut(response, seriesIndex=1):
    extenderString = {"heartsLeft": 3,
                      "startTime": 1716384284,
                      "enableBonusPoints": 'false',
                      "endTime": 1716384384,
                      "failed": 'false',
                      "maxInLessonStreak": 10,
                      "shouldLearnThings": 'true',
                      "xpPromised": 200,
                      "pathLevelSpecifics": {
                          "unitIndex": 1
                      }

                      }

    content = str(response.content, encoding='utf8')
    id = content[7:23]
    prefixPart = content[0:content.find('sessionExperimentRecord')]
    suffixPart = str(extenderString)[1:].replace('\'','\"')
    # print(suffixPart)
    preTimeJson = prefixPart[0:-1] + '' + suffixPart + ''
    timeEnd = int(time.time() - 1000*(seriesIndex-1))
    timeStart = timeEnd - 1000*seriesIndex
    preJson1 = preTimeJson.replace(preTimeJson[preTimeJson.find("startTime"):preTimeJson.find("startTime")+22], 'startTime": ' + str(timeStart))
    preJson2 = preJson1.replace(preJson1[preJson1.find("endTime"):preJson1.find("endTime")+20], 'endTime": ' + str(timeEnd)).replace('\"false\"', 'false').replace('\"true\"', 'true')

    json_data = json.dumps(preJson2)

    putUrl = url + '/' + id

    headers = {"Content-Type": "application/json",
               "authorization": "",
               "idempotency-key": "CxZYRs4GJ8B2SXC6",
               "accept": "*/*",
               "user-agent": "insomnia/2023.1.0"
               }


    # print(preJson2)
    #
    # print(headers)
    # print(putUrl)
    headers['authorization'] = token
    print(headers)
    with open('file.json', 'w', encoding='utf-8') as f:
        f.write(preJson2)
    response = requests.put(putUrl, headers=headers, data=open('file.json', 'rb'))

    print(response)
    print(response.status_code)
    print(response.content)

    return

series = 2
for i in range(series):
    sendPut(sendPost(),i)
