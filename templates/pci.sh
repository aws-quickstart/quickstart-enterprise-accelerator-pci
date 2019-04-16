#!/bin/bash
set -Eeuox pipefail

STACK_NAME=pci-quickstart-2
BUCKET=jjjoy-pci-quickstart-5
export AWS_DEFAULT_REGION=us-west-2

#aws s3api create-bucket --bucket ${BUCKET} --acl private --create-bucket-configuration LocationConstraint="$AWS_DEFAULT_REGION"

sam build --template cfn.iamauthentication.yaml #--use-container

sam package \
    --s3-bucket "$BUCKET" \
    --output-template-file packaged-main.template \
    --template-file main.template


sam deploy \
    --stack-name "$STACK_NAME" \
    --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND \
    --template-file packaged-main.template
     #--on-failure DO_NOTHING

