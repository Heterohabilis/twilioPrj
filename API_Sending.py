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
    sentence, sol=getPic(sol) # call the picture getter
    message = Mail(
        from_email=fromEM,
        to_emails=target,
        subject='Your Picture',
        html_content='<strong>'+sentence+'        Your query sol='+str(sol)+'</strong>') # message (success/failure)
    if sentence[0] == "H": # if succeeded
        with open('pic.png', 'rb') as f:
            data = f.read()
        # add the photo to email
        message.attachment = sendgrid.Attachment(
            disposition='inline',
            file_name='pic.png',
            file_type='image/png',
            file_content=base64.b64encode(data).decode(),
            content_id='mars_picture',
        )
    try:
        # send it
        sg = sendgrid.SendGridAPIClient('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')
        # if successfully get the photo, delete it after sending
        if sentence[0] == "H":
            os.remove("pic.png")
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)

def getPic(sol): # picture getter
    try:
        if sol==-1: # if there is no valid query, randomly choose a photo from 0<=sol<=4000
            sol=random.randrange(0,4001)
        api_key='dOBGcn0ysF2HjF9ZySzd8jqbxf1z8FBimiuafx4L'
        url ='https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?api_key='
        link=url+api_key+'&page=1'+'&sol='+str(int(sol))
        response = requests.get(link) # download the json
        query=response.json()
        photoSet=query["photos"] # choose the photo lists
        queryInd=random.randint(0,len(photoSet)-1)
        photo=photoSet[int(queryInd)] # randomly select a photo
        picUrl=photo['img_src']   # get its link
        picSol=photo['sol']
        print(sol)
        urllib.request.urlretrieve(picUrl, 'pic.png') # save the picture
        return ("Here is your pic, catch it!", picSol) # message if succeeded
    except:
        return ("Busy...try again later plz :(", 'err')


        # message if failed


