from conans import ConanFile, CMake, tools

required_conan_version = ">=1.33.0"


class YoctoglConan(ConanFile):
    name = "yocto-gl"
    description = "Yocto/GL: Tiny C++ Libraries for Data-Driven Physically-based Graphics."
    license = "MIT"
    topics = ("yocto/gl", "pbr", "physically-based-rendering")
    homepage = "https://github.com/xelatihy/yocto-gl"
    url = "https://github.com/conan-io/conan-center-index"

    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }

    exports_sources = ["CMakeLists.txt", "patches/**"]
    generators = "cmake", "cmake_find_package_multi"
    _cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

    def requirements(self):
        self.requires("fast_float/3.2.0")
        self.requires("nlohmann_json/3.10.3")
        self.requires("stb/cci.20210713")
        # tinyexr is also a dependency but vendored and modified

    def source(self):
        tools.get(**self.conan_data["sources"][self.version],
                  destination=self._source_subfolder, strip_root=True)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.definitions["YOCTO_OPENGL"] = False
        self._cmake.definitions["YOCTO_DENOISE"] = False
        self._cmake.definitions["YOCTO_EMBREE"] = False
        self._cmake.definitions["YOCTO_TESTING"] = False
        self._cmake.configure()
        return self._cmake

    def build(self):
        for patch in self.conan_data.get("patches", {}).get(self.version, []):
            tools.patch(**patch)
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["yocto_unsupported", "yocto"]
        if self.settings.os in ["Linux", "FreeBSD"]:
            self.cpp_info.system_libs.append("pthread")
