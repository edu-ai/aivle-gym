from setuptools import setup

setup(
    name="aivle_gym",
    version="0.2.1",
    description="Super-class of OpenAI Gym environment for aiVLE.",
    url="https://github.com/edu-ai/aivle-gym",
    author="Nishita Dutta",
    author_email="nishita.dutta@u.nus.edu",
    packages=["aivle_gym"],
    install_requires=["pyzmq", "gym==0.26.2", "numpy==1.24.2"],
    python_requires=">=3.4",
    setup_requires=['wheel'],
    zip_safe=False,
)
