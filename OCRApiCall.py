import requests
import json
url = 'https://api.ocr.space/parse/image'
headers = {
    'apikey': 'K84270671188957',
}

payload = {
    'language': 'eng',
    'isOverlayRequired': 'false',
    'url': 'https://scontent-ord5-2.cdninstagram.com/v/t51.2885-15/370756379_1025149722260803_1282863242509454581_n.jpg?stp=dst-jpg_e35&_nc_ht=scontent-ord5-2.cdninstagram.com&_nc_cat=107&_nc_ohc=HNZeSQwbZvUAX_JCvIS&edm=ACWDqb8BAAAA&ccb=7-5&ig_cache_key=MzE3OTUyNTUyNzQ2MTY5NjIyNQ%3D%3D.2-ccb7-5&oh=00_AfAqX_6wJE00STZvZvM_sBIF40FhSxmmt6hGSbo_fYIaRQ&oe=651E833B&_nc_sid=ee9879',
    'iscreatesearchablepdf': 'false',
    'issearchablepdfhidetextlayer': 'false',
}

response = requests.post(url, headers=headers, data=payload)
if response.status_code==200:
    data = response.json()
    exitmsg=data["OCRExitCode"]
    errormsg=data["IsErroredOnProcessing"]
    if exitmsg==1 and errormsg==False: 
        # Print the response
        print(data["ParsedResults"][0]["ParsedText"])
    else:
        print("Error occured")
