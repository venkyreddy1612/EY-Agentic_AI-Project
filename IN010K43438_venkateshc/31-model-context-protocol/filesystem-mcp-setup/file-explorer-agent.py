import requests
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

# -----------------------------
# CONFIG
# -----------------------------

f = open(r"E:\Lenovo Ideapad 330\company-material\digital-workforce-transformation\ai-upskill-4\key-vault\openai\openai-api-key.txt")
apikey = f.read()
f.close()

OPENAI_API_KEY = apikey.strip()
MCP_BASE_URL = "http://127.0.0.1:8000"

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=OPENAI_API_KEY,
    temperature=0
)

# -----------------------------
# MCP TOOL WRAPPERS
# -----------------------------

@tool
def list_files(_=""):
    """List all files in the directory"""
    res = requests.post(f"{MCP_BASE_URL}/tools/list_files")
    return str(res.json())

@tool
def read_file(path):
    """Read file content. Input should be a filename"""
    res = requests.post(
        f"{MCP_BASE_URL}/tools/read_file",
        json={"path": path}
    )
    return res.json().get("content", "Error reading file")

@tool
def write_file(input_str):
    """
    Write to a file. Input format: filename|content
    Expected format:
    filename|content
    """
    try:
        path, content = input_str.split("|", 1)
        res = requests.post(
            f"{MCP_BASE_URL}/tools/write_file",
            json={"path": path.strip(), "content": content.strip()}
        )
        return str(res.json())
    except Exception as e:
        return f"Error: {str(e)}"


# -----------------------------
# TOOL DEFINITIONS
# -----------------------------
tools = [
   list_files,
   write_file,
   read_file
]

# -----------------------------
# AGENT
# -----------------------------
agent = create_agent(
    llm,
    tools
)

# -----------------------------
# RUN LOOP
# -----------------------------
if __name__ == "__main__":
    print("\n📁 MCP File Explorer Agent Ready!\n")
    
    while True:
        query = input("🧑 You: ")
        
        if query.lower() in ["exit", "quit"]:
            break
        
        response = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": query
                    }
                ]
            }
        )

        print("\n🤖 Agent:\n")
        print(response["messages"][-1].content)
        print()

'''
List all files
Create a file called test.txt with content Hello MCP world
Read test.txt
Summarize the contents of test.txt

'''