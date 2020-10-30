from setuptools import setup

setup(
    name='pArm',
    version='1.0',
    packages=['pArm', 'pArm.gcode', 'pArm.utils', 'pArm.logger', 'pArm.control',
              'pArm.security', 'pArm.communications'],
    url='https://github.com/pArm-TFG/pArm-S1',
    license='GNU GPL v3',
    author='pArm-TFG',
    python_requires='~=3.8',
    install_requires=['pyqtgraph~=0.11.0', 'pyserial~=3.4', 'PyQt5~=5.15.1'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'pArm=pArm.__main__:main'
        ]
    }
)
