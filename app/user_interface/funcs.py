import json
import os

import requests
import streamlit as st
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

from cyclical_encoding_new_inputs import extract_cyclical_features

scoring_uri = ""
headers = {}


def bind_socket():
    # Load configuration from environment variables

    subscription_id = os.environ["SUBSCRIPTION_ID"]
    resource_group = os.environ["RESOURCE_GROUP"]
    workspace_name = os.environ["WORKSPACE_NAME"]
    score = os.eviron["scoring_uri"]
    key = os.eviron["KEY"]
    global scoring_uri
    scoring_uri = score
    global headers
    headers = {"Authorization": ("Bearer " + key)}
    # return scoring_uri, headers


def get_response(in_data):
    # Display the selected dates and predicted rainfall
    input_encoded = extract_cyclical_features(in_data)
    input_dict = {"input_data": input_encoded.tolist()}

    # Send the POST request
    response = requests.post(scoring_uri, json=input_dict, headers=headers).text
    out = json.loads(response)
    return out


def set_page_confic():
    st.set_page_config(
        page_title="Deliverable App",
        page_icon="images/Deliverable_logo.png",
    )
