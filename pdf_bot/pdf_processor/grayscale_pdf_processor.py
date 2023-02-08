from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from gettext import gettext as _

from telegram.ext import CallbackQueryHandler

from pdf_bot.analytics import TaskType
from pdf_bot.models import FileData, FileTaskResult, TaskData

from .abstract_pdf_processor import AbstractPdfProcessor


class GrayscalePdfData(FileData):
    pass


class GrayscalePdfProcessor(AbstractPdfProcessor):
    @property
    def task_type(self) -> TaskType:
        return TaskType.grayscale_pdf

    @property
    def task_data(self) -> TaskData:
        return TaskData(_("Grayscale"), GrayscalePdfData)

    @property
    def handler(self) -> CallbackQueryHandler:
        return CallbackQueryHandler(self.process_file, pattern=GrayscalePdfData)

    @asynccontextmanager
    async def process_file_task(self, file_data: FileData) -> AsyncGenerator[FileTaskResult, None]:
        async with self.pdf_service.grayscale_pdf(file_data.id) as path:
            yield FileTaskResult(path)
