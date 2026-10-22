import json
from BoundedMemoryAssistant import BoundedMemoryAssistant

def main():
    boundedMemoryAssistant=BoundedMemoryAssistant()
    history_file_path="./history.json"
    boundedMemoryAssistant.import_session(history_file_path)
    while True:
        user_input_str=input("User: ").strip()
        command=user_input_str.lower()
        if command in ["exit","quit"]:
            print("Exiting...")
            break
        elif command in ["inspectmemory","inspect_memory","inspect"]:
            print(json.dumps(boundedMemoryAssistant.inspect_memory(), indent=4))
        elif command=="history":
            try:
                with open(history_file_path, "r") as f:
                    print(f.read())
            except FileNotFoundError:
                print("No history file found.")
        elif command=="delete":
            boundedMemoryAssistant._prune_memory()
        elif command=="":
            continue
        else:
            boundedMemoryAssistant.chat_stream(user_input_str)

if __name__=="__main__":
    main()