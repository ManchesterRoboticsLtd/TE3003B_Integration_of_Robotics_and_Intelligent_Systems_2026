from setuptools import find_packages, setup
import os
from glob import glob


package_name = 'puzzlebot_description'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
        (os.path.join('share', package_name, 'config'), glob(os.path.join('config', '*.[yma]*'))),
        (os.path.join('share', package_name, 'rviz'), glob(os.path.join('rviz', '*.rviz'))),
    ]+ [
        (os.path.join('share', package_name, root), [os.path.join(root, file)]) 
        for root, _, files in os.walk('urdf') for file in files
    ]+
    [
        (os.path.join('share', package_name, root), [os.path.join(root, file)]) 
        for root, _, files in os.walk('meshes') for file in files
    ]
    ,
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Mario Martinez',
    maintainer_email='mario.mtz@manchester-robotics.com',
    description='Puzzlebot Description Files',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'joint_state_publisher = puzzlebot_description.joint_state_publisher:main'
        ],
    },
)
