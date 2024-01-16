from openai import OpenAI
import time
# from dotenv import load_dotenv
import os

# load_dotenv()

class AssistantManager:
    def __init__(self, api_key, organisation_id="org-8rXJdgZzKzP9teA4DCw0j5Gn", model="gpt-4-1106-preview"):
        self.client = OpenAI(api_key=api_key, organization=organisation_id)
        self.model = model
        self.assistant = None
        self.thread = None
        self.run = None

    def create_assistant(self, name, instructions, tools):
        self.assistant = self.client.beta.assistants.create(
            name=name,
            instructions=instructions,
            tools=tools,
            model=self.model
        )

    def create_thread(self):
        self.thread = self.client.beta.threads.create()

    def add_message_to_thread(self, role, content, file_ids=None):
        if file_ids is None:
            file_ids = []

        self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role=role,
            content=content,
            file_ids=file_ids
        )

    def run_assistant(self, instructions):
        self.run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
            instructions=instructions
        )

    def wait_for_completion(self):
        while True:
            time.sleep(5)
            run_status = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id=self.run.id
            )
            print(run_status.model_dump_json(indent=4))

            if run_status.status == 'completed':
                self.process_messages()
                word_count = len(self.process_messages().split())
                print("Number of words in the sentence:", word_count)
                break
            else:
                print("Waiting for the Assistant to process...")

    def process_messages(self):
        messages = self.client.beta.threads.messages.list(thread_id=self.thread.id)

        for msg in messages.data:
            role = msg.role
            content = msg.content[0].text.value
            print(f"{role.capitalize()}: {content}")


def main():
    api_key = os.getenv("api_key")
    organisation_id = "org-8rXJdgZzKzP9teA4DCw0j5Gn"
    manager = AssistantManager(api_key)

    manager.create_assistant(
        name="Math Tutor",
        instructions="You are a personal math tutor. Write and run code to answer math questions.",
        tools=[{"type": "code_interpreter"}]
    )
    manager.create_thread()
    manager.add_message_to_thread(role="user",
                                  content="I need to solve the equation `3x^2 + 11x = 14`. Can you help me?")
    manager.run_assistant(instructions="Please address the user as elbowai, the user has a premium account")
    manager.wait_for_completion()


if __name__ == '__main__':
    main()