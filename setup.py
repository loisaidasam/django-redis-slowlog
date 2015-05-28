
import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-redis-slowlog',
    version='0.1',
    packages=['djangoredisslowlog'],
    include_package_data=True,
    license='MIT License',
    description='Command line support for ./manage.py redisslowlog',
    long_description=README,
    url='https://github.com/loisaidasam/django-redis-slowlog',
    author='@LoisaidaSam',
    author_email='sam.sandberg@gmail.com',
    install_requires=['pytz', 'redis'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
