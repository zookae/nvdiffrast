import os
from setuptools import setup
from torch.utils import cpp_extension

plugin_name = "nvdiffrast_plugin"
source_files = [
    '../common/cudaraster/impl/Buffer.cpp',
    '../common/cudaraster/impl/CudaRaster.cpp',
    '../common/cudaraster/impl/RasterImpl.cuda.cu', # changed
    '../common/cudaraster/impl/RasterImpl.cpp',
    '../common/common.cpp',
    '../common/rasterize.cu',
    '../common/interpolate.cu',
    '../common/texture.cuda.cu', # changed
    '../common/texture.cpp',
    '../common/antialias.cu',
    'torch_bindings.cpp',
    'torch_rasterize.cpp',
    'torch_interpolate.cpp',
    'torch_texture.cpp',
    'torch_antialias.cpp',
]
opts = ['-DNVDR_TORCH']
ldflags = []

# torch.utils.cpp_extension.load(
#     name=plugin_name,
#     sources=source_paths,
#     extra_cflags=opts,
#     extra_cuda_cflags=opts+['-lineinfo'],
#     extra_ldflags=ldflags,
#     with_cuda=True, # force inclusion of CUDA headers. redundant with *.cu[h] files
#     verbose=False)


os.environ["TORCH_CUDA_ARCH_LIST"] = "7.5 8.0 8.6+PTX"
setup(name=plugin_name,
    ext_modules=[cpp_extension.CUDAExtension(
        plugin_name,
        source_files,
        # note: CUDAExtension is not smart about matching *.cpp & *.cu files
        #   so we name the *.cu version *.cuda.cu
        extra_compile_args={
            "cxx": opts,
            "nvcc": opts+['-lineinfo'],
        },
    )],
    cmdclass={"build_ext": cpp_extension.BuildExtension},
)