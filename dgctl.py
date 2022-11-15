from glob import glob
import json
import re

import click
from utils import popen_to_object

RE_BUNDLE_ID = re.compile(r"environment-(.*)-\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}")
REGION = "us-east-2"


def get_bundle_id():
    dirs = glob("environment-*", recursive=False)
    assert len(dirs) == 1

    r = re.match(RE_BUNDLE_ID, dirs[0])
    return r.groups()[0]


@click.group()
def cli():
    pass


@click.command()
def init():
    # 1/4 Get AWS account ID
    ret_code, caller_identity = popen_to_object(
        ["aws", "sts", "get-caller-identity"], json.loads
    )

    account_id = caller_identity["Account"]

    # 2/4 Check if digger_{aws_account_id} bucket exists
    ret_code, head_bucket = popen_to_object(
        ["aws", "s3api", "head-bucket", "--bucket", f"digger-{account_id}"], str
    )

    if ret_code != 0:
        # 3/4 Create digger_{aws_account_id} bucket if it doesn't exist
        ret_code, create_bucket = popen_to_object(
            [
                "aws",
                "s3api",
                "create-bucket",
                "--bucket",
                f"digger-{account_id}",
                "--region",
                REGION,
            ],
            json.loads,
        )

        print("create_bucket", create_bucket)

    # 4/4 Get bundle based on local directory environment-*
    # TODO: local or current ?
    bundle_id = get_bundle_id()

    with open("backend.tf", "w") as f:
        f.write(
            f"""
terraform {{
  backend "s3" {{
    bucket  = "digger-{account_id}"
    encrypt = true
    key     = "digger/{bundle_id}/terraform.tfstate"
    region  = "{REGION}"
  }}
}}
"""
        )


cli.add_command(init)

if __name__ == "__main__":
    cli()
