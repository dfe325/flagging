"""
Configurations for the website.
"""


import os
from dataclasses import dataclass

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
VAULT_FILE = os.path.join(ROOT_DIR, 'vault.zip')


@dataclass
class BaseConfig:
    DEBUG: bool = False
    TESTING: bool = False
    #source: https://realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/#update-configuration
    #SQLALCHEMY_DATABASE_URI = "postgresql://yourusername:yourpassword@localhost/yournewdb"
    SQLALCHEMY_DATABASE_URI = "postgresql://daneder:flagging@localhost/crwa_flagging"
    SECRET_KEY: str = None  # Loaded from vault
    KEYS: dict = None  # Loaded from vault
    VAULT_FILE: str = VAULT_FILE


class ProductionConfig(BaseConfig):
    DEBUG: bool = False
    TESTING: bool = False


class DevelopmentConfig(BaseConfig):
    DEBUG: bool = True
    TESTING: bool = True


# class StagingConfig(ProductionConfig):
#     pass


class TestingConfig(BaseConfig):
     TESTING: bool = True
