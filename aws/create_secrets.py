"""
Create, update, and delete secrets in AWS Secrets Manager
============================================================
# Summary
This script provides utility functions to manage AWS Secrets Manager secrets using boto3. It allows you to create, 
update, and delete secrets, with error handling for common AWS exceptions. The script can load environment variables 
from a .env file and store them as a secret in AWS Secrets Manager.

# Description of main components:
`get_secrets_manager_client`: Returns a boto3 client for AWS Secrets Manager.
`create_secret`: Creates a new secret with a given name and value. Handles the case where the secret already exists.
`update_secret`: Updates the value of an existing secret.
`delete_secret`: Deletes a secret, with an option to force immediate deletion.
`Example usage`: Loads environment variables from a .env file, serializes them to JSON, and creates a secret in AWS 
Secrets Manager with those values.
"""

import json

import boto3
from botocore.exceptions import ClientError
from dotenv import dotenv_values


def get_secrets_manager_client(region_name="us-east-1"):
    return boto3.client("secretsmanager", region_name=region_name)


# 1. Create a new secret
def create_secret(secret_name, secret_value, region_name="us-east-1"):
    client = get_secrets_manager_client(region_name)
    try:
        response = client.create_secret(
            Name=secret_name,
            SecretString=secret_value,
            Description="Secret for Intranet service account",
        )
        print(f"Secret '{secret_name}' created successfully.")
        return response
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceExistsException":
            print(f"Secret '{secret_name}' already exists.")
        else:
            print(f"Unexpected error: {e}")
        return None


def update_secret(secret_name, secret_value, region_name="us-east-1"):
    client = get_secrets_manager_client(region_name)
    try:
        response = client.put_secret_value(
            SecretId=secret_name, SecretString=secret_value
        )
        print(f"Secret '{secret_name}' updated successfully.")
        return response
    except ClientError as e:
        print(f"Failed to update secret: {e}")
        return None


def delete_secret(
        secret_name, region_name="us-east-1", force_delete_without_recovery=True
):
    client = get_secrets_manager_client(region_name)
    try:
        response = client.delete_secret(
            SecretId=secret_name,
            ForceDeleteWithoutRecovery=force_delete_without_recovery,
        )
        print(f"Secret '{secret_name}' deleted successfully.")
        return response
    except ClientError as e:
        print(f"Failed to delete secret: {e}")
        return None


# Example usage:
_name = "intranet-service-account-secrets"
_value = json.dumps(dotenv_values("../../.env"))

create_secret(_name, _value)
