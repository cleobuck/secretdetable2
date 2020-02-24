from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import BlogPosts, Base

engine = create_engine('sqlite:///secretdetable.db')

# bind engine to Base metadata so that the database table and class definitions are connected 

Base.metadata.bind = engine

# interface called Session to execute queries 
DBSession = sessionmaker(bind=engine)

session = DBSession()


#push one entry:
blogPost1 = BlogPosts(title="blog post 1", content="blog post content 1")
session.add(blogPost1)
session.commit()




print(blogPost1.id)
editedBlogPost = session.query(BlogPosts).filter_by(id=1).one()
editedBlogPost.title = "different title"
session.add(editedBlogPost)
session.commit()
print(session.query(BlogPosts).filter_by(id=1).one().title)
blogPostToDelete = session.query(BlogPosts).filter_by(id=1).one()
session.delete(blogPostToDelete)
print(session.query(BlogPosts).filter_by(id=2).one().title)

