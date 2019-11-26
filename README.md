# quickstart-compliance-pci
## Standardized Architecture for PCI DSS on the AWS Cloud

This Quick Start deploys a standardized environment that helps organizations with workloads that fall in scope for Payment Card Industry (PCI) Data Security Standard (DSS) compliance.

The Quick Start will deploy a standard three-tier web architecture using multiple VPCs.

![Architecture](https://d0.awsstatic.com/partner-network/QuickStart/datasheets/pci-on-aws-architecture.png)

For architectural details, best practices, step-by-step instructions, and customization options, see the 
[deployment guide](https://fwd.aws/zmYVY).

To post feedback, submit feature ideas, or report bugs, use the **Issues** section of this GitHub repo.
If you'd like to submit code for this Quick Start, please review the [AWS Quick Start Contributor's Kit](https://aws-quickstart.github.io/). 

Be sure to create a AWS KMS key administrator role in order to manage the AWS Key Management Service CMK. Be sure that the key policy that you create allows the current user to [administer the CMK](https://aws.amazon.com/premiumsupport/knowledge-center/update-key-policy-future/).

For example, create a role named 'KeyAdministratorRole' with the following IAM Policy.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "kms:Create*",
                "kms:Describe*",
                "kms:Enable*",
                "kms:List*",
                "kms:Put*",
                "kms:Update*",
                "kms:Revoke*",
                "kms:Disable*",
                "kms:Get*",
                "kms:Delete*",
                "kms:ScheduleKeyDeletion",
                "kms:CancelKeyDeletion",
                "kms:TagResource",
                "kms:UntagResource"
            ],
            "Resource": "*",
            "Effect": "Allow"
        }
    ]
}
```
