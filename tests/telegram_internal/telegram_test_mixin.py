from unittest.mock import AsyncMock, MagicMock

from telegram import (
    Bot,
    CallbackQuery,
    Chat,
    Document,
    File,
    InlineKeyboardMarkup,
    Message,
    PhotoSize,
    PreCheckoutQuery,
    Update,
    User,
)
from telegram.ext import ContextTypes

from pdf_bot.models import FileData, FileTaskResult, MessageData
from pdf_bot.pdf_processor.abstract_pdf_text_input_processor import TextInputData
from tests.path_test_mixin import PathTestMixin


class TelegramTestMixin(PathTestMixin):
    TELEGRAM_USER_ID = 0
    TELEGRAM_QUERY_USER_ID = 1
    TELEGRAM_CHAT_ID = 2
    TELEGRAM_MESSAGE_ID = 3
    TELEGRAM_USERNAME = "username"
    TELEGRAM_FILE_ID = "file_id"
    TELEGRAM_DOCUMENT_ID = "document_id"
    TELEGRAM_DOCUMENT_NAME = "document_name"
    TELEGRAM_PHOTO_SIZE_ID = "photo_size_id"
    TELEGRAM_TEXT = "text"

    FILE_DATA = FileData(TELEGRAM_DOCUMENT_ID, TELEGRAM_DOCUMENT_NAME)
    MESSAGE_DATA = MessageData(TELEGRAM_CHAT_ID, TELEGRAM_MESSAGE_ID)
    TEXT_INPUT_DATA = TextInputData(
        id=TELEGRAM_DOCUMENT_ID,
        name=TELEGRAM_DOCUMENT_NAME,
        text=TELEGRAM_TEXT,
    )

    BACK_INLINE_MARKUP = MagicMock(spec=InlineKeyboardMarkup)

    def setup_method(self) -> None:
        self.dir_path = self.mock_dir_path()
        self.download_path = self.mock_file_path()
        self.file_path = self.mock_file_path()
        self.file_task_result = FileTaskResult(self.file_path)

        self.telegram_bot = MagicMock(spec=Bot)

        self.telegram_user = MagicMock(spec=User)
        self.telegram_user.id = self.TELEGRAM_USER_ID
        self.telegram_user.username = self.TELEGRAM_USERNAME

        self.telegram_query_user = MagicMock(spec=User)
        self.telegram_query_user.id = self.TELEGRAM_QUERY_USER_ID

        self.telegram_chat = MagicMock(spec=Chat)
        self.telegram_chat.id = self.TELEGRAM_CHAT_ID

        self.telegram_file = MagicMock(spec=File)
        self.telegram_file.file_id = self.TELEGRAM_FILE_ID

        self.telegram_document = MagicMock(spec=Document)
        self.telegram_document.file_id = self.TELEGRAM_DOCUMENT_ID
        self.telegram_document.file_name = self.TELEGRAM_DOCUMENT_NAME

        self.telegram_photo_size = MagicMock(spec=PhotoSize)
        self.telegram_photo_size.file_id = self.TELEGRAM_PHOTO_SIZE_ID

        self.telegram_message = AsyncMock(spec=Message)
        self.telegram_message.chat = self.telegram_chat
        self.telegram_message.chat_id = self.TELEGRAM_CHAT_ID
        self.telegram_message.from_user = self.telegram_user
        self.telegram_message.document = self.telegram_document
        self.telegram_message.text = self.TELEGRAM_TEXT

        self.telegram_callback_query = AsyncMock(spec=CallbackQuery)
        self.telegram_callback_query.from_user = self.telegram_query_user
        self.telegram_callback_query.message = self.telegram_message

        self.telegram_pre_checkout_query = MagicMock(spec=PreCheckoutQuery)

        self.telegram_update = AsyncMock(spec=Update)
        self.telegram_update.message = self.telegram_message
        self.telegram_update.effective_message = self.telegram_message
        self.telegram_update.callback_query = self.telegram_callback_query
        self.telegram_update.pre_checkout_query = self.telegram_pre_checkout_query

        self.telegram_user_data = MagicMock(spec=dict)
        self.telegram_context = AsyncMock(spec=ContextTypes.DEFAULT_TYPE)
        self.telegram_context.bot = self.telegram_bot
        self.telegram_context.user_data = self.telegram_user_data

    def teardown_method(self) -> None:
        pass
