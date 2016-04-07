# -*- coding: utf-8 -*-
from application.mod_api.models_comment import Comment, CommentDAO
from application.mod_api.models_entry import Entry, EntryDAO
from application.mod_api.models_followed_entries import FollowedEntriesItem, FollowedEntriesDAO
from application.mod_api.models_user_notification import UserNotification, UserNotificationDAO
from application.mod_api.utils_mentions import MentionsUtils


class UserNotificationBroadcaster:

    @staticmethod
    def post_notification_to_op_and_followers(entry_id, user_token):
        # Get entry and create excerpt that can be used as a part of
        # the notification message
        entry = EntryDAO.get_entry(entry_id=entry_id, cur_user_token=user_token)
        excerpt = UserNotificationBroadcaster.excerpt(entry.content)

        recipients = list()
        # Add OP token if user of the comment is not author of the entry
        # the comment is added to.
        if entry.cur_user_is_author is False:
            entry_op_token = EntryDAO.get_op_token_for_entry(entry_id)
            recipients.append(entry_op_token)

        # Get tokens of the followers of this entry and add them if they are
        # not yet added to recipients list.
        following = FollowedEntriesDAO.get_user_tokens_for_entry(entry_id)
        for follower in following:
            if (follower.user_token != user_token and
                follower.user_token not in following):
                recipients.append(follower.user_token)

        # Post notification to recipients
        for token in recipients:
            UserNotificationDAO.save(user_token=token,
                content='Dodano nowy komentarz do wpisu - {}'.format(excerpt),
                object_id=entry_id,
                object_type='entry')


    @staticmethod
    def post_notification_to_mentions(entry_id, comment_content):
        # cur_user_token is not needed here so passing empty string is enough
        entry = EntryDAO.get_entry(entry_id=entry_id, cur_user_token='')

        # get mentions from the comment_content. Do not include @op
        # as original poster of the entry that comment is added to will
        # be notified anyway in post_notification_to_op_and_followers
        # method
        mentions = list()
        findings = MentionsUtils.get_mentions_from_text(comment_content)
        for m in findings:
            if m != 'op' and int(m) <= entry.comments_count:
                mentions.append(m)

        if len(mentions) == 0:
            return

        # Get tokens of users for mentioned comments
        recipients = CommentDAO.get_user_tokens_for_comment_ids(entry_id=entry_id,
            comment_order_numbers=mentions)

        # Post notification to recipients
        excerpt = UserNotificationBroadcaster.excerpt(entry.content)
        for token in recipients:
            UserNotificationDAO.save(user_token=token,
                content='Twój komentarz został wspomnianany w odpowiedzi do wpisu - {}'.format(excerpt),
                object_id=entry_id,
                object_type='entry')


    @staticmethod
    def excerpt(content):
        excerpt = content[:70]
        if len(excerpt) == 70:
            excerpt += "..."
        return excerpt
