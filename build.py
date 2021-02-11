from cpt.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager(username="sobotklp", build_policy="missing")
    builder.add_common_builds(shared_option_name="rabbitmq-c:shared", pure_c=False)
    builder.run()

