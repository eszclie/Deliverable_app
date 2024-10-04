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

    # Create Azure ML client
    ml_client = MLClient(
        credential=DefaultAzureCredential(),
        subscription_id=subscription_id,
        resource_group_name=resource_group,
        workspace_name=workspace_name,
    )
    print("hiereeeeeeeeeeeeeeeeeeeeeeeeee")
    # Set endpoint name
    endpoint_name = "endpoint-xgb-model"

    # Get the endpoint credentials
    endpoint = ml_client.online_endpoints.get(endpoint_name)
    print(endpoint)
    global scoring_uri
    scoring_uri = endpoint.scoring_uri
    keys = ml_client.online_endpoints.get_keys(name=endpoint_name)
    key = keys.primary_key
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
