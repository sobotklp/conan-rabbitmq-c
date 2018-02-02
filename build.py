from conan.packager import ConanMultiPackager
import platform

if __name__ == "__main__":
    builder = ConanMultiPackager(username="sobotklp", archs=["x86_64"], args="--build missing")
    builder.add_common_builds(shared_option_name="rabbitmq-c:shared", pure_c=False)

    # The rabbitmq-c library cannot be built as a static library on Win32.
    if platform.system() == "Windows":
        shared_builds = []
        for settings, options, env_vars, build_requires in builder.builds:
            if options.get("rabbitmq-c:shared"):
                shared_builds.append([settings, options, env_vars, build_requires])

        builder.builds = shared_builds

    builder.run()

