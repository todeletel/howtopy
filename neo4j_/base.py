from datetime import datetime
from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
                      UniqueIdProperty, RelationshipTo, DateTimeProperty)

config.DATABASE_URL = "bolt://neo4j:123@localhost:7687"


class Person(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True)
    show_name = StringProperty()
    biography = StringProperty()
    profile_photo = StringProperty()
    likes_count = IntegerProperty()
    tweets_count = IntegerProperty()
    followers_count = IntegerProperty()
    following_count = IntegerProperty()
    # traverse outgoing IS_FROM relations, inflate to Country objects
    following = RelationshipTo("Person", 'IS_FOLLOWING')
    using_tag = RelationshipTo("HashTag", "IS_USING_TAG")


class HashTag(StructuredNode):
    uid = UniqueIdProperty()
    tag_name = StringProperty(unique_index=True)
