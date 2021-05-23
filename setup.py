import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name='wx_grab_spider',
    version='1.0.0',
    packages=setuptools.find_packages(),
    install_requires=required,
    url='https://github.com/a-osipov/wx_grab_spider',
    license='MIT License',
    author='Aleksandr Osipov',
    author_email='aleksandr.osipov@zoho.eu',
    description='Building a simple GUI for Grab:Spider with WxPython',
    long_description=long_description,
    keywords='grabbing scraping wxpython',
)
