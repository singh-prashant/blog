import datetime, re

from app import db
from app import bcrypt, login_manager


@login_manager.user_loader
def _user_loader(user_id):
    return User.query.get(int(user_id))

def slugify(s):
    return re.sub('[^\w]+', '-', s).lower()


entry_tags = db.Table('entry_tags',
                      db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                      db.Column('entry_id', db.Integer, db.ForeignKey('entry.id'))
                      )

entry_category = db.Table('entry_category',
                      db.Column('category_id', db.Integer, db.ForeignKey('category.id')),
                      db.Column('entry_id', db.Integer, db.ForeignKey('entry.id'))
                      )

class Entry(db.Model):
    STATUS_PUBLIC = 0
    STATUS_DRAFT = 1
    STATUS_DELETED = 2
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    slug = db.Column(db.String(256), unique=True)
    body = db.Column(db.Text)
    status = db.Column(db.SmallInteger, default=STATUS_PUBLIC)
    created_timestamp = db.Column(
        db.DateTime,
        default=datetime.datetime.now
    )
    modified_timestamp = db.Column(
        db.DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now
    )

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))


    tags = db.relationship('Tag', secondary = entry_tags,
                           backref=db.backref('entries', lazy='dynamic'))


    category = db.relationship('Category', secondary = entry_category,
                           backref=db.backref('entries', lazy='dynamic'))

    comments = db.relationship('Comment',backref='entry',lazy='dynamic')

    @property
    def tag_list(self):
        return ', '.join([tag.name for tag in self.tags])

    @property
    def tease(self):
        return self.body[:100]

    def __init__(self, *args, **kwargs):
        super(Entry, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        self.slug = ''
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self):
        return '<Entry: %s>' %self.title


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    slug = db.Column(db.String(64), unique=True)

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.generate_slug()

    def __repr__(self):
        return '<Tag: %s>'% (self.name)

    def generate_slug(self):
        self.slug = ''
        if self.name:
            self.slug = slugify(self.name)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    slug = db.Column(db.String(64), unique=True)

    def __init__(self, *args, **kwargs):
        super(Category, self).__init__(*args, **kwargs)
        self.slug = slugify(self.name)

    def __repr__(self):
        return '<Category: %s>'%( self.name )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(64))
    slug = db.Column(db.String(64), unique=True)
    active = db.Column(db.Boolean, default=False)
    admin = db.Column(db.Boolean, default=False)
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    last_seen = db.Column(db.DateTime,
                          default=datetime.datetime.now,
                          onupdate=datetime.datetime.now
    )

    entries = db.relationship('Entry', backref='author', lazy='dynamic')

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        self.slug = slugify(self.name)

    def get_id(self):
        return unicode(self.id)

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def is_admin(self):
        return self.admin

    def __str__(self):
        return "<User %s>"%unicode(self.name)

    @staticmethod
    def make_password(plaintext):
        return bcrypt.generate_password_hash(plaintext)


    def check_password(self, raw_password):
        return bcrypt.check_password_hash(self.password, raw_password)

    @classmethod
    def create(cls, email, password, **kwargs):
        return User(
            email=email,
            password = User.make_password(password),
            **kwargs
        )

    @staticmethod
    def authenticate(email, password):
        user = User.query.filter(User.email==email).first()
        if user and user.check_password(password):
            return user
        return False


class Comment(db.Model):
    STATUS_PENDING_MODERATION = 0
    STATUS_PUBLIC  = 1
    STATUS_SPAM = 8
    STATUS_DELETED = 9

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    url = db.Column(db.String(100))
    ip_address = db.Column(db.String(64))
    body = db.Column(db.Text)
    status = db.Column(db.SmallInteger, default=STATUS_PUBLIC)
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    entry_id = db.Column(db.Integer, db.ForeignKey('entry.id'))

    def __repr__(self):
        return '<Comment from %s>'%(self.name)



