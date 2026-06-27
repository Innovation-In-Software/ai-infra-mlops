#!/bin/bash
# Classroom environment defaults for Labs 2+ (source from lab0 or add to /etc/profile.d/)
export LAB_NUM_RECORDS="${LAB_NUM_RECORDS:-1000}"
export LAB_USE_COMPREHEND="${LAB_USE_COMPREHEND:-0}"
export AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-west-2}"
echo "MLOps lab env: LAB_NUM_RECORDS=$LAB_NUM_RECORDS LAB_USE_COMPREHEND=$LAB_USE_COMPREHEND region=$AWS_DEFAULT_REGION"
