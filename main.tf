resource "aws_s3_bucket" "bad_example" {
  bucket = "my-unsecure-bucket"
  acl    = "public-read"   # ❌ insecure
}
