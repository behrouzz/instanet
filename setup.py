import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="instanet",
    version="0.0.4",
    author="Behrouz Safari",
    author_email="behrouz.safari@gmail.com",
    description="A python package for analysing Instagram network",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/behrouzz/instanet",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["instanet"],
    include_package_data=True,
    install_requires=["requests", "networkx", "matplotlib"],
    python_requires='>=3.4',
)
