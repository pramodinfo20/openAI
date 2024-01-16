import os

import streamlit as st
import numpy as np
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent

# chat_model = ChatOpenAI(temperature=0, model_name="gpt-4")
key = os.environ.get('OPENAI_API_KEY')
print(key)
st.title('Hinweise auf Abweichungen')
bescheid = st.file_uploader(label='Laden Sie hier einen Bescheid als .csv hoch', type=['csv'])
if bescheid:
    agent = create_csv_agent(
        ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo"),
        bescheid,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True
    )

    #try:
     #   antwort = agent.run(
      #      'Gibt es Hinweise auf Abweichungen zwischen dem Steuerbescheid (repräsentiert durch "Bescheidwert") und den Angaben in der Steuererklärung (repräsentiert durch "forium-Wert")? ')
       # st.write(antwort)
    #except ValueError as e:
    #    st.error(f"An error occurred: {str(e)}")
    antwort = agent.run("")
    #antwort = agent.run('Gibt es Hinweise auf Abweichungen zwischen dem Steuerbescheid (repräsentiert durch "Bescheidwert") und den Angaben in der Steuererklärung (repräsentiert durch "forium-Wert")? ')
    st.write(antwort)
    # frage = st.text_input('Frage')
    # if frage:

#     frage = 'Frage: '
#     if frage:
#         template = ChatPromptTemplate.from_messages([
#             ("system", "Du bist ein Steuerberater, der Laien in einfacher Sprache steuerfachliche Sachverhalte erklären kann."),
#             ("human", "Hier ist ein Bescheid über Einkommensteuer"),
#             ("human", "Context: " + str(result)),
#             ("human", "Gibt es Hinweise auf Unterschiede?"),
#         ])
#         llm_response = chat_model(template.format_messages(frage=frage))
#         st.write(llm_response.content)
