
from screenchop import config
from screenchop.models import Post, Vote

def set_upvote(username, postuid):
    vote, created = Vote.objects.get_or_create(username=username, postuid=postuid)
    
    if created:
        Vote.objects(username=username,
                postuid=postuid).update_one(set__upvoted=True,
                                                    set__downvoted=False)
