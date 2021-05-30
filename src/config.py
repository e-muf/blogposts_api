import os

class Config(object):
  """
  Base config
  """
  TESTING = False
  JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
  SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class DevelopmentConfig(Config):
  """
  Development environment configuration
  """
  DEBUG = True
  
class ProductionConfig(Config):
  """
  Production environment configurations
  """
  DEBUG = False

app_config = {
  'development': DevelopmentConfig,
  'production': ProductionConfig,
}