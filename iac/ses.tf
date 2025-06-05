data "aws_route53_zone" "selected_domain" {
  name         = var.ses_domain
  private_zone = false
}

resource "aws_ses_domain_identity" "domain_identity" {
  domain = var.ses_domain
}

resource "aws_ses_domain_dkim" "domain_dkim" {
  domain     = aws_ses_domain_identity.domain_identity.domain
  depends_on = [aws_ses_domain_identity.domain_identity]
}

resource "aws_ses_receipt_rule_set" "email_receiver_rule_set" {
  rule_set_name = "${var.project_title_lowercase}-email-receiver-ruleset"
}

resource "aws_ses_active_receipt_rule_set" "active_email_receiver_rule_set" {
  rule_set_name = aws_ses_receipt_rule_set.email_receiver_rule_set.rule_set_name
}

resource "aws_ses_receipt_rule" "email_processor_rule" {
  name          = "${var.project_title_lowercase}-email-processor-rule"
  rule_set_name = aws_ses_receipt_rule_set.email_receiver_rule_set.rule_set_name
  recipients    = [var.ses_receiving_email_address]

  enabled = true

  lambda_action {
    function_arn = aws_lambda_function.email_processor_lambda.arn
    position     = 1
  }

  depends_on = [
    aws_lambda_permission.allow_ses_to_invoke_email_processor,
    aws_ses_active_receipt_rule_set.active_email_receiver_rule_set
  ]
}

resource "aws_lambda_permission" "allow_ses_to_invoke_email_processor" {
  statement_id  = "AllowExecutionFromSES"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.email_processor_lambda.function_name
  principal     = "ses.amazonaws.com"
  source_arn    = "arn:aws:ses:${var.aws_account_region}:${var.aws_account_number}:*"
}

resource "aws_route53_record" "ses_domain_verification_record" {
  zone_id    = data.aws_route53_zone.selected_domain.zone_id
  name       = aws_ses_domain_identity.domain_identity.id
  type       = "TXT"
  ttl        = 60
  records    = [aws_ses_domain_identity.domain_identity.verification_token]
  depends_on = [aws_ses_domain_identity.domain_identity]
}

resource "aws_route53_record" "ses_dkim_records" {
  count = 3

  zone_id    = data.aws_route53_zone.selected_domain.zone_id
  name       = "${aws_ses_domain_dkim.domain_dkim.dkim_tokens[count.index]}._domainkey.${var.ses_domain}"
  type       = "CNAME"
  ttl        = 60
  records    = ["${aws_ses_domain_dkim.domain_dkim.dkim_tokens[count.index]}.dkim.amazonses.com"]
  depends_on = [aws_ses_domain_dkim.domain_dkim]
}

resource "aws_route53_record" "ses_receiving_mx_record" {
  zone_id    = data.aws_route53_zone.selected_domain.zone_id
  name       = var.ses_domain
  type       = "MX"
  ttl        = 60
  records    = ["10 inbound-smtp.${var.aws_account_region}.amazonaws.com"]
  depends_on = [aws_ses_receipt_rule_set.email_receiver_rule_set]
}
