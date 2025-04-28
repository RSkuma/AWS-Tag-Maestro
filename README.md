# AWS-Tag-Maestro Background
Management Tool for shared resources in AWS, for cases where multiple projects are restricted to a single AWS account

AWS Tag Maestro is a tool I designed for HackForLA, a non-profit, which has given me permisson to replicate on my personal account to apply for a MLH fellowship.

Maestro aims to provide management and monitoring for software engineering projects hosted on a singular AWS account.
This is infrastructure setup is somewhat rare, as AWS recommends each project have a dedicated account managed by an AWS organization.

However this is not always ideal, either due to finanical contraints or factors making the management of many AWS accounts unrealistic.

# Setup
`aws configure` must be used to configure AWS credentials

Once that is complete the tool can be access by running `maestro.py`
