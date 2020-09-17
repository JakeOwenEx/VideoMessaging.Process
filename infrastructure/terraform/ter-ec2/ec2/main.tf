data "aws_ami" "al2" {
    most_recent = true
    owners      = ["amazon"]
    filter {
        name   = "owner-alias"
        values = ["amazon"]
    }


    filter {
        name   = "name"
        values = ["amzn2-ami-hvm*"]
    }
}

resource "aws_security_group" "allow_ssh" {
  name        = "allow_ssh"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "allow_ssh"
  }
}

resource "aws_instance" "web" {
    ami           = "ami-0346ee471bb2c892a"
    instance_type = "c6g.xlarge"
    key_name      = "video-messaging-processing-kp"
    security_groups = [aws_security_group.allow_ssh.name]
    tags = {
        Name = "processor-ec2"
    }
}