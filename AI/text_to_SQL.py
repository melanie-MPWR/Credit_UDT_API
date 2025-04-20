from typing_extensions import Annotated, TypedDict
from langchain import hub
import getpass
import os
from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(model='claude-3-opus-20240229')
# anthropic ai

if "ANTHROPIC_API_KEY" not in os.environ:
    os.environ["ANTHROPIC_API_KEY"] = getpass.getpass("Enter your Anthropic API key: ")


llm = ChatAnthropic(
    model="claude-3-5-sonnet-20240620",
    temperature=0,
    max_tokens=1024,
    timeout=None,
    max_retries=2,
    # other params...
)

class QueryOutput(TypedDict):
    """Generated SQL query."""

    query: Annotated[str, ..., "Syntactically valid SQL query."]

def getQueryPrompt():
    query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")

    assert len(query_prompt_template.messages) == 2
    for message in query_prompt_template.messages:
        message.pretty_print()
    return

def write_query(question):
    """Generate SQL query to fetch information."""
    query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")
    prompt = query_prompt_template.invoke(
        {
            "dialect": "SQL",
            "top_k": 10,
            "table_info": ['accounts', 'transcactions'],
            "input": question,
        }
    )
    structured_llm = llm.with_structured_output(QueryOutput)
    result = structured_llm.invoke(prompt)
    return result["query"]



