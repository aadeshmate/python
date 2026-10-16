from ollama import Client
from config import MODEL_NAME,OLLAMA_HOST,DEFAULT_SYSTEM_PROMPT,DEFAULT_TEMPERATURE
import json

class BoundedMemoryAssistant:
    def __init__(self,max_turns=5):
        self.client=Client(OLLAMA_HOST)
        self.max_turns=max_turns
        #set guardrails
        self.history=[{"role":"system","content":DEFAULT_SYSTEM_PROMPT}]
        self._prune_memory()

    def _prune_memory(self):
       #"""keeps the last masx_turns of conversaiton"""
       if(len(self.history)>self.max_turns*2+1):
           #remove the oldest user and assistant messages while keeping the system prompt
           del self.history[1:3]

    
    def add_message(self,role:str,content:str):
        self.history.append({"role":role,"content":content})
        self._prune_memory()

    def export_session(self,filepath:str):
       #i want to add data in json each time i run the code
        try:
            with open(filepath,"w") as f:
                json.dump(self.history,f,indent=4)
        except Exception as e:
            print(f"Error dumping memory: {e}")
           
    def import_session(self,filepath:str):
        try:
            with open(filepath,"r") as f:
                self.history=json.load(f)

            self._prune_memory()  # Ensure memory is pruned after loading
        except FileNotFoundError:
            print("No previous memory found. Starting fresh.")
        except Exception as e:
            print(f"Error loading memory: {e}") 
           
    def chat_stream(self,user_input_str):
        self.add_message("user",user_input_str)
        response=""
        try:
            stream=self.client.chat(
                model=MODEL_NAME,
                messages=self.history,
                stream=True,
                options={"temperature":DEFAULT_TEMPERATURE}
            )
            print("AI: ",end='')
            for chunk in stream:
                token=chunk['message']['content']
                print(token,end='',flush=True)
                response+=token
            
            print('\n')
            self.add_message("assistant",response)
            self._prune_memory()  # Ensure memory is pruned after adding the assistant's response
            self.export_session("./history.json")  # Save memory after each interaction
        except Exception as e:
            print(f"Error during chat: {e}")
            self.history.pop()  # Rollback to last user input on failure
    

        
       