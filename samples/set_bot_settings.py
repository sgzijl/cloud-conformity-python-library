from cloud_conformity import CloudConformity

if __name__ == "__main__":
    # To generate an API key, follow this guide https://www.cloudconformity.com/help/public-api/api-keys.html
    # Save the key to a file named "credentials"
    # In the file, make sure that there is no newline after the private key

    with open("credentials") as c:
        api_key = c.read()

    cc = CloudConformity(
        api_key=api_key
    )

    AWS_ACCOUNT_ALIASES = [
        "aws_alias_1",
        "aws_alias_2"
    ]

    data = cc.list_accounts(
        aws_account_names=AWS_ACCOUNT_ALIASES
    )["data"]

    cc_account_ids = [x["id"] for x in data]

    for account_id in cc_account_ids:
        data = cc.update_account_bot_settings(
            account_id=account_id,
            is_disabled=False,
            disabled_until=None,
            scan_interval_hour=6,
            disabled_regions=[
                "eu-north-1",
                "ap-northeast-1",
                "ap-northeast-2",
                "ap-south-1",
                "ap-southeast-2",
                "ca-central-1",
                "eu-central-1",
                "eu-west-1",
                "eu-west-2",
                "eu-west-3",
                "sa-east-1",
                "us-east-2",
                "us-west-1",
                "us-west-2"
            ]
        )
