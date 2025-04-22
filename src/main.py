import argparse
import logging

from botocore.exceptions import ClientError

from src.aws.s3 import SERVICE_BUCKET, s3_client
from src.features.llm_chat.client import LLMChatClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main(message: str):
    ensure_bucket_exists()
    chat_client = LLMChatClient(s3_client)
    return chat_client.chat(message)


def ensure_bucket_exists():
    try:
        s3_client.head_bucket(Bucket=SERVICE_BUCKET)
        logger.info(f"Bucket '{SERVICE_BUCKET}' already exists.")
    except ClientError:
        logger.info(f"Creating bucket '{SERVICE_BUCKET}'")
        s3_client.create_bucket(Bucket=SERVICE_BUCKET)


if __name__ == "__main__":
    argparse = argparse.ArgumentParser(description="LLM Chat Client")
    argparse.add_argument(
        "message",
        type=str,
        help="The message to send to the LLM chat client",
    )
    args = argparse.parse_args()
    message = args.message
    logger.info(f"Sending message to LLM chat client: {message}")
    response = main(message)
    logger.info(f"Response from LLM chat client: {response}")
