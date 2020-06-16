url = "https://www.googleapis.com/drive/v3/files/1yaNh_ytiha8N_RyyrAtm5vIrN1IR_LPj/permissions"

payload = "{\"role\": \"reader\", \"type\": \"anyone\"}"
headers = {
  'Authorization': 'Bearer ya29.a0AfH6SMAXcUVDOF5CvlwAnuyHRJKH8YeX7PqnhS9t31bL844MS6dWZvNVw-fgWdhHIonSrCGffOaSwiu2xtLU4S2UEDvNLqk4KHkpJ-rYzFc2SmMh297qXGbMIQ0ytfnwQZfebD53mJw5wSO_Eqm-kqRyUkZSjT3mAEA',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data = payload)

print(response.text.encode('utf8'))
