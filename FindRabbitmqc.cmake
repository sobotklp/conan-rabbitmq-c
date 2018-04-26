# Try to find Rabbitmqc
# Once done, this will define
#
# Rabbitmqc_FOUND        - system has Rabbitmqc
# Rabbitmqc_INCLUDE_DIR  - The Rabbitmqc include directory
# Rabbitmqc_LIBRARIES    - The libraries need to use Rabbitmqc
# Rabbitmqc_SSL_ENABLED  - OpenSSL is enabled in the Rabbitmqc build

find_path(
        Rabbitmqc_INCLUDE_DIR
        NAMES amqp.h
        PATHS ${CONAN_INCLUDE_DIRS_RABBITMQ-C}
)

find_library(
        Rabbitmqc_LIBRARY
        NAMES rabbitmq rabbitmq.4 librabbitmq.4
        PATHS ${CONAN_LIB_DIRS_RABBITMQ-C}
)

set(Rabbitmqc_FOUND TRUE)
set(Rabbitmqc_INCLUDE_DIRS ${Rabbitmqc_INCLUDE_DIR})
set(Rabbitmqc_LIBRARIES ${Rabbitmqc_LIBRARY})
set(Rabbitmqc_SSL_ENABLED TRUE)

mark_as_advanced(Rabbitmqc_LIBRARY Rabbitmqc_INCLUDE_DIR)
