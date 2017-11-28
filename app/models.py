from django.db import models
from django.contrib.auth.models import User
import json
from django.utils.timezone import now
from datetime import datetime


class Base(models.Model):
    created_at = models.DateTimeField(default=now())
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def json(self):
        ret = {}
        d = self.__dict__
        d = {k: d[k] for k in d if not (k.startswith('_') or k == 'id' or k.endswith('_id'))}
        for k in d:
            v = d[k]
            ret[k] = v
            if type(v) is datetime:
                ret[k] = v.strftime('%s')

        return ret


class Post(Base):
    author = models.ForeignKey(User, db_index=True, related_name="posts")
    title = models.CharField(max_length=128, null=True, blank=False)
    body_text = models.TextField(null=True, blank=False)
    

    class Meta:
        db_table = "post"

    def json(self):
        ret = super(Post, self).json()
        ret["author"] = user_to_json(self.author)

        # comments = []
        # for c in self.comments:
        #     comments.append(c.json())
        comments = [c.json() for c in self.comments.all()]
        ret["comments"] = comments
        return ret

    def __str__(self):
        return "{} [by {}]".format(self.title, self.author.username)


class Comment(Base):
    author = models.ForeignKey(User, db_index=True, related_name="comments")
    post = models.ForeignKey("Post", db_index=True, related_name="comments", on_delete=models.CASCADE)
    body_text = models.TextField(null=True, blank=False)

    class Meta:
        db_table = "comment"

    def json(self):
        ret = super(Comment, self).json()
        ret["author"] = user_to_json(self.author)
        return ret

    def __str__(self):
        return "Comment by {}".format(self.author.username)


def user_to_json(user):
    return {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "full_name": "{} {}".format(user.first_name, user.last_name),
        "email": user.username,
    }