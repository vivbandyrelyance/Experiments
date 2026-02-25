"""
Salesforce Agent — interactive CLI

Lets you query Leads, Contacts, and Accounts, and send marketing emails
from Salesforce. The agent always drafts and confirms emails before sending.

Usage:
    python agent.py
"""

from dotenv import load_dotenv

# Load .env before anything else — the Anthropic client reads
# ANTHROPIC_API_KEY at import time.
load_dotenv()

from langchain_anthropic import ChatAnthropic
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage

from tools.query_tools import query_leads, query_contacts, query_accounts
from tools.email_tool import send_marketing_email

SYSTEM_PROMPT = """You are a Salesforce CRM assistant. You help users query their \
Salesforce org and send marketing emails to leads and contacts.

## Tools available
- query_leads          — search Leads by any SOQL filter
- query_contacts       — search Contacts by any SOQL filter
- query_accounts       — search Accounts by any SOQL filter
- send_marketing_email — send an email via Salesforce

## Rules you must follow

### Querying
- Use SOQL filters when the user narrows by name, company, status, etc.
- For relationship fields use dot notation: Account.Name = 'Acme'
- String literals in SOQL must use single quotes.

### Emailing
1. Always look up the recipient in Salesforce first to get their real name and email.
2. Compose a draft email (subject + plain-text body + HTML body).
3. Show the full draft to the user — who it goes to, subject, and body.
4. Ask the user: "Shall I send this? (yes / no)"
5. Only call send_marketing_email after the user says yes.
6. For bulk sends (multiple recipients), list all recipients and confirm once before sending any.

Keep responses concise. When showing records, summarise rather than dumping raw JSON \
unless the user asks for details."""


def main() -> None:
    llm = ChatAnthropic(model="claude-sonnet-4-6", temperature=0)

    tools = [query_leads, query_contacts, query_accounts, send_marketing_email]

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
    )

    # Seed the message history with the system prompt so it persists across turns
    messages: list = []

    print("\n=== Salesforce Agent ===")
    print("Type your request, or 'exit' to quit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit", "bye"):
            print("Goodbye.")
            break

        messages.append(HumanMessage(content=user_input))

        result = agent.invoke({"messages": messages})

        # result["messages"] is the full updated history
        messages = result["messages"]

        # Last message is always the assistant's response
        response = messages[-1].content

        print(f"\nAgent: {response}\n")


if __name__ == "__main__":
    main()
