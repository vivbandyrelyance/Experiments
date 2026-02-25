# Salesforce Agent Experiment

A LangChain + Claude agent that queries Salesforce Leads, Contacts, and Accounts,
and sends marketing emails from your org.

---

## Part 1 — One-time Salesforce setup (do this first)

### 1. Enable outbound email

Developer Edition orgs block all API-sent email by default.

**Setup → Email → Deliverability → Access Level → All Email** → Save

### 2. Get your security token

The security token is a separate credential required for API access.

Your Name (top-right avatar) → **Settings** → **Personal** → **Reset My Security Token**
→ Check your email for a message from Salesforce — the token is in the body.

Keep it somewhere safe. It only changes if you reset it again.

---

## Part 2 — Local setup

### 1. Create and activate a virtual environment

```bash
cd salesforce-agent-experiment
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
# .venv\Scripts\activate       # Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure credentials

```bash
cp .env.example .env
```

Open `.env` and fill in:

| Variable | Where to find it |
|---|---|
| `SALESFORCE_USERNAME` | Your Salesforce login email |
| `SALESFORCE_PASSWORD` | Your Salesforce login password |
| `SALESFORCE_SECURITY_TOKEN` | From the reset email (Step 1 above) |
| `SALESFORCE_DOMAIN` | `login` for Developer Edition; `test` for sandboxes |
| `ANTHROPIC_API_KEY` | https://console.anthropic.com |

The `.env` file is git-ignored — it will never be committed.

---

## Part 3 — Run the agent

```bash
python agent.py
```

The agent starts an interactive session. Type naturally.

### Example prompts to try

**Querying**
```
Show me the first 10 leads
Show me contacts at Acme
Show me tech companies in our accounts
Show me leads with no email address
Show me open leads from our website
```

**Emails**
```
Send a marketing email to all leads from Acme about our new product launch
Draft a follow-up email to Jane Smith about her demo request
Send a re-engagement email to leads who haven't been contacted yet
```

The agent will always show you the draft and ask for confirmation before sending.

---

## Project structure

```
salesforce-agent-experiment/
├── .env.example          # Credential template
├── .env                  # Your real credentials (git-ignored)
├── requirements.txt
├── agent.py              # Entry point — run this
└── tools/
    ├── sf_connection.py  # Shared Salesforce connection
    ├── query_tools.py    # query_leads / query_contacts / query_accounts
    └── email_tool.py     # send_marketing_email
```

---

## Troubleshooting

| Error | Fix |
|---|---|
| `INVALID_LOGIN` | Wrong username, password, or security token. Re-check `.env`. |
| `INVALID_SESSION_ID` | Security token is wrong or expired — reset it again. |
| Email sends but recipient gets nothing | Setup → Deliverability → set to "All Email" |
| `SalesforceResourceNotFound` on emailSimple | API version mismatch — try `SALESFORCE_API_VERSION=57.0` in `.env` |
| `ModuleNotFoundError` | Make sure your venv is activated and you ran `pip install -r requirements.txt` |
