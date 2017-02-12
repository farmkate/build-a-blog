import os
import jinja2
import webapp2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Blog(db.Model):
    title = db.StringProperty(required = True)
    blog_post = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class MainPage(Handler):
    def render_main(self):
        blog_posts = db.GqlQuery('SELECT * FROM Blog ORDER BY created DESC LIMIT 5')
        self.render('blog.html', blog=blog_posts)

    def get(self):
        self.render_main()


class NewPostHandler(Handler):
    def render_add(self, title, blog_post, error):
        self.render('add.html', title=title, blog_post=blog_post, error=error)

    def get(self):
        self.render_add(title='', blog_post='', error='')

    def post(self):
        title = self.request.get('title')
        blog_post = self.request.get('blog_post')

        if title and blog_post:
            a = Blog(title = title, blog_post = blog_post)
            a.put()
            id = a.key().id()
            self.redirect('/blog/' + str(id))
        else:
            error = 'We need both a title and something to post!'
            self.render_add(title, blog_post, error)


class ViewPostHandler(Handler):
    def get(self, id):
        single = Blog.get_by_id( int(id) )
        self.render('blog.html', single_post = single)

  

app = webapp2.WSGIApplication(
    [('/blog', MainPage), ('/blog/newpost', NewPostHandler), webapp2.Route('/blog/<id:\d+>', handler = ViewPostHandler)
], debug=True)
