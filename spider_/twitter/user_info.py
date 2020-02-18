from base import Person, HashTag
from twitter_api import Profile


def fill_user_info(user_obj: Person):
    try:
        user_profile = Profile(user.name)
        """
        show_name = StringProperty()
        biography = StringProperty()
        profile_photo = StringProperty()
        likes_count = IntegerProperty()
        tweets_count = IntegerProperty()
        followers_count = IntegerProperty()
        following_count = IntegerProperty()
        """
        user_obj.show_name = user_profile.name
        user_obj.biography = user_profile.biography
        user_obj.profile_photo = user_profile.profile_photo
        user_obj.likes_count = user_profile.likes_count
        user_obj.tweets_count = user_profile.tweets_count
        user_obj.followers_count = user_profile.followers_count
        user_obj.following_count = user_profile.following_count
        user_obj.save()
        using_tags = user_profile.tags
        if using_tags:
            for tag in using_tags:
                tag_obj = HashTag.get_or_create(tag_name=tag)
                if not tag_obj:
                    tag_obj = HashTag(tag_name=tag).save()
                user.using_tag.connect(tag_obj)
        print(user_profile.to_dict())
    except Exception as e:
        print(e)
        user_obj.delete()


if __name__ == '__main__':
    all_user = Person.nodes.all()
    for user in all_user:
        fill_user_info(user)