import dotenv
dotenv.load_dotenv()

# llamaindex deps
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.llms.gemini import Gemini
import tiktoken
# from llama_index.core.agent import ReActAgent
# from llama_index.tools.google import GmailToolSpec

from gmail import GmailSearcher

searcher = GmailSearcher()

# dotenv is taking care of the OpenAI API key for us
#MODEL = "gpt-4o"
MODEL = "gpt-3.5-turbo"
Settings.llm = OpenAI(model=MODEL)

# Settings.llm = Gemini(
#     model="models/gemini-1.5-pro-latest",
#     temperature=0.1
# )

def sliceUntilFits(string, max_tokens):
    enc = tiktoken.encoding_for_model(MODEL)
    while True:
        encoded = enc.encode(string)    
        print(f"Number of tokens: {len(encoded)}")
        if len(encoded) > max_tokens:
            print("Message too long, slicing it down")
            string = string[-10000:] # slice off the last 10000 characters
        else:
            return string


def summarizeMessages(messages):
    for message in messages:
        print("Handling a message")
        print(message['extra_info'])
        instructions = f"""
            Attached is the body of an email message. If the email is a flight itinerary, summarize the origin and destination of the flight in JSON, like this:
            {{
                isItinerary: true,
                origin: "San Francisco, USA",
                destination: "New York City, USA"
            }}
            If the email is not an itinerary (most will not be), just responsd with:
            {{
                isItinerary: false
            }}
            Respond with JSON *only*, you do not need triple ticks or any other quoting.
            
            Message is below this line:
            ------------
            {message['text']}
            """
        # openai has a maximum string length it can handle
        instructions = sliceUntilFits(instructions, 128000)
        response = Settings.llm.complete(instructions)
        print(response)

next_token = None
while True:
    # TODO: get the LLM to think of good searches
    messageResults = searcher.search_messages(
        "your flight itinerary", 
        max_results=2, 
        next_token=next_token
    )
    summarizeMessages(messageResults['messages'])
    if messageResults['next_token']:
        next_token = messageResults['next_token']
    else:
        break
