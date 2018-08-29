from setuptools import setup

setup(
    name='joushi',
    version='1.0',
    py_modules=["joushi"],
    url='',
    license='MIT',
    author='Jonathan Rainer',
    author_email='jonathan.rainer@york.ac.uk',
    description='A file to automate running simulations and plotting their results.',
    install_requires=[
        "cycler==0.10.0",
        "matplotlib==2.1.1",
        "numpy==1.13.3",
        "pyparsing==2.2.0",
        "python-dateutil==2.6.1",
        "pytz==2017.3",
        "six==1.11.0",
        "Verilog-VCD==1.11"
    ]
)
