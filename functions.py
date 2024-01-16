import time
import os
import streamlit as st
from openai import OpenAI
from util import AssistantManager

api_key = os.environ.get('OPENAI_API_KEY')
print(api_key)

#multiple threads code
def main():
    manager = AssistantManager(api_key=api_key)

    # process 1
    manager.create_assistant(
        name="CSV file analyser",
        instructions="You are a tax consultant who can explain tax issues to laypeople in simple language.",
        tools=[{"type": "code_interpreter"}]
    )

    # process 2
    manager.create_thread()

    # file to upload
    file = manager.client.files.create(
        file=open("/Users/pku/Code/forium-ai/supporting_files/CLEAN_Beispielbescheid_39241071.csv", "rb"),
        purpose='assistants'
    )
    file_id = file.id

    # process 3
    manager.add_message_to_thread(role="user",
                                  # content="Ich habe eine csv-Datei beigefügt. Gibt es in den Zahlen Hinweise auf Abweichungen zwischen dem Steuerbescheid (repräsentiert durch 'Bescheidwert') und den Angaben in der Steuererklärung (repräsentiert durch 'forium-Wert')? Beziehe nach dem Vergleich der Werte den Text in der Zeile 'Erläuterung zur Festsetzung' mit ein! Können Sie mir 5 wichtige Punkte nennen?",
                                  content="Ich habe eine Datei beigefügt, die die Werte des Steuerbescheids ('Bescheidwert') und der Steuererklärung ('forium-Wert') enthält. Können Sie mir bitte 3 wichtige Punkte nennen, die auf Abweichungen zwischen den beiden Werten hindeuten? Beziehen Sie dabei den Text in der Spalte 'Erläuterung zur Festsetzung' mit ein und erläutern Sie kurz, warum diese Abweichungen relevant sind.",
                                  # content="How many columns in the table?, name the columns in the table",
                                  file_ids=[file.id])
    # manager.add_message_to_thread(role="user",
    #                               content="Können Sie mir 5 wichtige Punkte aus den von Ihnen gegebenen Antworten nennen?"
    #                               )
    # process 4
    manager.run_assistant(instructions="please address the user as pramod")

    manager.wait_for_completion()

if __name__== '__main__':
    main()