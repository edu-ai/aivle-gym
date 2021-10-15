from setuptools import setup

setup(
    name="aivle_gym",
    version="0.2.0",
    description="Super-class of OpenAI Gym environment for aiVLE.",
    url="https://github.com/edu-ai/aivle-gym",
    author="Yuanhong Tan",
    author_email="tan.yuanhong@u.nus.edu",
    packages=["aivle_gym"],
    install_requires=["pyzmq", "gym"],
    setup_requires=['wheel'],
    zip_safe=False,
)
