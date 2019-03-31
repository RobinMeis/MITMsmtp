import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mitmsmtp",
    version="0.0.1",
    author="Robin Meis",
    author_email="blog@smartnoob.de",
    description="An evil SMTP Server for client pentesting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RobinMeis/MITMsmtp",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
