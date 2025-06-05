# 💧 Watch Drop: Your Email Driven TV & Movie Notification Service

Simple AWS SES service to keep track of shows & movies with email when a new
episode is available to stream.

---

## 🚀 Overview

Watch Drop is a serverless, personalized notification service that keeps you
updated on your favorite TV shows and movies. No more missing new episodes or
releases Once subscribed to a title, Watch Drop automatically creates you an
account and checks for new content daily, then sends you an email alert when a
new episode or movie becomes available to stream.

This project is built leveraging the power of AWS serverless services for
efficiency and scalability, integrating with The Movie Database (TMDB) for
comprehensive content information.

---

## ✨ Features (MVP)

The initial MVP focuses on core functionality to get notifications delivered
reliably.

- **Automated Content Monitoring:** Daily checks for new episodes of subscribed
  TV shows and new releases of subscribed movies.
- **Personalized Email Notifications:** Timely email alerts delivered directly
  to your inbox via AWS SES when new content "drops."
- **Simple Subscription Management:** (Experimental for MVP) Add or remove TV
  shows/movies from your tracking list by sending an email with specific
  commands in the subject line.

---

## 🧠 How It Works

Watch Drop is built entirely on a serverless architecture, ensuring
cost-efficiency and automatic scaling.

### Key Components:

- **AWS Lambda (Python):** The backbone of the service, running all the business
  logic.
  - **Lambda #1 (Email Processor):** Triggered by incoming emails, parses
    commands from the subject line (`add <url>`, `remove <url>`), and updates
    DynamoDB.
  - **Lambda #2 (TMDB Scanner):** Triggered daily by EventBridge, iterates
    through subscribed titles in DynamoDB, queries the TMDB API for the latest
    status, and identifies new content.
  - **Lambda #3 (SES Sender):** Invoked by Lambda #2 (or directly by other
    Lambda functions), responsible for formatting and sending email
    notifications via SES.
- **Amazon DynamoDB:** A fast and flexible NoSQL database storing user
  subscriptions (email, TMDB ID, content type, last known state).
- **Amazon SES (Simple Email Service):** Used for sending email notifications to
  users and for receiving inbound emails to manage subscriptions.
- **Amazon EventBridge:** Schedules the daily execution of Lambda #2 to perform
  content checks.
- **The Movie Database (TMDB) API:** Provides comprehensive data about movies,
  TV shows, and their episodes.

---

## ✨ Nice-to-Haves (Future Enhancements)

These features are planned

- **User-Friendly Unsubscribe Button:** Add a pre-configured "remove"
  link/button directly within notification emails that automatically populates a
  new email for Lambda #1.
- **Confirmation Emails:** Send confirmation emails (via Lambda #3) after
  successful subscription additions or removals from Lambda #1.
- **Email Domain**
  - Custom email like foo@watchdrop.com instead of a gmail one
- **Email Design:**
  - Integrate the "Watch Drop" logo into notification emails.
  - Include relevant show banner/cover art.
  - Develop fancy HTML email styling for a better user experience.
- **Weekly Roundup Digest:** Option for users to receive a weekly summary email
  of all new drops, instead of individual notifications.
- **Enhanced Rate Limiting / Security:** Implement more sophisticated rate
  limiting strategies and security measures beyond basic IAM.
- **Setup MAIL FROM**
- **S3 for Email Content Storage:** Transition from relying solely on email
  subject lines to storing full email content in S3 for more robust parsing of
  commands from the email body and handling attachments.

---

## 🔗 Links

- **TMDB API Documentation (TV Series Episodes):**
  [https://developer.themoviedb.org/reference/tv-series-episode-groups](https://developer.themoviedb.org/reference/tv-series-episode-groups)

---

## Scaling Concerns

- API rate limit - Currently a maximum of 50 requests per second
- DynamoDB scan - Currently a maximum of 7000 records before pagination is
  available

---

## 🚀 Getting Started (Developer Info)

To get Watch Drop up and running locally and deploy to your AWS account:


- Setup Terraform, AWS CLI and Python3
- Buy a domain in Route53
- Setup Statelock in S3 and DynamoDB - Clickops
- Update all values in /iac/variables and /iac/provider.tf
- Get API key from TMDB and add to terraform.tfvars
- Run iac and take outputs to setup TXT for domain
