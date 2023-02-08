from google.cloud.datastore import Client, Entity

from pdf_bot.consts import LANGUAGE, USER


class LanguageRepository:
    EN_GB_CODE = "en_GB"
    EN_CODE = "en"

    def __init__(self, datastore_client: Client) -> None:
        self.datastore_client = datastore_client

    def get_language(self, user_id: int) -> str:
        user_key = self.datastore_client.key(USER, user_id)
        user = self.datastore_client.get(key=user_key)
        lang: str

        if user is None or LANGUAGE not in user:
            return self.EN_GB_CODE

        lang = user[LANGUAGE]

        # This check is for backwards compitability
        if lang == self.EN_CODE:
            return self.EN_GB_CODE
        return lang

    def upsert_language(self, user_id: int, language_code: str) -> None:
        with self.datastore_client.transaction():
            user_key = self.datastore_client.key(USER, user_id)
            user = self.datastore_client.get(key=user_key)
            if user is None:
                user = Entity(user_key)
            user[LANGUAGE] = language_code
            self.datastore_client.put(user)
