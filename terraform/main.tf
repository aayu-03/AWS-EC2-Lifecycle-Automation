provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "demo" {
  ami           = "ami-0152204c1a187337c"
  instance_type = "t3.micro"
  count         = 2

  tags = { 
    Name = "app-linux-${count.index}" 
  }
}
