import conans
from conans import ConanFile, CMake, tools
import os

class RabbitMQConan(ConanFile):
    name = "rabbitmq-c"
    version = "0.6.0"
    license = "MIT"
    description = "This is a C-language AMQP client library for use with v2.0+ of the RabbitMQ broker."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    exports = "FindRabbitmqc.cmake"
    default_options = "shared=True", "fPIC=True"
    requires = ("openssl/1.1.1h")
    generators = "cmake"
    unzipped_name = "rabbitmq-c-%s" % version
    zip_name = "%s.tar.gz" % unzipped_name

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def source(self):
        url = "https://github.com/alanxz/rabbitmq-c/archive/v%s.tar.gz" % (self.version)
        self.output.info("Downloading %s..." % url)

        tools.download(url, self.zip_name)
        tools.unzip(self.zip_name)
        os.unlink(self.zip_name)
        root_cmakelists = os.path.join(self.unzipped_name, "CMakeLists.txt")
        librabbitmq_cmakelists = os.path.join(os.path.join(self.unzipped_name, "librabbitmq"), "CMakeLists.txt")
        tools.replace_in_file(root_cmakelists, """project(rabbitmq-c "C")""",
                              """project(rabbitmq-c "C")
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()""")
        # CMake's find_package(OpenSSL) has numerous problems: it fails to add dl lib under Linux,
        # crypt32 lib under Windows etc. So we use conan-supplied settings
        tools.replace_in_file(librabbitmq_cmakelists, "OPENSSL_INCLUDE_DIR", "CONAN_INCLUDE_DIRS_OPENSSL")
        tools.replace_in_file(librabbitmq_cmakelists, "OPENSSL_LIBRARIES", "CONAN_LIBS_OPENSSL")
        # Actually Win32 static lib can be built
        try:
            tools.replace_in_file(root_cmakelists,
                              """if (WIN32 AND BUILD_STATIC_LIBS)
  message(FATAL_ERROR "The rabbitmq-c library cannot be built as a static library on Win32. Set BUILD_STATIC_LIBS=OFF to get around this.")
endif()""", "")
        except conans.errors.ConanException:
            # This pattern does not exist in later versions of rabbitmq-c
            pass

    @property
    def subfolder(self):
        return self.unzipped_name


    def build(self):
        cmake = CMake(self)

        # Use dependency version of openssl
        openssl_root_dir = self.deps_cpp_info["openssl"].rootpath
        cmake.definitions['OPENSSL_ROOT_DIR'] = openssl_root_dir
        cmake.definitions['BUILD_EXAMPLES'] = "OFF"  # Don't need to build examples
        cmake.definitions['BUILD_TESTS'] = "OFF"  # Don't need to build tests

        # same as cmake.configure(source_folder=self.source_folder, build_folder=self.build_folder)
        if self.options.shared:
            cmake.definitions['BUILD_SHARED_LIBS'] = True
        else:
            cmake.definitions['BUILD_STATIC_LIBS'] = True
        if self.settings.os != "Windows":
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = self.options.fPIC
        cmake.definitions["CMAKE_INSTALL_PREFIX"] = "install"
        cmake.configure(source_folder=self.subfolder)

        cmake.build()
        #cmake.test()  # Build the "RUN_TESTS" or "test" target
        # Build the "install" target, defining CMAKE_INSTALL_PREFIX to self.package_folder
        cmake.install()


    def package(self):
        self.copy("*.h", dst="include", src="install", keep_path=False)
        self.copy("*.lib", dst="lib", src="install", keep_path=False)
        self.copy("*.dll", dst="bin", src="install", keep_path=False)
        self.copy("*.pdb", dst="bin", src="install", keep_path=False)
        self.copy("*.so*", dst="lib", src="install", keep_path=False, symlinks=True)
        self.copy("*.dylib", dst="lib", src="install", keep_path=False, symlinks=True)
        self.copy("*.a", dst="lib", src="install", keep_path=False)

        # Copy cmake find_package script into project
        self.copy("FindRabbitmqc.cmake", ".", ".")

    def package_info(self):
        if self.settings.os == "Windows":
            if self.options.shared:
                self.cpp_info.libs = ["rabbitmq.4"]
            else:
                self.cpp_info.libs = ["librabbitmq.4"]
        else:
            self.cpp_info.libs = ["rabbitmq"]
