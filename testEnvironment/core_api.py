import datetime
import logging
import urllib.parse

import requests, uuid
from datetime import timezone
from .models import CoreTokens
from django.db import transaction


client_id = "eA172bI8p3IQFDxLrZuv6oTbHIe2MSat.apps.bqe.com"  # TODO: store in constants manager or config file
scope = "readwrite:core"
redirect_uri = "https://andrewmckernan.ca/testEnvironment/callback"
response_type = "code"
# TODO: determine what we should set for the state value, if anything


def get_authorization_code_uri():
    logger = logging.getLogger(__name__)
    base_uri = "https://api-identity.bqecore.com/idp/connect/authorize"
    core_token = None
    with transaction.atomic():
        if CoreTokens.objects.filter(_singleton=True).exists():
            core_token = CoreTokens.objects.select_for_update().get(_singleton=True)
        else:
            core_token = CoreTokens()
            core_token.refresh_token_expiry = datetime.datetime.now(timezone.utc)
            core_token.access_token_expiry = datetime.datetime.now(timezone.utc)
        # TODO: probably need to make timezone aware
        # if we're waiting, or we don't need to update, then don't request another one
        if core_token.waiting_for_tokens or core_token.refresh_token_expiry > datetime.datetime.now(timezone.utc):
            logger.info("We are either waiting for tokens, or we don't need to update, so we will not request more.")
            return
        core_token.state = uuid.uuid4().hex
        # result = requests.get(base_uri, params={"client_id": client_id, "scope": scope, "redirect_uri":
        #                       redirect_uri, "response_type": response_type, "state": core_token.state})
        final_url = base_uri + urllib.parse.urlencode(
            {"client_id": client_id, "scope": scope, "redirect_uri":
                redirect_uri, "response_type": response_type, "state": core_token.state})
        logger.info("Requested a new authorization code.")
        core_token.waiting_for_tokens = True  # TODO: potentially remove this field
        core_token.save()
        return final_url


def get_refresh_and_access_tokens(request):
    # compare the state value from the request to the state value we set, and then set the code response
    logger = logging.getLogger(__name__)
    if request.method == "POST":
        logger.info("POST request received.")
    elif request.method == "GET":
        logger.info("GET request received.")
    base_uri = "https://api-identity.bqecore.com/idp/connect/token "
    code = request.GET.get('code', None)
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
        response = requests.post(base_uri, params={
            "code": core_token.token_request_code,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": "",
        }, headers={"Content-Type": "application/x-www-form-urlencoded"})
        json_data = response.json()
        core_token.access_token = json_data.get("access_token")
        core_token.access_token_expiry = datetime.datetime.now(timezone.utc) + \
                                         datetime.timedelta(seconds=json_data.get("expires_in"))
        core_token.refresh_token = json_data.get("refresh_token")
        core_token.refresh_token_expiry = datetime.datetime.now(timezone.utc) + \
                                          datetime.timedelta(seconds=json_data.get("refresh_token_expires_in"))
        core_token.waiting_for_tokens = False
        core_token.save()
        logger.info("Refresh and access tokens received.")
        logger.info("Access token: " + str(core_token.access_token))
        logger.info("Access token expiry: " + str(core_token.access_token_expiry))
        logger.info("Refresh token: " + str(core_token.refresh_token))
        logger.info("Refresh token expiry: " + str(core_token.refresh_token_expiry))
    pass
