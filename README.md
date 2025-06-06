# 💧 Watch Drop: Your Email Driven TV & Movie Notification Service

Simple Email service to subscribe and keep track of shows/movies when a new
episode is available to stream.

---

## 🚀 Overview

Watch Drop is a serverless, personalized notification service that keeps you
updated on your favorite TV shows and movies. No more missing new episodes or
releases

Once subscribed to a title, Watch Drop automatically creates you an account and
checks for new content daily, then sends you an email alert when a new episode
or movie becomes available to stream.

This project is built leveraging the power of AWS serverless services for
efficiency and scalability, integrating with The Movie Database (TMDB) for
comprehensive content information.

---

## 🧠 How It Works

1. Research what show(s) you want to get alerts for
   [TMDB](https://developer.themoviedb.org/reference/tv-series-episode-groups)

2. Copy the url

3. Send an email to `subscribe@watchdrop.org` with the heading
   `add https://www.themoviedb.org/tv/83867-andor`

4. You are now subscribed and if a new episode airs, you will receive an email
   alert to the address you sent from

5. To unsubscribe from a show, simply send an email with `remove` instead of
   `add`

---

## Tech Stack

![Diagram](https://github.com/user-attachments/assets/0b5e7399-5cfe-4f53-8819-27a7ac141d08)

- **Route 53** to provide Domain name, TXT, MX and 3 CNAME record
- **SES Simple Email Service** to Receive and Send emails to AWS
- **Lambda** 3 Serverless functions, email_processor, tmdb_scanner, ses-sender
- **IAM** For Lambda and SES role utilization, least privilege
- **Secrets Manager** to store credentials for TMDB API
- **DynamoDB** Store records of users with their movie/show preferences - Also
  state-lock
- **S3** State-lock storage
- **Python** For writing Lambda functions
- **Terraform** All resources orchestrated using Hashicorp Terraform IaC

---

## 🚀 Do It Yourself

Watch Drop is built with an entirely **Infrastructure As Code** approach so with
a few simple steps you can have your own custom version up and running in your
own AWS account

Note: You will need to buy a domain costing about $14usd+ per year

### Prerequisites

1. Download and install [Git](https://github.com/git-guides/install-git)

2. Setup an
   [AWS account](https://docs.aws.amazon.com/accounts/latest/reference/manage-acct-creating.html)

3. Download and install the
   [AWS Command Line Interface (CLI)](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

4. Setup
   [AWS Credentials on your machine](https://docs.aws.amazon.com/cli/v1/userguide/cli-chap-configure.html)

5. Download and install
   [Terraform](https://developer.hashicorp.com/terraform/install)

6. Setup a [TMDB Account](https://www.themoviedb.org/signup)

7. Apply for TMDB [API Key](https://www.themoviedb.org/settings/api)

Optional - If you want to run code locally:

- Download and install [Python 3.9 or above](https://www.python.org/downloads/)
- Install [pip](https://pip.pypa.io/en/stable/installation/)

### Initialization

Open your terminal and clone this repository

```
gh repo clone OperationFman/Watch-Drop
```

Rename if desired and navigate to the `/iac` directory e.g:

Create a new file called `terraform.tfvars`

Open the file then paste this starter configuration, in following steps we will
_replace_ this with your own data. Save the file

```
project_title                  = "WatchDrop"
project_title_lowercase        = "watch-drop"
ses_domain                     = "watchdrop.org"
ses_receiving_email_address    = "subscribe@watchdrop.org"
owner                          = "Franklin Moon"
aws_account_number             = "123456781234"
aws_account_region             = "ap-southeast-2"
tmdb_api_key_value             = "eyBLAHBLAHBLAH"
schedule_cron                  = "cron(0 8 * * ? *)"
environment                    = "Production"
```

### Configuration

#### Update basic variables

Inside `terraform.tfvars` update these values:

- project_title
- project_title_lowercase
- owner (you)
- aws_account_number (Found in the top right of the AWS console)
- aws_account_region (Wherever you choose, be consistent from now on)

Optional: You can leave the Production and Cron as-is if you are happy with them

#### Get TMDB API Key

Open TMDB API, if your application has been approved, generate a key
[here](https://www.themoviedb.org/settings/api)

Copy and paste the key in `terraform.tfvars` `tmdb_api_key_value` field:

```
tmdb_api_key_value = "YOURKEYGOESHERE"
```

#### Buy a domain

Log in to your new AWS account and open 'Route 53'

On the left side panel, select 'Registered domains' then click 'Register
domains'

Search for a new domain name you'd like to use and select the option you want at
a reasonable price

Complete the purchase

Add the domain name to your `terraform.tfvars` file, e.g

```
ses_domain                  = "yournewdomain.com"
ses_receiving_email_address = "subscribe@yournewdomain.com"
```

#### Setup State-lock

In AWS Console, open S3

Create a new bucket with name
`<YOUR-PROJECT-NAME>-terraform-state-<YOUR-AWS-ACCOUNT-ID>`

Keep all settings as default, create

#### Create DynamoDB State-lock

In the AWS Console, open DynamoDB and make sure you're in the region you want to
use going forward (Top right corner) e.g `ap-southeast-2`

Click Create Table:

- Name `<YOUR-PROJECT-NAME>-terraform-locks`
- Partition Key `LockID` (String)

Open `provider.tf` in the `/iac` folder and update the bucket, key and dynamodb
table values to match what you just created

```
  backend "s3" {
    bucket         = "<YOUR-PROJECT-NAME>-terraform-state-<YOUR-AWS-ACCOUNT-ID>"
    key            = "<YOUR-PROJECT-NAME-IN-LOWERCASE>/terraform.tfstate"
    region         = "ap-southeast-2"
    dynamodb_table = "<YOUR-PROJECT-NAME>-terraform-locks"
    encrypt        = true
  }
```

Note: Make sure the start of the `key` value matches what you put in
terraform.tfvars `project_title_lowercase`

### Running IaC

Note: Before running the IaC, ensure your new Route 53 domain is active. Open
Route 53 in AWS S3, if the domain says inactive, keep waiting for DNS
propagation (should take several minutes but up-to 24 hours)

In your terminal from the `/iac` folder:

```
terraform init
```

```
terraform plan
```

Note what new cloud resources will be created

```
terraform apply
```

This command will provision all your core AWS resources: DynamoDB table, IAM
roles/policies, Lambda functions and crucially, it will automatically configure
your SES domain verification, DKIM, and MX records directly in Route 53

### Exit Sandbox Mode

Note, by default your SES account will be in Sandbox mode which means you can
only send/receive emails to verified email addresses (You can add more verified
email address in the AWS SES Console under 'identities')

In your AWS Console, Open AWS SES (Simple Email Service)

Open the 'get set up' menu on the left side

Click 'Request production access' and fill out the form

### Testing

Send an email to the @subscribe address, e.g

Receiver:

```
subscribe@<your-project-name>.com
```

Email header:

```
add https://www.themoviedb.org/tv/83867-andor
```

Note the new show in the DynamoDB Subscription table in AWS

You should now receive an alert at UTC+8

---

## ✨ Planned Enhancements

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
