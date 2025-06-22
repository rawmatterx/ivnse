from setuptools import setup, find_packages

setup(
    name="ivnse",
    version="0.1.0",
    description="Intrinsic-value engine with Streamlit UI",
    author="Arup Roy",
    author_email="arup@ivnse.com",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.28",
        "pandas",
        "plotly",
        "openpyxl",
        "nsepy"
    ],
    python_requires=">=3.9",
    include_package_data=True
)
