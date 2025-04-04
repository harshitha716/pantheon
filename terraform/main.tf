provider "aws" {
  region = var.AWS_REGION
}

resource "aws_instance" "example" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
}

output "instance_id" {
  value = aws_instance.example.id
}

