import datetime
import logging
import urllib.parse

import requests, uuid
from datetime import timezone
from .models import CoreTokens
from django.db import transaction


client_id = "eA172bI8p3IQFDxLrZuv6oTbHIe2MSat.apps.bqe.com"  # TODO: store in constants manager or config file
scope = "readwrite:core offline_access"
redirect_uri = "https://andrewmckernan.ca/testEnvironment/callback"
response_type = "code"
# TODO: determine what we should set for the state value, if anything


def get_authorization_code_uri():
    logger = logging.getLogger(__name__)
    base_uri = "https://api-identity.bqecore.com/idp/connect/authorize?"
    core_token = None
    with transaction.atomic():
        if CoreTokens.objects.filter(_singleton=True).exists():
            core_token = CoreTokens.objects.select_for_update().get(_singleton=True)
        else:
            core_token = CoreTokens()
            core_token.refresh_token_expiry = datetime.datetime.now(timezone.utc)
            core_token.access_token_expiry = datetime.datetime.now(timezone.utc)
        core_token.state = uuid.uuid4().hex
        final_url = base_uri + urllib.parse.urlencode(
            {"client_id": client_id, "scope": scope, "redirect_uri":
                redirect_uri, "response_type": response_type, "state": '{"state": ' + core_token.state + '}'})
        logger.info("Requested a new authorization code.")
        core_token.save()
        return final_url


def get_access_token(request):
    # compare the state value from the request to the state value we set, and then set the code response
    logger = logging.getLogger(__name__)
    base_uri = "https://api-identity.bqecore.com/idp/connect/token"
    code = request.GET.get('code', None)
    logger.info(request.build_absolute_uri())
    logger.info(request.body.decode('utf-8'))
    with transaction.atomic():
        core_token = CoreTokens.objects.select_for_update().get(_singleton=True)
        if code is None:
            logger.error("Could not parse the authorization code from the callback, and therefore cannot get the "
                         "access token.")
            core_token.waiting_for_tokens = False
            core_token.save()
            return
        core_token.token_request_code = code
        logger.info("Requesting access token.")
        response = requests.post(base_uri, data={
            "code": core_token.token_request_code,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": "",
        }, headers={"Content-Type": "application/x-www-form-urlencoded"})
        logger.info(str(response.request.url))
        logger.info(str(response))
        json_data = response.json()
        logger.info(str(json_data))
        core_token.access_token = json_data.get("access_token")
        core_token.access_token_expiry = datetime.datetime.now(timezone.utc) + \
                                         datetime.timedelta(seconds=json_data.get("expires_in"))
        # core_token.refresh_token = json_data.get("refresh_token")
        # core_token.refresh_token_expiry = datetime.datetime.now(timezone.utc) + \
        #                                   datetime.timedelta(seconds=json_data.get("refresh_token_expires_in"))
        core_token.endpoint = json_data.get("endpoint")
        core_token.access_token_type = json_data.get("token_type")
        core_token.save()
        logger.info("Tokens received.")
        logger.info("Access token: " + str(core_token.access_token))
        logger.info("Access token expiry: " + str(core_token.access_token_expiry))
        logger.info("Endpoint: " + str(core_token.endpoint))
        logger.info("Token Type: " + str(core_token.access_token_type))
        # logger.info("Refresh token: " + str(core_token.refresh_token))
        # logger.info("Refresh token expiry: " + str(core_token.refresh_token_expiry))
    pass


def get_refresh_code_uri():
    logger = logging.getLogger(__name__)
    base_uri = "https://api-identity.bqecore.com/idp/connect/authorize?"
    core_token = None
    with transaction.atomic():
        if CoreTokens.objects.filter(_singleton=True).exists():
            core_token = CoreTokens.objects.select_for_update().get(_singleton=True)
        else:
            logger.log("A refresh token was requested, but no core token was found.")
            return
        final_url = base_uri + urllib.parse.urlencode(
            {"client_id": client_id, "scope": "offline_access", "redirect_uri":
                redirect_uri, "response_type": response_type, "token": core_token.access_token})
        logger.info("Requested an authentication code for a refresh token.")
        # TODO: this is giving me an error indicating I have specified an invalid scope, despite the fact that the app
        # is configured to allow offline access. I need to investigate this further.
        return final_url


def get_refresh_token(request):
    # compare the state value from the request to the state value we set, and then set the code response
    logger = logging.getLogger(__name__)
    base_uri = "https://api-identity.bqecore.com/idp/connect/token"
    code = request.GET.get('code', None)
    logger.info(request.build_absolute_uri())
    logger.info(request.body.decode('utf-8'))
    with transaction.atomic():
        core_token = CoreTokens.objects.select_for_update().get(_singleton=True)
        if code is None:
            logger.error("Could not parse the authorization code from the callback, and therefore cannot get the "
                         "refresh and access tokens.")
            core_token.waiting_for_tokens = False
            core_token.save()
            return
        core_token.token_request_code = code
        logger.info("Requesting refresh and access tokens.")
        response = requests.post(base_uri, data={
            "code": core_token.token_request_code,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": "",
        }, headers={"Content-Type": "application/x-www-form-urlencoded"})
        logger.info(str(response.request.url))
        logger.info(str(response))
        json_data = response.json()
        logger.info(str(json_data))
        core_token.access_token = json_data.get("access_token")
        core_token.access_token_expiry = datetime.datetime.now(timezone.utc) + \
                                         datetime.timedelta(seconds=json_data.get("expires_in"))
        core_token.refresh_token = json_data.get("refresh_token")
        # core_token.refresh_token_expiry = datetime.datetime.now(timezone.utc) + \
        #                                   datetime.timedelta(seconds=json_data.get("refresh_token_expires_in"))
        # core_token.endpoint = json_data.get("endpoint")
        core_token.access_token_type = json_data.get("token_type")
        core_token.save()
        logger.info("Tokens received.")
        logger.info("Access token: " + str(core_token.access_token))
        logger.info("Access token expiry: " + str(core_token.access_token_expiry))
        # logger.info("Endpoint: " + str(core_token.endpoint))
        logger.info("Token Type: " + str(core_token.access_token_type))
        logger.info("Refresh token: " + str(core_token.refresh_token))
        # logger.info("Refresh token expiry: " + str(core_token.refresh_token_expiry))
    pass


'''
Takes local users and syncs them with the Core API.

This takes the local users and writes their attributes over the corresponding Client object in Core. If a linked Client
object does not exist, then it creates a new one.
'''
def sync_users():
    pass
