#!/usr/bin/env bash

IMAGE_URI="mikomel/demo:latest"

docker build -t ${IMAGE_URI} -f docker/pytorch.Dockerfile .
