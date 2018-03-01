from conan.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager(username="sobotklp", args="--build missing")
    builder.add_common_builds(shared_option_name="rabbitmq-c:shared", pure_c=False)
    builder.run()

