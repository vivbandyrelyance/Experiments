import os
from simple_salesforce import Salesforce


def get_sf_connection() -> Salesforce:
    """Return an authenticated Salesforce connection using env vars."""
    return Salesforce(
        username=os.environ["SALESFORCE_USERNAME"],
        password=os.environ["SALESFORCE_PASSWORD"],
        security_token=os.environ["SALESFORCE_SECURITY_TOKEN"],
        domain=os.environ.get("SALESFORCE_DOMAIN", "login"),
        version=os.environ.get("SALESFORCE_API_VERSION", "62.0"),
    )
