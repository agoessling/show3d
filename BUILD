load("@rules_python//python:defs.bzl", "py_binary")
load("@show3d_py_deps//:requirements.bzl", "requirement")

py_library(
    name = "camera_controller",
    srcs = ["camera_controller.py"],
    deps = [
        requirement("panda3d"),
    ],
    visibility = ["//visibility:public"],
)

py_library(
    name = "draw",
    srcs = ["draw.py"],
    deps = [
        requirement("panda3d"),
    ],
    visibility = ["//visibility:public"],
)

py_library(
    name = "grid",
    srcs = ["grid.py"],
    deps = [
        requirement("panda3d"),
    ],
    visibility = ["//visibility:public"],
)

py_binary(
    name = "show3d",
    srcs = ["show3d.py"],
    deps = [
        requirement("panda3d"),
        "@procedural_panda//:procedural_panda",
        ":camera_controller",
        ":grid",
    ],
    visibility = ["//visibility:public"],
)
