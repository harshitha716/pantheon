terraform {
  backend "s3" {
    bucket = "zamp-dev-sg-helm-repository"
    key    = "terraform.tfstate.txt"
    region = "us-east-2"
    encrypt = true
  }
}
