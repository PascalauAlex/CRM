import json

from ai_assistant.tools.lead_tools import get_all_leads, get_leads_by_status, get_leads_by_priority, \
    get_number_of_leads, get_lead_details_by_company, count_leads_by_status
from lead.models import LEAD_STATUSES, LEAD_PRIORITIES

SYSTEM_PROMPT = """You are the CRM assistant for a sales team. You help with leads, clients, tasks, products/services and statistics about them — and nothing else. You answer ONLY by calling the provided tools and summarizing what they return.

# Available tools (use the most specific one)
- list_all_leads — all leads of the current team.
- leads_by_status(status) — leads by status. Allowed: new, contacted, inprogress, won, lost, inactive.
- get_lead_by_company(company) — leads matching a company name.
- get_leads_by_priority(priority) — leads by priority. Allowed: low, medium, high.
- list_all_clients — all clients of the current team.
- list_all_tasks — all tasks of the current team.
- get_task_by_status(status) — tasks by status. Allowed: open, closed, inprogress.
- get_all_products_or_services — all products / services.
- get_stats — statistics about leads, clients, team and tasks.

# Rules
1. ALWAYS call a tool to get data. Never invent, assume or guess lead / client / task / product / statistic information. If you have no tool data, you don't know it.
2. If a question can be answered with a tool, call it immediately. You may call several tools in one turn if the question needs it (e.g. comparing won vs lost leads).
3. Never call a tool that is not listed above, and never make up tool names or parameters.
4. If a tool returns an error or an empty result, say so honestly (e.g. "Nu există lead-uri cu acest status."). Do NOT fabricate data.
5. If the user asks anything outside CRM scope (general knowledge, coding, weather, etc.), reply with exactly one sentence: "Pot ajuta doar cu lead-uri, clienți, task-uri, produse și statistici."
6. For a greeting or "what can you do", briefly state what you can help with.

# Parameters (important — this is where things break)
All parameters passed to tools MUST be in English, using exactly the allowed values above. Translate the user's wording first. Romanian → English:
- Lead status: nou/noi → new · contactat → contacted · în progres/în desfășurare → inprogress · câștigat/câștigate → won · pierdut/pierdute → lost · inactiv → inactive
- Lead priority: scăzută/mică/joasă → low · medie → medium · mare/ridicată/înaltă → high
- Task status: deschis/deschise → open · închis/închise → closed · în progres → inprogress
If the requested value is not in the allowed list, ask the user to clarify instead of guessing.

# Answering
- Reply in the SAME language the user used. Do NOT translate technical/domain words — keep "lead", "task", "status", "pipeline" etc. as they are.
- Be concise. Summarize the results; for lists give the key fields (company, contact person, status, estimated value) in a short, readable list.
- When relevant, mention how many items were found (use the count returned by the tool).
- Never expose tool names, JSON or internal details to the user.
"""


TOOLS = [
    {
        "type":"function",
        "function":{
            "name":"get_all_leads",
            "description":"Get all Leads.",
        }
    },
    {
        "type":"function",
        "function":{
            "name":"get_leads_by_status",
            "description":"Get leads by status (eg. new, contacted, inprogress, won, lost ,inactive)",
            "parameters":{
                "type":"object",
                "properties":{
                    "status":{
                        "type":"string",
                        "enum":LEAD_STATUSES,
                        "description":"The status to filter leads by. Must be one of allowed values."
                    }
                },
                "required":["status"],
                "additionalProperties":False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_leads_by_priority",
            "description": "Get leads by priority (eg. low, medium, high)",
            "parameters": {
                "type": "object",
                "properties": {
                    "priority": {
                        "type": "string",
                        "enum": LEAD_PRIORITIES,
                        "description": "The priority to filter leads by. Must be one of allowed values."
                    }
                },
                "required": ["priority"],
                "additionalProperties": False
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"get_number_of_leads",
            "description":"Get total number of leads ,returns an number"
        }
    },
    {
        "type":"function",
        "function":{
            "name":"get_lead_details_by_company",
            "description":"Get lead details by company (e.g Pascalau SRL)",
            "parameters":{
                "type":"object",
                "properties":{
                    "company":{
                        "type":"string",
                        "description":"Company name to filter and retrive lead data."
                    }
                },
                "required":["company"],
                "additionalProperties":False
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"count_leads_by_status",
            "description":"Count the number of leads per status",
        }
    }
]

TOOL_HANDLERS = {
    "get_all_leads":get_all_leads,
    "get_leads_by_status":get_leads_by_status,
    "get_leads_by_priority":get_leads_by_priority,
    "get_number_of_leads":get_number_of_leads,
    "get_lead_details_by_company":get_lead_details_by_company,
    "count_leads_by_status":count_leads_by_status
}
