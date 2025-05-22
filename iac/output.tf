output "ec2_public_ip" {
  description = "Public IP of the EC2 instance"
  value       = aws_instance.ml_serving_instance.public_ip
}

output "ec2_instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.ml_serving_instance.id
}
