#!/usr/bin/env python3
# Built using Python 3.8.1 on March 16, 2020

import requests
import json


class CloudConformity:
    """
    Cloud Conformity API Client.

    A class to interact with Cloud Conformity API.
    Mostly what it does is making API call to Cloud Conformity endpoint using a Python library named requests.

    Args:
        api_key (str): A secure 64-bit strong key randomly generated by Cloud Conformity on behalf of a user.
        api_endpoint (str): One of the Cloud Conformity API endpoints. (default "https://eu-west-1-api.cloudconformity.com")
    """

    def __init__(self, api_key, api_endpoint="https://eu-west-1-api.cloudconformity.com"):
        self.api_endpoint = api_endpoint
        self.headers = {
            "Content-Type": "application/vnd.api+json",
            "Authorization": "ApiKey {api_key}".format(api_key=api_key)
        }

    def __generate_resource_endpoint(self, resource_endpoint):
        """
        Helper method to generate resource endpoint."

        Basically what is does is appending the resource endpoint to the API endpoint.

        Args:
            resource_endpoint (str): Resource endpoint defined on Cloud Conformity documentation.

        Returns:
            str: Full endpoint of a resource.
        """

        return "{api_endpoint}{resource_endpoint}".format(
            api_endpoint=self.api_endpoint,
            resource_endpoint=resource_endpoint
        )

    def __process_response(self, response):
        """
        Helper method to process API call response."

        In order to increase consistency, this method will help to reform response data into a predefined structure.
        This method will also raise an error when the status code is not 200

        Status Code Docs: https://github.com/cloudconformity/documentation-api

        Args:
            response (requests.Response): The Response object, which contains a server’s response to an HTTP request.

        Returns:
            dict: Response of the API

        Raises:
            requests.exceptions.HTTPError: If response.status_code != 200
        """

        message = ""
        if response.status_code == 201:
            message = "201 Created"
        elif response.status_code == 202:
            message = "202 Accepted"
        elif response.status_code == 204:
            message = "204 No Content"
        elif response.status_code == 301:
            message = "301 Moved Permanently"
        elif response.status_code == 304:
            message = "304 Not Modified"
        elif response.status_code == 400:
            message = "400 Bad Request"
        elif response.status_code == 401:
            message = "401 Unauthorized"
        elif response.status_code == 403:
            message = "403 Forbidden"
        elif response.status_code == 404:
            message = "404 Not Found"
        elif response.status_code == 422:
            message = "422 Unprocessable Entity"
        elif response.status_code == 500:
            message = "500 Internal Server Error"

        if message:
            raise requests.exceptions.HTTPError(message, response=response)

        return (response.json())

    def get_organisation_external_id(self):
        """
        Get the organisation's external ID.

        API Docs: https://github.com/cloudconformity/documentation-api/blob/master/ExternalId.md

        Returns
            dict: To see a sample response, you can access the API Docs link above.
        """

        endpoint = "/v1/organisation/external-id"

        response = requests.get(
            self.__generate_resource_endpoint(endpoint),
            headers=self.headers
        )

        return(self.__process_response(response))

    def create_account(self, aws_account_id, aws_account_name, aws_tag_environment, external_id, cost_package=False, subscriptionType="advanced"):
        """Create a new account to Cloud Conformity organisation.

        API Docs: https://github.com/cloudconformity/documentation-api/blob/master/Accounts.md

        Args:
            aws_account_id (int): A 12-digit number like 123456789000 and is used to construct Amazon Resource Names (ARN).
            aws_account_name (str): The name of the account in the Cloud Conformity, usually it is the same as the account's alias.
            aws_tag_environment (str): The name of the environment the account belongs to. Valid values are: testing, staging, production.
            external_id (str): The organisation's external ID.
            cost_package (bool): True for enabling the cost package add-on for the account (AWS spend analysis, forecasting, monitoring). (default False)
            subscriptionType (str): 'advanced' comes with Real-Time threat monitoring enabled, 'essentials' comes with Real-Time threat monitoring disabled. (default 'advanced')

        Returns
            dict: To see a sample response, you can access the API Docs link above.
        """

        endpoint = "/v1/accounts"

        payload = {
            "data": {
                "type": "account",
                "attributes": {
                    "name": aws_account_name,
                    "environment": aws_tag_environment,
                    "access": {
                        "keys": {
                            "roleArn": "arn:aws:iam::{}:role/CloudConformity".format(aws_account_id),
                            "externalId": external_id
                        }
                    },
                    "costPackage": cost_package,
                    "subscriptionType": subscriptionType
                }
            }
        }

        response = requests.post(
            self.__generate_resource_endpoint(endpoint),
            headers=self.headers,
            data=json.dumps(payload)
        )

        return(self.__process_response(response))

    def delete_account(self, account_id):
        """
        Delete existing account.

        API Docs: https://github.com/cloudconformity/documentation-api/blob/master/Accounts.md

        Args:
            account_id (str): Cloud Conformity ID of the account. Provide to delete the account.

        Returns
            dict: To see a sample response, you can access the API Docs link above.
        """

        endpoint = "/v1/accounts/{}".format(account_id)

        response = requests.delete(
            self.__generate_resource_endpoint(endpoint),
            headers=self.headers,
        )

        return(self.__process_response(response))

    def update_account(self, account_id, aws_account_name, aws_tag_environment, aws_tag_product_domain):
        """
        Update the account name, environment, and code.

        API Docs: https://github.com/cloudconformity/documentation-api/blob/master/Accounts.md

        Args:
            account_id (str): Cloud Conformity ID of the account. Provide to get only settings set for the specified account.
            aws_account_name (str): The name of the account in the Cloud Conformity, usually it is the same as the account's alias.
            aws_tag_environment (str): The name of the environment the account belongs to. Valid values are: testing, staging, production.
            aws_tag_product_domain (str): The 3-character-abbreviation of Product Domain who owns the AWS account.

        Returns
            dict: To see a sample response, you can access the API Docs link above.
        """

        endpoint = "/v1/accounts/{}".format(account_id)

        payload = {
            "data": {
                "attributes": {
                    "name": aws_account_name,
                    "environment": aws_tag_environment,
                    "tags": [
                        aws_tag_environment,
                        aws_tag_product_domain
                    ]
                }
            }
        }

        response = requests.patch(
            self.__generate_resource_endpoint(endpoint),
            headers=self.headers,
            data=json.dumps(payload)
        )

        return(self.__process_response(response))

    def list_accounts(self, aws_account_name=None):
        """
        Query all accounts that you have access to

        API Docs: https://github.com/cloudconformity/documentation-api/blob/master/Accounts.md

        Args:
            aws_account_name (str): Filter to get only account with the name of as specified. The value is the same as the account's alias. (default None)

        Returns
            dict: To see a sample response, you can access the API Docs link above.
        """

        endpoint = "/v1/accounts"

        response = requests.get(
            self.__generate_resource_endpoint(endpoint),
            headers=self.headers,
        )

        response = self.__process_response(response)

        if aws_account_name is not None:
            response = {
                "data": [
                    x for x in response["data"] if x["attributes"]["name"] == aws_account_name
                ]
            }

        return(response)

    def list_communication_settings(self, channel=None, account_id=None, include_parents=False):
        """
        List communication settings.

        API Docs: https://github.com/cloudconformity/documentation-api/blob/master/Settings.md

        Args:
            channel (str): Provide if you want to only get settings for one specific channel: email, sms, slack, pager-duty, or sns.
            account_id (str): Cloud Conformity ID of the account. Provide to get only settings set for the specified account.
            include_parents (bool): Specify true if you want to see both account level settings and organisation level settings.

        Returns:
            dict: To see a sample response, you can access the API Docs link above.
        """

        endpoint = "/v1/settings/communication"

        if ((channel is not None) or (account_id is not None)):
            endpoint = "{endpoint}?".format(endpoint=endpoint)

            endpoint = "{endpoint}&accountId={account_id}".format(
                endpoint=endpoint,
                account_id=account_id,
            ) if account_id is not None else endpoint

            endpoint = "{endpoint}&channel={channel}".format(
                endpoint=endpoint,
                channel=channel
            ) if channel is not None else endpoint

            endpoint = "{endpoint}&includeParents={include_parents}".format(
                endpoint=endpoint,
                include_parents="true" if include_parents else "false"
            ) if account_id is not None else endpoint

            endpoint = endpoint.replace("?&", "?")

        response = requests.get(
            self.__generate_resource_endpoint(endpoint),
            headers=self.headers
        )

        # There is a bug in the API that `channel` query string doesn't work.
        # This additional processing is to handle the issue.
        response = {
            "data": [x for x in self.__process_response(response)["data"] if x["attributes"]["channel"] == channel]
        }

        return(response)

    def delete_communication_setting(self, setting_id):
        """
        Delete a communication setting.

        API Docs: https://github.com/cloudconformity/documentation-api/blob/master/Settings.md

        Args:
            setting_id (str): The Cloud Conformity ID of the communication setting.

        Returns
            dict: To see a sample response, you can access the API Docs link above.
        """

        endpoint = "/v1/settings/{}".format(setting_id)

        response = requests.delete(
            self.__generate_resource_endpoint(endpoint),
            headers=self.headers
        )

        return(self.__process_response(response))

    def list_profiles(self):
        """
        List profiles associated to the organisation.

        API Docs: https://github.com/cloudconformity/documentation-api/blob/master/Profiles.md

        Returns:
            dict: To see a sample response, you can access the API Docs link above.
        """

        endpoint = "/v1/profiles"

        response = requests.get(
            self.__generate_resource_endpoint(endpoint),
            headers=self.headers
        )

        return(self.__process_response(response))

    def get_profile(self, profile_id):
        """
        Get a profile associated to organisation.

        API Docs: https://github.com/cloudconformity/documentation-api/blob/master/Profiles.md

        Args:
            profile_id (str): The Cloud Conformity ID of the profile.

        Returns
            dict: To see a sample response, you can access the API Docs link above.
        """

        endpoint = "/v1/profiles/{}".format(profile_id)

        response = requests.get(
            self.__generate_resource_endpoint(endpoint),
            headers=self.headers
        )

        return(self.__process_response(response))

    def apply_profile_to_accounts(self, profile_id, account_ids, mode="replace"):
        """
        Apply profile to a set of accounts under the organisation.

        API Docs: https://github.com/cloudconformity/documentation-api/blob/master/Profiles.md

        Args:
            profile_id (str): The Cloud Conformity ID of the profile.
            account_id (list): An Array of account Id's that will be configured by the profile.
            mode (str): Mode of how the profile will be applied to the accounts, i.e. "fill-gaps", "overwrite" or "replace". (default 'replace')
                        - fill-gaps: Merge existing settings with this Profile. If there is a conflict, the account's existing setting will be used.
                        - overwrite: Merge existing settings with this Profile. If there is a conflict, the Profile's setting will be used.
                        - replace  : Clear all existing settings and apply settings from this Profile.

        Returns
            dict: To see a sample response, you can access the API Docs link above.
        """

        endpoint = "/v1/profiles/{}/apply".format(profile_id)

        profile_name = self.get_profile(
            profile_id=profile_id
        )["data"]["attributes"]["name"]

        payload = {
            "meta": {
                "accountIds": account_ids,
                "types": ["rule"],
                "mode": mode,
                "notes": "Applied from Profile: {profile_name}".format(profile_name=profile_name)
            }
        }

        response = requests.post(
            self.__generate_resource_endpoint(endpoint),
            headers=self.headers,
            data=json.dumps(payload)
        )

        return(self.__process_response(response))

    def create_report_configuration(self, account_id, aws_account_name, recipient_email_addresses):
        """
        Create a new report config for an account.

        API Docs: https://github.com/cloudconformity/documentation-api/blob/master/ReportConfigs.md

        Args:
            account_id (str): The Cloud Conformity ID of the communication setting.
            aws_account_name (str): The name of the account in the Cloud Conformity, usually it is the same as the account's alias.
            recipient_email_addresses (list): List of email addresses that will receive the reports

        Returns
            dict: To see a sample response, you can access the API Docs link above.
        """

        endpoint = "/v1/report-configs"

        payload = {
            "data": {
                "attributes": {
                    "accountId": account_id,
                    "configuration": {
                        "title": "[Cloud Conformity] Report for {}".format(aws_account_name),
                        "scheduled": True,
                        "frequency": "* * MON",
                        "tz": "Asia/Jakarta",
                        "sendEmail": True,
                        "emails": recipient_email_addresses,
                        "filter": {
                            "statuses": [
                                "FAILURE"
                            ],
                            "riskLevels": [
                                "EXTREME",
                                "VERY_HIGH",
                                "HIGH"
                            ],
                            "suppressed": False
                        }
                    }
                }
            }
        }

        response = requests.post(
            self.__generate_resource_endpoint(endpoint),
            headers=self.headers,
            data=json.dumps(payload)
        )

        return(self.__process_response(response))

    def update_account_bot_settings(self, account_id, is_disabled=False, disabled_until=None, scan_interval_hour=None, disabled_regions=[]):
        """
        Update Conformity Bot settings for an account.

        API Docs: https://github.com/cloudconformity/documentation-api/blob/master/Accounts.md

        Args:
            account_id (str): The Cloud Conformity ID of the communication setting.
            is_disabled (bool): A boolean value to disable or enable the Conformity Bot (default False)
            disabled_until (int): A date-time in Unix Epoch timestamp format (in milliseconds). 
                                  Setting this value will disable the Conformity Bot until the date and time indicated. 
                                  Setting this value to null will disable the Conformity Bot indefinitely if disabled field is set to true.
            scan_interval_hour (int): An integer value that sets the number of hours delay between Conformity Bot runs.
            disabled_regions (list): This field can only be applied to AWS accounts. 
                                     An attribute object containing a list of AWS regions for which Conformity Bot runs will be disabled.

        Returns
            dict: To see a sample response, you can access the API Docs link above.
        """

        endpoint = "/v1/accounts/{}/settings/bot".format(account_id)

        bot_settings = {}

        if is_disabled == True:
            bot_settings["disabled"] = True

        if disabled_until is not None:
            bot_settings["disabledUntil"] = int(disabled_until)

        if scan_interval_hour is not None:
            bot_settings["delay"] = int(scan_interval_hour)

        if len(disabled_regions) > 0:
            bot_settings["disabledRegions"] = {}
            for region in disabled_regions:
                bot_settings["disabledRegions"][region] = True

        payload = {
            "data": {
                "type": "accounts",
                "attributes": {
                    "settings": {
                        "bot": bot_settings
                    }
                }
            }
        }

        response = requests.patch(
            self.__generate_resource_endpoint(endpoint),
            headers=self.headers,
            data=json.dumps(payload)
        )

        return(self.__process_response(response))
