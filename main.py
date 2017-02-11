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
        blogs = db.GqlQuery('SELECT * FROM Blog ORDER BY created DESC LIMIT 5')
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
            error = 'we need both a title and something to post!'
            self.render_main(title, blog, error)


class ViewPostHandler(Handler):
    def get(self, id):
        #self.request.get('id')
        if id:
            post = Blog.get_by_id(int(id))
            self.render_view('view.html, 

    def render_view(self, title, blog, error):
         blogs = db.GqlQuery('SELECT * FROM Blog ORDER BY created DESC LIMIT 5')
         self.render('view.html', blogs=blogs)

        
        if id:
            self.render
        post = Blog.get_by_id(int(id))
        self.render('view.html', post=post)


# class ViewBlogHandler(Handler):
#     def render_view(self, title, blog, error):
#         blogs = db.GqlQuery('SELECT * FROM Blog ORDER BY created DESC LIMIT 5')
#         self.render('view.html', blogs=blogs)

#     def get(self):
#         self.render('/blog', blogs=blogs)

app = webapp2.Route(
    [('/', MainPage), ('/blog<id:/d+>', ViewPostHandler)#, ('/blog<id:/d+>', ViewBlogHandler), ('/new', NewPostHandler)
], debug=True)
