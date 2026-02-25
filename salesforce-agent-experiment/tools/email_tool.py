import json
from langchain_core.tools import tool
from tools.sf_connection import get_sf_connection


@tool
def send_marketing_email(
    recipient_email: str,
    recipient_name: str,
    subject: str,
    body_text: str,
    body_html: str,
) -> str:
    """Send a marketing email to a lead or contact via Salesforce.

    IMPORTANT: Only call this tool after the user has explicitly confirmed they
    want to send the email. Always show the draft first and wait for confirmation.

    Args:
        recipient_email: The email address to send to.
        recipient_name:  The recipient's full name (for your reference/logging).
        subject:         The email subject line.
        body_text:       Plain-text version of the email body.
        body_html:       HTML version of the email body (use inline styles; no <head>).

    Returns a success or error message string.
    """
    sf = get_sf_connection()

    payload = {
        "inputs": [
            {
                "emailAddresses": recipient_email,
                "emailSubject": subject,
                "emailBody": body_text,
                "emailHtmlBody": body_html,
                "senderType": "CurrentUser",
            }
        ]
    }

    try:
        result = sf.restful(
            "actions/standard/emailSimple",
            method="POST",
            json=payload,
        )
        if result and isinstance(result, list) and result[0].get("isSuccess"):
            return f"Email sent successfully to {recipient_name} <{recipient_email}>."
        else:
            return f"Salesforce reported a failure: {json.dumps(result)}"
    except Exception as e:
        return f"Error sending email: {e}"
