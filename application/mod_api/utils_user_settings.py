from application.mod_api.models_user_settings import UserSettings, UserSettingsDAO

def utils_get_user_settings(token):
    user_settings = UserSettingsDAO.get_settings(token=token)
    if user_settings is None:
        UserSettingsDAO.create_settings(token=token)
        user_settings = UserSettingsDAO.get_settings(token=token)

    return user_settings
