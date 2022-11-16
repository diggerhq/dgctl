import json

from dgctl.utils import popen_to_object


def get_caller_identity():
    ret_code, caller_identity = popen_to_object(
        ["aws", "sts", "get-caller-identity"], json.loads
    )

    return caller_identity


def bucket_exists(bucket_name):
    """
    Return True/False whether bucket exists or not.
    """
    ret_code, _ = popen_to_object(
        ["aws", "s3api", "head-bucket", "--bucket", bucket_name], str
    )

    return ret_code == 0


def bucket_create(bucket_name):
    """
    Create bucket. Raise error if it was unsuccessful>
    """
    ret_code, create_bucket = popen_to_object(
        [
            "aws",
            "s3api",
            "create-bucket",
            "--bucket",
            bucket_name,
        ],
        str,
    )

    if ret_code != 0:
        raise RuntimeError(create_bucket)
