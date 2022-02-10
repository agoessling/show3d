load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
load("@rules_python//python:pip.bzl", "pip_install")

def show3d_direct_deps():
    pip_install(
       name = "show3d_py_deps",
       requirements = "@show3d//:requirements.txt",
    )

    procedural_panda_build = """
load("@rules_python//python:defs.bzl", "py_binary")
load("@show3d_py_deps//:requirements.bzl", "requirement")

py_library(
    name = "procedural_panda",
    srcs = glob(["procedural3d/*.py"]),
    deps = [
        requirement("panda3d"),
    ],
    visibility = ["//visibility:public"],
)"""

    http_archive(
        name = "procedural_panda",
        build_file_content = procedural_panda_build,
        sha256 = "0fede7584b15dbf539f2e46b70e0dac985dfb9401038acea0f13fb3ac289bac5",
        strip_prefix = "procedural_panda3d_model_primitives-261d8d76ee29d69704e5d10257f7ac0acc940487",
        url = "https://github.com/Epihaius/procedural_panda3d_model_primitives/archive/261d8d76ee29d69704e5d10257f7ac0acc940487.zip"
    )
