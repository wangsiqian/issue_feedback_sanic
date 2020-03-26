#!/bin/bash

echo "使用 pylava 检查代码..."
pylava --skip '*/tests/*,*/configs/*,*/aiocqlengine/models.py'

echo "使用 yapf 格式化代码..."
yapf -ir . | (! grep '.')

echo "使用 isort 格式化代码..."
isort -rc .
