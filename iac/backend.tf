terraform {
  backend "s3" {
    bucket         = "vahid-mlapp-tfstate"
    key            = "mlapp/terraform.tfstate"
    region         = "eu-west-2"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
