from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout, CMakeToolchain, CMakeDeps


class EnsmallenConan(ConanFile):
    name = "ensmallen"
    version = "2.19.0"
    license = "BSD-3-Clause"
    author = "Harald Held <harald.held@gmail.com>"
    url = "https://github.com/hheld/ensmallen-conan"
    description = "a high-quality C++ library for non-linear numerical optimization"
    topics = ("optimization", "gradient descent", "gradient free", "machine learning")
    settings = "os", "compiler", "build_type", "arch"
    requires = ["armadillo/10.7.3"]
    default_options = "armadillo:use_hdf5=False"

    def source(self):
        self.run(f"git clone -b {self.version} https://github.com/mlpack/ensmallen.git")

    def generate(self):
        tc = CMakeToolchain(self)
        tc.preprocessor_definitions["ARMADILLO_INCLUDE_DIR"] = self.dependencies["armadillo"].cpp_info.includedirs[0]
        tc.preprocessor_definitions["ARMADILLO_LIBRARY"] = self.dependencies["armadillo"].cpp_info.libs
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure(build_script_folder="ensmallen")
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("*.h", dst="include", src="ensmallen")
        self.copy("*.hpp", dst="include", src="ensmallen")

    def layout(self):
        cmake_layout(self)
