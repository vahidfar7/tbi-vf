resource "aws_instance" "ml_serving_instance" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = "t3.large"
  subnet_id                   = data.aws_subnets.default_subnets.ids[0]
  vpc_security_group_ids      = [aws_security_group.ml_serving_sg.id]
  associate_public_ip_address = true
  iam_instance_profile        = aws_iam_instance_profile.ec2_instance_profile.name

  tags = {
    Name = "ml-serving-app"
  }

  user_data = <<-EOF
    #!/bin/bash
    apt-get update -y
    apt-get install -y docker.io awscli

    systemctl start docker
    systemctl enable docker

    aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin <your-account-id>.dkr.ecr.eu-west-2.amazonaws.com
    docker pull <your-account-id>.dkr.ecr.eu-west-2.amazonaws.com/ml-serving-app:latest
    docker run -d -p 80:8000 <your-account-id>.dkr.ecr.eu-west-2.amazonaws.com/ml-serving-app:latest
  EOF
}
