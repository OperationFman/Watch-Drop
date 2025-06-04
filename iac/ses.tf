resource "aws_ses_domain_identity" "domain_identity" {
  domain = var.ses_domain
}

resource "aws_ses_domain_dkim" "domain_dkim" {
  domain = aws_ses_domain_identity.domain_identity.domain

  depends_on = [aws_ses_domain_identity.domain_identity]
}

resource "aws_ses_receipt_rule_set" "email_receiver_rule_set" {
  rule_set_name = "${var.project_title_lowercase}-email-receiver-ruleset"

}

resource "aws_ses_receipt_rule" "email_processor_rule" {
  name          = "${var.project_title_lowercase}-email-processor-rule"
  rule_set_name = aws_ses_receipt_rule_set.email_receiver_rule_set.rule_set_name
  recipients    = [var.ses_receiving_email_address]

  lambda_action {
    function_arn = aws_lambda_function.email_processor_lambda.arn
    position     = 1
  }

  depends_on = [aws_lambda_permission.allow_ses_to_invoke_email_processor]

}

resource "aws_lambda_permission" "allow_ses_to_invoke_email_processor" {
  statement_id  = "AllowExecutionFromSES"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.email_processor_lambda.function_name
  principal     = "ses.amazonaws.com"
  source_arn    = "arn:aws:ses:${var.aws_account_region}:${var.aws_account_number}:*"
}

output "ses_domain_verification_txt_record_name" {
  description = "DNS name for TXT record"
  value       = "_amazonses.${var.ses_domain}"
}
output "ses_domain_verification_txt_record_value" {
  description = "DNS record value for TXT record"
  value       = aws_ses_domain_identity.domain_identity.verification_token
}

output "ses_dkim_cname_records" {
  description = "List of CNAMEs for SES DKIM authentication"
  value       = aws_ses_domain_dkim.domain_dkim.dkim_tokens
}

output "ses_receiving_mx_record_name" {
  description = "DNS for MX record"
  value       = var.ses_domain
}
output "ses_receiving_mx_record_value" {
  description = "DNS record value for MX record"
  value       = "10 inbound-smtp.${var.aws_account_region}.amazonaws.com"
}
