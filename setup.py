from setuptools import setup


setup(
    name='moodster-api',
    version=1.0,
    packages=[
        'app',
        'scripts'
    ],
    install_requires=[
        'Flask',
        'Flask-Bcrypt',
        'Flask-JWT-Extended',
        'Flask-Migrate',
        'Flask-SQLAlchemy',
        'SQLAlchemy-Utils',
        'flask-restplus',
        'Flask-Testing',
        'bcrypt',
        'passlib',
        'colour',
        'psycopg2'
    ]
)
