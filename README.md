# conan-rabbitmq-c

[Conan.io](https://conan.io) package for [RabbitMQ C/C++ library](https://github.com/alanxz/rabbitmq-c)

[![Build Status](https://travis-ci.org/sobotklp/conan-rabbitmq-c.svg?branch=master)](https://travis-ci.org/sobotklp/conan-rabbitmq-c)

## Build packages

Download conan client from [Conan.io](https://conan.io) and run:

    $ python build.py

Or, alternatively with python3/pip3:

    $ CONAN_PIP_COMMAND=pip3 CONAN_APPLE_CLANG_VERSIONS=11.0 python3 build.py

## Upload packages to server

    $ conan upload rabbitmq-c/0.6.0@sobotklp/stable --all

## Reuse the packages

### Basic setup

    $ conan install rabbitmq-c/0.6.0@sobotklp/stable

### Project setup

If you handle multiple dependencies in your project, it would be better to add a *conanfile.txt*

    [requires]
    rabbitmq-c/0.6.0@sobotklp/stable

    [generators]
    txt
    cmake


