from src.aws.s3 import s3_client


def test_s3_client_endpoint():
    expected_endpoint = "http://localhost:4566"
    assert s3_client._endpoint.host == expected_endpoint


def test_s3_client_service():
    assert s3_client.meta.service_model.service_name == "s3"
