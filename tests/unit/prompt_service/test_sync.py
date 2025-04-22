from aws.s3 import SERVICE_BUCKET
from features.llm_chat import FEATURE_NAME
from src.prompt_service.sync import main as prompt_sync


def test_sync_uploads_missing_prompts(s3_client):
    original_files = s3_client.list_objects_v2(Bucket=SERVICE_BUCKET, Prefix=FEATURE_NAME)

    prompt_sync(FEATURE_NAME)
    updated_files = s3_client.list_objects_v2(Bucket=SERVICE_BUCKET, Prefix=FEATURE_NAME)
    uploaded_prompts = [obj["Key"] for obj in updated_files.get("Contents", [])]

    assert original_files["KeyCount"] == 0, "Expected no files in the bucket before sync"
    assert sorted(uploaded_prompts) == sorted(
        [
            f"{FEATURE_NAME}/system_prompt.txt",
            f"{FEATURE_NAME}/user_prompt.txt",
        ]
    ), "Expected system and user prompts to be uploaded"


def test_sync_deletes_unused_prompts_by_filename(s3_client):
    s3_client.put_object(
        Bucket=SERVICE_BUCKET, Key=f"{FEATURE_NAME}/unused_system_prompt.txt", Body="Unused system prompt"
    )
    original_files = s3_client.list_objects_v2(Bucket=SERVICE_BUCKET, Prefix=FEATURE_NAME)

    prompt_sync(FEATURE_NAME)
    updated_files = s3_client.list_objects_v2(Bucket=SERVICE_BUCKET, Prefix=FEATURE_NAME)
    uploaded_prompts = [obj["Key"] for obj in updated_files.get("Contents", [])]

    assert original_files["KeyCount"] == 1, "Expected one file in the bucket before sync"
    assert (
        f"{FEATURE_NAME}/unused_system_prompt.txt" not in uploaded_prompts
    ), "Expected unused system prompt to be deleted"


def test_sync_updates_prompt_with_new_content(s3_client):
    old_content = "Old system prompt"
    s3_client.put_object(Bucket=SERVICE_BUCKET, Key=f"{FEATURE_NAME}/system_prompt.txt", Body=old_content)

    prompt_sync(FEATURE_NAME)
    updated_content = s3_client.get_object(Bucket=SERVICE_BUCKET, Key=f"{FEATURE_NAME}/system_prompt.txt")[
        "Body"
    ].read()

    assert updated_content.decode("utf-8") == "A test system prompt.", "Expected system prompt to be updated"
