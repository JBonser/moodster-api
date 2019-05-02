from setuptools import setup


setup(
    name='moodster-api',
    version=1.0,
    packages=[
        'app'
    ],
    install_requires=[
        'Flask',
        'Flask-Migrate',
        'Flask-SQLAlchemy',
        'SQLAlchemy-Utils',
        'flask-restplus',
        'Flask-Testing',
        'bcrypt',
        'passlib',
        'colour'
    ]
)
