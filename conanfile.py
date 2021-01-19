from conans import ConanFile, CMake, MSBuild, tools


class BaldrConan(ConanFile):
    name = "baldr"
    requires = (("eigen/3.3.9"),
                ("fmt/7.1.3"),
                ("glew/2.1.0"))
    version = "0.2"
    license = "unlicense"
    author = "Richard Vock vock@cs.uni-bonn.de"
    url = "https://github.com/richard-vock/conan-baldr"
    description = "Modern OpenGL wrapper library"
    topics = ("opengl")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "verbose": [True, False]}
    default_options = "shared=False", "verbose=False"
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/richard-vock/baldr.git")

    def build(self):
        cmake = CMake(self)
        cmake.definitions["DEBUG_VERBOSE"] = self.options.verbose
        cmake.configure(source_folder="baldr")
        if self.settings.os == "Windows":
            msbuild = MSBuild(self)
            msbuild.build("baldr.sln")
        else:
            cmake.build()

    def package(self):
        if self.settings.os == "Windows":
            self.copy("baldr/include/*.hpp", dst="include/baldr", keep_path=False)
            self.copy("baldr/include/*.ipp", dst="include/baldr", keep_path=False)
            self.copy("*baldr.lib", dst="lib", keep_path=False)
            self.copy("*.dll", dst="bin", keep_path=False)
        else:
            self.copy("include/*.hpp")
            self.copy("include/*.ipp")
            self.copy("*.so", dst="lib", keep_path=False)
            self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["baldr"]
