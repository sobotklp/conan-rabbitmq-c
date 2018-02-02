from conans import ConanFile, CMake, tools
import os

class RabbitMQConan(ConanFile):
    name = "rabbitmq-c"
    version = "0.6.0"
    license = "MIT"
    description = "This is a C-language AMQP client library for use with v2.0+ of the RabbitMQ broker."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    exports = "FindRabbitmq.cmake"
    default_options = "shared=True"
    requires = ("OpenSSL/1.0.2n@conan/stable")
    generators = "cmake"
    unzipped_name = "rabbitmq-c-%s" % version
    zip_name = "%s.tar.gz" % unzipped_name

    def source(self):
        url = "https://github.com/alanxz/rabbitmq-c/releases/download/v%s/%s" % (self.version, self.zip_name)
        self.output.info("Downloading %s..." % url)

        tools.download(url, self.zip_name)
        tools.unzip(self.zip_name)
        os.unlink(self.zip_name)


    @property
    def subfolder(self):
        return self.unzipped_name


    def build(self):
        cmake = CMake(self)

        # Use dependency version of openssl
        openssl_root_dir = self.deps_cpp_info["OpenSSL"].rootpath
        cmake.definitions['OPENSSL_ROOT_DIR'] = openssl_root_dir
        cmake.definitions['BUILD_EXAMPLES'] = "OFF"  # Don't need to build examples
        cmake.definitions['BUILD_TESTS'] = "OFF"  # Don't need to build tests

        # same as cmake.configure(source_folder=self.source_folder, build_folder=self.build_folder)
        if self.options.shared:
            cmake.definitions['BUILD_SHARED_LIBS'] = True
        else:
            cmake.definitions['BUILD_STATIC_LIBS'] = True
        cmake.configure(source_folder=self.subfolder, build_folder=self.subfolder)

        cmake.build()
        #cmake.test()  # Build the "RUN_TESTS" or "test" target
        # Build the "install" target, defining CMAKE_INSTALL_PREFIX to self.package_folder
        cmake.install()


    def package(self):
        self.copy("*.h", dst="include", src=self.subfolder)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

        # Copy cmake find_package script into project
        self.copy("FindRabbitmq.cmake", ".", ".")

        # Copying debug symbols
        if self.settings.compiler == "Visual Studio" and self.options.include_pdbs:
            self.copy(pattern="*.pdb", dst="lib", src=".", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["rabbitmq"]

        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
