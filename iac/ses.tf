resource "aws_ses_email_identity" "watch_drop_sender_email" {
  email = var.ses_email

}

# resource "aws_ses_domain_identity" "watch_drop_domain_identity" {
#   domain = var.ses_domain
# }

# output "ses_domain_verification_token" {
#   value = aws_ses_domain_identity.watch_drop_domain_identity.verification_token
# }
