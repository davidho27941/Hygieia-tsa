import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hygieia-tsa",
    version="0.1.0",
    author="David Ho",
    author_email="davidho@gapp.nthu.edu.tw",
    description="A pytorch based time series forecasting for ER.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10.0',
    install_requires=[
    ]
)
