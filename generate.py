# dotenv will load our API keys from .env
import dotenv
dotenv.load_dotenv()

# llamaindex deps
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.llms.gemini import Gemini
from llama_index.llms.ollama import Ollama
import tiktoken
import json

from gmail import GmailSearcher
searcher = GmailSearcher()

# if using openAI, this specifies which model to use
# and it will use the same model for counting tokens.
# If using non-OpenAI model, it will count as if for an openAI model because I'm lazy
#MODEL="gemini-1.5-pro-latest"
#MODEL = "gpt-4o"
MODEL = "gpt-3.5-turbo"
#Settings.llm = OpenAI(model=MODEL)

# Settings.llm = Gemini(
#     model="models/gemini-1.5-pro-latest",
#     temperature=0.1
# )

Settings.llm = Ollama(model="llama3", request_timeout=30.0)

# some emails have attachments and are enormous and hard to parse
# so we slice everything down to 128k tokens or less.
def sliceUntilFits(string, max_tokens):
    enc = tiktoken.encoding_for_model(MODEL)
    while True:
        encoded = enc.encode(string)    
        print(f"Number of tokens: {len(encoded)}")
        if len(encoded) > 300000: # like, WAY too long
            string = string[-300000:] # get the last 300k chars
        elif len(encoded) > max_tokens:
            print("Message too long, slicing it down")
            string = string[:-10000] # remove the last 10k chars to shorten it
        else:
            return string

# this processes a batch of emails and modifies the python code via the LLM
def summarizeMessages(messages,extraction_code):
    for message in messages:
        print("Handling a message")
        print(message['extra_info'])
        instructions = f"""
            Attached is the body of an email message, and a block of python code (which might be empty). The Python code's job is to extract flight itineraries from emails. If you detect that the email is a flight itinerary, modify the Python code such that it would correctly extract the origin and destination of the flight from this email as well as the emails it already knows how to parse. The code should return JSON listing the origin and destination, like this:
            {{
                "isItinerary": true,
                "origin": "San Francisco, USA",
                "destination": "New York City, USA"
            }}
            If the email is not an itinerary (most will not be), you do not need to modify the python code.
            
            In either case, or if you can't figure out what to do, return the following JSON:
            {{
                "was_itinerary": True or False depending if it was an itinerary,
                "modified_code": true or false depending if you modified the code,
                "code": the python code, correctly enclosed in quotes and escaped for JSON
            }}
            You don't need to enclose the JSON in backticks or any other quoting, and you don't need to include any other information.
            
            The python code is between the next two lines of dashes:
            ------------
            {extraction_code}
            ------------

            And the text of the email is below this line:
            ------------
            {message['text']}
            """
        # openai has a maximum string length it can handle
        instructions = sliceUntilFits(instructions, 128000)
        response = Settings.llm.complete(instructions)
        try:
            result = json.loads(str(response))
            print(f"Was itinerary: {result['was_itinerary']}")
            extraction_code = result['code']
        except Exception as e:
            print("Error parsing response")
            print(e)
    return extraction_code

# this iterates through all emails matching the search
# it prints out the resulting python after each batch
next_token = None
extraction_code = ""
while True:
    # TODO: get the LLM to think of good searches
    messageResults = searcher.search_messages(
        "your flight itinerary", 
        max_results=4, # number of messages in a batch 
        next_token=next_token
    )
    try:
        extraction_code = summarizeMessages(messageResults['messages'],extraction_code)
    except Exception as e:
        print("Error summarizing messages")
        print(e)
    print("==== Current extraction code ====:")
    print(extraction_code)
    if messageResults['next_token']:
        next_token = messageResults['next_token']
    else:
        break
