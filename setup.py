from setuptools import setup, find_packages

with open("README-cn.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

setup(
    name="pixiver",
    version="0.0.8.8161",
    author="yomikochan",
    author_email="darkchii@qq.com",
    description="This is a python package for getting illustration with pixiv ajax interfaces.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['requests', 'pillow'],
    packages=find_packages(),
    url='https://github.com/yomikochan/pixiver',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet'
    ]
)
