from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool, save_tool

load_dotenv() # This will load the ".env"

# Setup LLM
# llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
# Simple example
# response = llm.invoke("What is the meaning of life?")
# print(response)


# To specify all the output fields we want from our LLM call
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

# Generate the LLM
llm = ChatOpenAI(model="gpt-4o-mini")
# Make the parser
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# Create a prompt and set a prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant that will help generate a research paper.
            Answer the user query and use necessary tools.
            Wrap the output in this format and provide no other test\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

# Creating a simple agent
tools = [search_tool, wiki_tool, save_tool] # List of tools from tools.py
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

# Create an agent executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
query = input("What can I help you research? ")
# here you  add the parameters from the above prompt "human". You can add more parameters to e.g) {name}. In this case you add it to the "human" as well.
raw_response = agent_executor.invoke({"query": query})
# Generate the raw response
print(f"Raw Response: {raw_response}")

try:
    structured_response = parser.parse(raw_response.get("output"))
    print(f"Structured response using parser: \n{structured_response}")
except Exception as e:
    print("Error parsing response", e, "Raw Response - ", raw_response)
