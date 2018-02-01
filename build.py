from conan.packager import ConanMultiPackager


if __name__ == "__main__":
    builder = ConanMultiPackager(username="sobotklp", apple_clang_versions=["8.1"], archs=["x86_64"], args="--build missing")
    builder.add_common_builds(shared_option_name="rabbitmq-c:shared", pure_c=False)
    builder.run()
