from agents import Agent, Runner, function_tool, trace
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

load_dotenv()

# -------- SYSTEM PROMPTS -------- #
SYSTEM_PROMPT1 = """\
You are an AI email writer. Write persuasive yet concise marketing emails that sell online Computer Science courses.
Focus on clarity, strong value propositions, benefits, and a direct call-to-action.
"""

SYSTEM_PROMPT2 = """\
Your task is to craft high-impact sales emails promoting online Computer Science courses.
Use a confident, benefit-led tone and speak to individuals seeking skill growth or career upgrades.
Highlight outcomes (jobs, certificates, portfolio), remove hesitation, establish credibility,
and end with a compelling CTA that drives enrollment. Avoid unnecessary fluff.
"""

SYSTEM_PROMPT3 = """\
Write emails like a friendly mentor inviting someone to check out your online Computer Science courses.
Keep the tone warm and relatable, explain how the courses can help them learn coding,
get projects done, or land better opportunities. Make it feel personal, simple to read,
and end with an easy next-step CTA (“Join today,” “Take the first class,” etc.).
"""

# -------- SALES AGENTS -------- #
sales_agent1 = Agent(name="Sales Agent 1", instructions=SYSTEM_PROMPT1)
sales_agent2 = Agent(name="Sales Agent 2", instructions=SYSTEM_PROMPT2)
sales_agent3 = Agent(name="Sales Agent 3", instructions=SYSTEM_PROMPT3)

tool1 = sales_agent1.as_tool(tool_name="sales_tool_1", tool_description="Sales tool for online courses")
tool2 = sales_agent2.as_tool(tool_name="sales_tool_2", tool_description="Sales tool for online courses")
tool3 = sales_agent3.as_tool(tool_name="sales_tool_3", tool_description="Sales tool for online courses")

sales_tools = [tool1, tool2, tool3]


# -------- EMAIL SENDING TOOL -------- #
@function_tool
def sendEmail(message: str, subject: str = "Demo"):
    """Function Tool to send emails to the user"""

    api_key = os.environ.get("SENDGRID_API_KEY")
    from_email = os.environ.get("FROM_EMAIL")
    to_email = os.environ.get("TO_EMAIL")

    if not api_key or not from_email or not to_email:
        return {
            "status": "error",
            "error": "Missing SENDGRID_API_KEY, FROM_EMAIL or TO_EMAIL env variables."
        }

    mail = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=message
    )

    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(mail)
        return {"status": "success", "status_code": response.status_code}
    except Exception as e:
        return {"status": "failed", "error": str(e)}


# -------- SUBJECT & HTML AGENTS -------- #
subject_agent = Agent(
    name="Subject Agent",
    instructions="Generate catchy subject lines for marketing emails."
)
html_agent = Agent(
    name="HTML Agent",
    instructions="Convert plain text emails to clean responsive HTML format."
)

subject_tool = subject_agent.as_tool("subject_tool", "Subject tool for online courses")
html_tool = html_agent.as_tool("html_tool", "HTML formatting tool for email body")

email_tools = [subject_tool, html_tool, sendEmail]

EMAIL_AGENT_PROMPT = """
You will take the selected winning sales email, generate a crisp subject line,
convert the message into HTML, and then call sendEmail() to email it to the user.
"""

email_agent = Agent(
    name="Email Agent",
    model="gpt-4o-mini",
    instructions=EMAIL_AGENT_PROMPT,
    tools=email_tools
)


# -------- MASTER SALES DECISION AGENT -------- #
SALES_ORCHESTRATOR_PROMPT = """
Your job: call all three sales tools, get 3 different email drafts,
pick the strongest / highest reply-chance email, then hand it off to Email Agent.

Return nothing — instead, use the handoff.
"""

orchestrator = Agent(
    name="Sales Orchestrator",
    model="gpt-4o-mini",
    instructions=SALES_ORCHESTRATOR_PROMPT,
    tools=sales_tools,
    handoffs=[email_agent]
)


# -------- RUNNER -------- #
if __name__ == "__main__":
    with trace("email-sales-handoff-v2"):
        runner = Runner.run_sync(orchestrator, "Begin")
        print(runner.final_output)
