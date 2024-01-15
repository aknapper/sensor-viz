from setuptools import setup, find_packages

setup(
    name='sensorviz',
    version='0.1.0',
    packages=find_packages(),  # Automatically discover and include all packages
    install_requires=[
        'dash==2.14.2',
        'pandas==2.1.4',
        'sensirion-shdlc-sensorbridge'
    ],
    entry_points={
        'console_scripts': [
            'your_script_name = your_package.module:main_function',
        ],
    },
    description='Helpful to read and visualize some data.',
    author='Aaron Knapper'
    license='MIT'
)
