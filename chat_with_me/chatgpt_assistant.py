from openai import OpenAI
from keys import OPENAI_TOKEN, OPENAI_ASSISTANT_ID
from configs import SYSTEM_PROMPT

import re
from logger import setup_logger
logger = setup_logger()

class GPT_assistant:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_TOKEN)
        # create a thread ID to keep the context
        #self.thread_id = self.client.beta.threads.create().id 
        
    def create_new_thread(self) -> str:
        return self.client.beta.threads.create().id 
    
    def set_thread(self, thread_id: str) -> None:
        self.thread_id = thread_id
    
    def remove_citations(self, text: str) -> str:
        # Regular expression to match citations like " "
        citation_pattern = re.compile(r"【\d+:\d+†\w+】")
        # Substitute the matched patterns with an empty string
        cleaned_text = citation_pattern.sub('', text)
        return cleaned_text.strip()
    
    def ask_assistant(self, question) -> str:
        # Create a new message in the existing thread
        message = self.client.beta.threads.messages.create(
            thread_id=self.thread_id,
            role="user",
            content=question
        )
        
        # Run the assistant with specific instructions
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=self.thread_id,
            assistant_id=OPENAI_ASSISTANT_ID,
            instructions=SYSTEM_PROMPT
        )
        
        # Check if the run is completed
        if run.status == 'completed': 
            # List messages from the thread
            messages = self.client.beta.threads.messages.list(
                thread_id=self.thread_id
            )
            try:
                return self.remove_citations(text=str(messages.data[0].content[0].text.value))
            except Exception as e:
                logger.error(f"\nError: {e}")
                logger.error("message:" + messages.data[0].content[0].text.value)
                logger.error("type:"+str(type(messages.data[0].content[0].text.value)))
        else:
            return f"\n\nERROR:\n\n{run.status}"

    
# Example usage
if __name__ == '__main__':
    assistant = GPT_assistant()
    thread = assistant.create_new_thread()
    assistant.set_thread(thread_id=thread)
    
    question: str = ''
    while question != 'bye':
        question = input("You:")
        if question == 'bye': 
            break
        
        response = assistant.ask_assistant(question)
        print(response)
