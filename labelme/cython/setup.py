from Cython.Build import cythonize
from setuptools import setup, Extension

setup(ext_modules=cythonize(Extension(
    'mylivewire',                            # 生成的模块名称
    sources=['mylivewire.pyx'],              # 要编译的文件
    language='c++',                         # 使用的语言
    include_dirs=[],                        # gcc的-I参数
    library_dirs=[],                        # gcc的-L参数
    libraries=[],                           # gcc的-l参数
    extra_compile_args=[],                  # 附加编译参数
    extra_link_args=[],                     # 附加链接参数
)))