import json
from langchain_core.tools import tool
from tools.sf_connection import get_sf_connection


def _records(result: dict) -> str:
    """Strip Salesforce metadata noise and return clean JSON string of records."""
    records = result.get("records", [])
    # Remove the 'attributes' key Salesforce adds to every record
    for r in records:
        r.pop("attributes", None)
    return json.dumps(records, indent=2)


@tool
def query_leads(soql_filter: str = "") -> str:
    """Query Salesforce Leads and return their details.

    Args:
        soql_filter: Optional WHERE clause content, e.g. "Email != null" or
                     "Status = 'Open - Not Contacted'" or "Company = 'Acme'".
                     Leave empty to return the first 50 leads.

    Returns JSON list of leads with Id, Name, Email, Company, Phone, Status, LeadSource.
    """
    sf = get_sf_connection()
    where = f"WHERE {soql_filter}" if soql_filter.strip() else ""
    query = (
        f"SELECT Id, Name, Email, Company, Phone, Status, LeadSource "
        f"FROM Lead {where} LIMIT 50"
    )
    return _records(sf.query(query))


@tool
def query_contacts(soql_filter: str = "") -> str:
    """Query Salesforce Contacts and return their details.

    Args:
        soql_filter: Optional WHERE clause content, e.g. "Email != null" or
                     "Account.Name = 'Acme'" or "LastName = 'Smith'".
                     Leave empty to return the first 50 contacts.

    Returns JSON list of contacts with Id, Name, Email, Phone, Account name.
    """
    sf = get_sf_connection()
    where = f"WHERE {soql_filter}" if soql_filter.strip() else ""
    query = (
        f"SELECT Id, Name, Email, Phone, Account.Name "
        f"FROM Contact {where} LIMIT 50"
    )
    return _records(sf.query(query))


@tool
def query_accounts(soql_filter: str = "") -> str:
    """Query Salesforce Accounts and return their details.

    Args:
        soql_filter: Optional WHERE clause content, e.g. "Industry = 'Technology'" or
                     "BillingCountry = 'US'" or "Name LIKE 'Acme%'".
                     Leave empty to return the first 50 accounts.

    Returns JSON list of accounts with Id, Name, Industry, Phone, Website, BillingCity.
    """
    sf = get_sf_connection()
    where = f"WHERE {soql_filter}" if soql_filter.strip() else ""
    query = (
        f"SELECT Id, Name, Industry, Phone, Website, BillingCity, BillingCountry "
        f"FROM Account {where} LIMIT 50"
    )
    return _records(sf.query(query))
