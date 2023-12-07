# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
import random
import urllib.request
import base64
import requests
import sendgrid
from sendgrid.helpers.mail import Mail



def mailSender(fromEM, target,sol):
    sentence=getPic(sol)
    message = Mail(
        from_email=fromEM,
        to_emails=target,
        subject='Your Picture',
        html_content='<strong>'+sentence+'</strong>')
    if sentence[0] == "H":
        with open('pic.png', 'rb') as f:
            data = f.read()
        message.attachment = sendgrid.Attachment(
            disposition='inline',
            file_name='pic.png',
            file_type='image/png',
            file_content=base64.b64encode(data).decode(),
            content_id='mars_picture',
        )
    try:
        sg = sendgrid.SendGridAPIClient('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')
        if sentence[0] == "H":
            os.remove("pic.png")
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)

def getPic(sol):
    try:
        if sol==-1:
            sol=random.randrange(0,4001)
        api_key='dOBGcn0ysF2HjF9ZySzd8jqbxf1z8FBimiuafx4L'
        url ='https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?api_key='
        link=url+api_key+'&page=1'+'&sol='+str(int(sol))
        response = requests.get(link)
        query=response.json()
        photoSet=query["photos"]
        queryInd=random.randint(0,len(photoSet)-1)
        photo=photoSet[int(queryInd)]
        picUrl=photo['img_src']
        print(picUrl)
        urllib.request.urlretrieve(picUrl, 'pic.png')
        return "Here is your pic, catch it!"
    except:
        return "Busy...try again later plz :("

