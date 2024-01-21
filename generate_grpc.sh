#!/usr/bin/env bash

# Скачиваем актуальные .proto файлы Salute Speech
echo "Загрузка .proto файлов..."
mkdir "protos"
cd "protos"

# Recognition
curl -OL -s https://raw.githubusercontent.com/salute-developers/salute-speech/master/task/v1/task.proto
curl -OL -s https://raw.githubusercontent.com/salute-developers/salute-speech/master/recognition/v1/recognition.proto

# Synthesis
curl -OL -s https://raw.githubusercontent.com/salute-developers/salute-speech/master/synthesis/v1/synthesis.proto

cd ..

# Создаем папку и __init__.py для сгенерированных .py файлов
mkdir "salute_grps"
touch salute_grps/__init__.py

# Запускаем генерацию gRPC
echo "Генерация gRPC..."
python3 -m grpc_tools.protoc --proto_path=./protos --python_out=./salute_grps --grpc_python_out=./salute_grps task.proto recognition.proto
python3 -m grpc_tools.protoc --proto_path=./protos --python_out=./salute_grps --grpc_python_out=./salute_grps task.proto synthesis.proto
echo "Готово!"