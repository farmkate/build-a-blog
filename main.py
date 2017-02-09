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
    blog = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class MainPage(Handler):
    def render_main(self, title, blog, error):
        blogs = db.GqlQuery('SELECT * FROM Blog ORDER BY created DESC')
        self.render('main.html', title=title, blog=blog, error=error, blogs=blogs)

    def get(self):
        self.render_main(title='', blog='', error='')

    def post(self):
        title = self.request.get('title')
        blog = self.request.get('blog')

        if title and blog:
            b = Blog(title = title, blog = blog)
            b.put()
            self.redirect('/')
        else:
            error = 'we need both a title and a blog post!'
            self.render_main(title, blog, error)

app = webapp2.WSGIApplication(
    [('/', MainPage)
], debug=True)
