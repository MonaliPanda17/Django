# from django.shortcuts import render

# Create your views here.
from django.http import HttpRequest, HttpResponse
import google_auth_oauthlib.flow
import requests


REDIRECT_URI = "https://5afd-103-92-103-134.in.ngrok.io/rest/v1/calendar/redirect"


#get access to gmail account verification
def GoogleCalendarInitView(request):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('google_creds.json', scopes=['https://www.googleapis.com/auth/calendar'])
    flow.redirect_uri = REDIRECT_URI
    authorization_url, state = flow.authorization_url(access_type='offline') #, include_granted_scopes='true')
    print(f'This is : ',authorization_url)
    return HttpResponse(authorization_url)

# Exchange authorization code for refresh and access tokens
def GoogleCalendarRedirectView(request: HttpRequest):
    state = request.GET.get('state')
    code =  request.GET.get('code')
    if state is None or code is None:
        raise ValueError("missing parameters: code/state")

    authorization_response = f"{REDIRECT_URI}?code={code}&state={state}"
    print("========", state, code, authorization_response, "====================")
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('google_creds.json',
        scopes=['https://www.googleapis.com/auth/calendar'],
        state=state)
    flow.redirect_uri = REDIRECT_URI
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    print(f"Credential data :",credentials.to_json())
    token = credentials.token 
    print(f'Access token is generated : ',token)
    headers = {
        'Content-Type': 'application/json',
        'Authorization':f'Bearer {token}'
    }
    data = requests.get("https://www.googleapis.com/calendar/v3/users/me/calendarList",headers=headers)
    print("Calendar data is printed")
    return HttpResponse(data)

