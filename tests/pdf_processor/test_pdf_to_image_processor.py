from unittest.mock import MagicMock

import pytest
from telegram.ext import CallbackQueryHandler

from pdf_bot.analytics import TaskType
from pdf_bot.models import TaskData
from pdf_bot.pdf import PdfService
from pdf_bot.pdf_processor import PdfToImageData, PdfToImageProcessor
from tests.language import LanguageServiceTestMixin
from tests.telegram_internal import TelegramServiceTestMixin, TelegramTestMixin


class TestPdfToImageProcessor(
    LanguageServiceTestMixin,
    TelegramServiceTestMixin,
    TelegramTestMixin,
):
    def setup_method(self) -> None:
        super().setup_method()
        self.pdf_service = MagicMock(spec=PdfService)
        self.language_service = self.mock_language_service()
        self.telegram_service = self.mock_telegram_service()

        self.sut = PdfToImageProcessor(
            self.pdf_service,
            self.telegram_service,
            self.language_service,
            bypass_init_check=True,
        )

    def test_get_task_type(self) -> None:
        actual = self.sut.task_type
        assert actual == TaskType.pdf_to_image

    def test_task_data(self) -> None:
        actual = self.sut.task_data
        assert actual == TaskData("To images", PdfToImageData)

    def test_handler(self) -> None:
        actual = self.sut.handler

        assert isinstance(actual, CallbackQueryHandler)
        assert actual.pattern == PdfToImageData

    @pytest.mark.asyncio
    async def test_process_file_task(self) -> None:
        self.pdf_service.convert_pdf_to_images.return_value.__aenter__.return_value = self.file_path

        async with self.sut.process_file_task(self.FILE_DATA) as actual:
            assert actual == self.file_task_result
            self.pdf_service.convert_pdf_to_images.assert_called_once_with(self.FILE_DATA.id)
