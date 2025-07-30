from setuptools import setup, find_packages

setup(
    name='myplugin',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'python-novaclient',
    ],
    entry_points={
        'openstack.plugin': [
            'myplugin = myplugin.plugin:MyPlugin',
        ],
    },
)
