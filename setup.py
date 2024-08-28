from setuptools import setup

setup(
    name='exp_lib',
    version='0.2.0',    
    description='Library for the automated running of experiments with computer connected actuators and instruments.',
    url='https://github.com/ssloxford/emi_experiment_lib',
    author='Marcell Szakály',
    author_email='marcell.szakaly@cs.ox.ac.uk',
    license='MIT License',
    packages=['exp_lib'],
    install_requires=['asyncio',
                      'numpy'],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: Microsoft:: Windows',
        'Programming Language :: Python :: 3.9',
    ],
)
