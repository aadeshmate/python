from BoundedMemoryAssistant import BoundedMemoryAssistant

boundedMemoryAssistant=BoundedMemoryAssistant()
history_file_path="./history.json"
boundedMemoryAssistant.import_session(history_file_path)
while True:
    user_input_str=input("User: ")
    if user_input_str.lower() in ["exit","quit"]:
        print("Exiting...")
        break

    boundedMemoryAssistant.chat_stream(user_input_str)
