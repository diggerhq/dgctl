from dotenv import dotenv_values

from dgctl.aws import get_caller_identity, bucket_exists, bucket_create


class InitCommand:
    backend_tf = "backend.tf"

    def __init__(self, region):
        self.region = region
        self.config = dotenv_values(".digger")

        if not self.config:
            raise RuntimeError("File .digger not found")

        self.environment_id = self.config.get("ENVIRONMENT_ID")
        if not self.environment_id:
            raise RuntimeError("Missing ENVIRONMENT_ID in .digger file")

        try:
            self.account = get_caller_identity()
        except:
            raise RuntimeError(
                "Failed to get AWS account ID. Do you have aws cli installed?"
            )

        self.account_id = self.account["Account"]
        self.bucket_name = f"digger-{self.account_id}"

        try:
            self.create_bucket_if_needed()
        except:
            raise RuntimeError("Failed to create bucket")

        try:
            self.dump_backend_tf()
        except:
            raise RuntimeError("Failed to dump backend file")

    def create_bucket_if_needed(self):
        if bucket_exists(self.bucket_name):
            return

        bucket_create(self.bucket_name)

    def dump_backend_tf(self):
        with open(self.backend_tf, "w") as f:
            f.write(
                f"""
terraform {{
  backend "s3" {{
    bucket  = "digger-{self.account_id}"
    encrypt = true
    key     = "digger/{self.environment_id}/terraform.tfstate"
    region  = "{self.region}"
  }}
}}
"""
            )

        print(f"Well done! File {self.backend_tf} was saved.")
