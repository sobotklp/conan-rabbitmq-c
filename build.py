from conan.packager import ConanMultiPackager


if __name__ == "__main__":
    builder = ConanMultiPackager(username="sobotklp", archs=["x86_64"], args="--build missing")
    builder.add_common_builds(shared_option_name="librabbitmq-c:shared", pure_c=False)
    builder.run()
