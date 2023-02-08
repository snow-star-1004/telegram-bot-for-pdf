from unittest.mock import MagicMock

import pytest
from telegram.ext import CallbackQueryHandler

from pdf_bot.analytics import TaskType
from pdf_bot.image import ImageService
from pdf_bot.image_processor import ImageToPdfProcessor
from pdf_bot.image_processor.image_to_pdf_processor import ImageToPdfData
from pdf_bot.models import TaskData
from tests.language import LanguageServiceTestMixin
from tests.telegram_internal import TelegramServiceTestMixin, TelegramTestMixin


class TestImageToPdfProcessorProcessor(
    LanguageServiceTestMixin,
    TelegramServiceTestMixin,
    TelegramTestMixin,
):
    def setup_method(self) -> None:
        super().setup_method()
        self.image_service = MagicMock(spec=ImageService)
        self.language_service = self.mock_language_service()
        self.telegram_service = self.mock_telegram_service()

        self.sut = ImageToPdfProcessor(
            self.image_service,
            self.telegram_service,
            self.language_service,
            bypass_init_check=True,
        )

    def test_task_type(self) -> None:
        actual = self.sut.task_type
        assert actual == TaskType.image_to_pdf

    def test_task_data(self) -> None:
        actual = self.sut.task_data
        assert actual == TaskData("To PDF", ImageToPdfData)

    def test_handler(self) -> None:
        actual = self.sut.handler

        assert isinstance(actual, CallbackQueryHandler)
        assert actual.pattern == ImageToPdfData

    @pytest.mark.asyncio
    async def test_process_file_task(self) -> None:
        self.image_service.convert_images_to_pdf.return_value.__aenter__.return_value = (
            self.file_path
        )

        async with self.sut.process_file_task(self.FILE_DATA) as actual:
            assert actual == self.file_task_result
            self.image_service.convert_images_to_pdf.assert_called_once_with([self.FILE_DATA])
