cmake_minimum_required(VERSION 3.19)
project(DiligentRenderStatePackager LANGUAGES C CXX)

set(DILIGENT_NO_RENDER_STATE_PACKAGER OFF CACHE BOOL "" FORCE)
set(DILIGENT_BUILD_TESTS         OFF CACHE BOOL "" FORCE)
set(DILIGENT_INSTALL_CORE        OFF CACHE BOOL "" FORCE)
set(DILIGENT_INSTALL_TOOLS       OFF CACHE BOOL "" FORCE)
set(DILIGENT_NO_OPENGL           ON  CACHE BOOL "" FORCE)
set(DILIGENT_NO_METAL            ON  CACHE BOOL "" FORCE)
# SuperResolution's DirectSR/DLSS FetchContent breaks on Windows + recent SDK; unused by the packager.
set(DILIGENT_NO_SUPER_RESOLUTION ON  CACHE BOOL "" FORCE)
set(DILIGENT_NO_VULKAN           OFF CACHE BOOL "" FORCE)
set(DILIGENT_NO_WEBGPU           OFF CACHE BOOL "" FORCE)

add_subdirectory(DiligentCore)
add_subdirectory(DiligentTools)

# Static-link libstdc++/libgcc so the manylinux wheel's binary runs on any Linux host.
if (UNIX AND NOT APPLE AND TARGET Diligent-RenderStatePackager)
    target_link_options(Diligent-RenderStatePackager PRIVATE -static-libstdc++ -static-libgcc)
endif()
