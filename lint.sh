#!/bin/bash

echo "使用 pylava 检查代码..."
pylava src --skip '*/tests/*,*/configs/*,*/aiocqlengine/models.py' --async

echo "使用 yapf 格式化代码..."
yapf -ipr src

echo "使用 isort 格式化代码..."
isort -rc -j 10 src
