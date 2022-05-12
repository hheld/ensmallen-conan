from importlib.metadata import requires
from conans import ConanFile, CMake, tools


class EnsmallenConan(ConanFile):
    name = "ensmallen"
    version = "2.19.0"
    license = "BSD-3-Clause"
    author = "Harald Held <harald.held@gmail.com>"
    url = "https://tbd.com"
    description = "a high-quality C++ library for non-linear numerical optimization"
    topics = ("optimization", "gradient descent", "gradient free", "machine learning")
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps"
    requires = ["armadillo/10.7.3"]
    default_options = "armadillo:use_hdf5=False"

    def source(self):
        self.run(f"git clone -b {self.version} https://github.com/mlpack/ensmallen.git")

    def build(self):
        print(self)
        cmake = CMake(self)
        cmake.definitions["ARMADILLO_INCLUDE_DIR"] = self.dependencies["armadillo"].cpp_info.includedirs[0]
        cmake.definitions["ARMADILLO_LIBRARY"] = self.dependencies["armadillo"].cpp_info.libs
        cmake.configure(source_folder="ensmallen")
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("*.h", dst="include", src="ensmallen")
        self.copy("*.hpp", dst="include", src="ensmallen")

