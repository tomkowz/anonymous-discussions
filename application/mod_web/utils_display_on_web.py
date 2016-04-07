import flask, json

from application.mod_api.models_hashtag import \
    Hashtag, HashtagDAO

from application.mod_api.models_recommended_hashtag import \
    RecommendedHashtag, RecommendedHashtagDAO

from application.mod_api.models_user_settings import UserSettings

from application.mod_api.views_user_settings import \
    api_get_user_settings

from application.mod_web.utils_user_notifications import \
    utils_get_user_notifications_count

from application.mod_web.presentable_object import \
    PresentableEntry, PresentablePopularHashtag, \
    PresentableRecommendedHashtag


class UtilsDisplayOnWeb:

    def __init__(self, user_token):
        self.user_token = user_token


    def get_popular_hashtags(self):
        hashtags = HashtagDAO.get_most_popular_hashtags(20)
        return [PresentablePopularHashtag(h) for h in hashtags]


    def get_recommended_hashtags(self):
        recommended_hashtags = RecommendedHashtagDAO.get_all()
        return [PresentableRecommendedHashtag(h) for h in recommended_hashtags]


    def get_user_notifications_count(self):
        return utils_get_user_notifications_count(self.user_token)


    def get_user_settings(self):
        response, _ = api_get_user_settings(user_token=self.user_token)
        response_json = json.loads(response.data)['user_settings']
        user_settings = UserSettings.from_json(response_json)
        return user_settings
