terraform {
  backend "s3" {
    bucket = "openproject-bucket1"  # Replace with your unique S3 bucket name
    key    = "path/use-case-4/my-bucket2/statefile/terraform.tfstate"  # Path inside the bucket to store the state
    region = "us-east-1"  # Replace with your desired AWS region
    encrypt = true  # Enable encryption of the state file
   
  }
}
