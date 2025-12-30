# AI Sales Email Agent

An AI-powered system that generates and sends marketing emails for online Computer Science courses using multiple specialized sales agents.

## Features

- Three specialized sales agents with different writing styles
- Automatic email generation and selection
- SendGrid integration for email delivery
- Agent-based architecture using OpenAI

## Setup

1. Install dependencies:
```bash
uv sync
```

2. Configure environment variables:
```bash
cp .env.example .env
```

Edit `.env` with your API keys:
- `OPENAI_API_KEY`: Your OpenAI API key
- `SENDGRID_API_KEY`: Your SendGrid API key
- `FROM_EMAIL`: Sender email address
- `TO_EMAIL`: Recipient email address

## Usage

```bash
python src/main.py
```

The system will:
1. Generate emails using three different sales agents
2. Select the most effective email
3. Send it via SendGrid

## Sales Agents

- **Agent 1**: Persuasive, concise marketing style
- **Agent 2**: High-impact, benefit-led approach  
- **Agent 3**: Friendly mentor tone

## Requirements

- Python 3.13+
- OpenAI API access
- SendGrid account