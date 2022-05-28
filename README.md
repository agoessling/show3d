# show3d

Library to provide discretized building blocks on top of [Panda3d](https://www.panda3d.org/).

## Usage

### WORKSPACE

To incorporate `show3d` into your project copy the following into your `WORKSPACE` file.

```Starlark
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "show3d",
    # See release page for latest version url and sha.
)

load("@show3d//:show3d_first_level_deps.bzl", "show3d_first_level_deps")
show3d_first_level_deps()

load("@show3d//:show3d_second_level_deps.bzl", "show3d_second_level_deps")
show3d_second_level_deps()
```
