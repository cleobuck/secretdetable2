import sys
import os

#for creating the mapper code
from sqlalchemy import Column, ForeignKey, Integer, String

#for configuration and class code
from sqlalchemy.ext.declarative import declarative_base

#for creating foreign key relationship between the tables
from sqlalchemy.orm import relationship

#for configuration
from sqlalchemy import create_engine

#create declarative_base instance
Base = declarative_base()

#we'll add classes here

class Post(Base):
   __tablename__ = 'Post'

   id = Column(Integer, primary_key=True)
   title = Column(String(250), nullable=False)
   content = Column(String(), nullable=False)
   image = Column(String(), nullable=False)

   @property
   def serialize(self):
     return {
        'title': self.title,
        'content': self.content,
        'id': self.id,
        'image': self.image,
     }

class Gallery(Base):
   __tablename__ = "Gallery"

   id = Column(Integer, primary_key=True)
   title = Column(String(250), nullable=False)
   url = Column(String(), nullable=False)
 
   @property 
   def serialize(self):
      return {
         'title': self.title,
         'id': self.id,
         'url': self.url
      }


#creates a create_engine instance at the bottom of the file
engine = create_engine(os.environ.get("DATABASE_URI"))

Base.metadata.create_all(engine)