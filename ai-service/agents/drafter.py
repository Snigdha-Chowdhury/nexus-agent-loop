from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

llm = ChatGroq(model="openai/gpt-oss-20b")
def draft(research_notes: str) -> str:
    prompt=f"Draft a structured summary based on these researched notes:\n\n{research_notes}"
    response=llm.invoke([HumanMessage(content=prompt)])
    return response.content