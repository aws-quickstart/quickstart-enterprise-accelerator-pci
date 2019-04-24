#!/bin/bash
set -Eeuox pipefail

STACK_NAME=STACK-NAME-HERE
BUCKET=BUCKET-NAME-HERE
export AWS_DEFAULT_REGION=us-east-1

#aws s3api create-bucket --bucket ${BUCKET} --acl private #--create-bucket-configuration LocationConstraint="$AWS_DEFAULT_REGION"

pushd ../templates

sam build --template iamauthentication.yaml --build-dir iamauthentication #--use-container

sam package \
    --s3-bucket "$BUCKET" \
    --output-template-file packaged-main.template \
    --template-file main.template


sam deploy \
    --stack-name "$STACK_NAME" \
    --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND \
    --template-file packaged-main.template
     #--on-failure DO_NOTHING

popd
