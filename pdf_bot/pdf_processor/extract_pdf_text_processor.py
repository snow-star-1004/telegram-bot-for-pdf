from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from gettext import gettext as _

from telegram.ext import CallbackQueryHandler

from pdf_bot.analytics import TaskType
from pdf_bot.models import FileData, FileTaskResult, TaskData

from .abstract_pdf_processor import AbstractPdfProcessor


class ExtractPdfTextData(FileData):
    pass


class ExtractPdfTextProcessor(AbstractPdfProcessor):
    @property
    def task_type(self) -> TaskType:
        return TaskType.get_pdf_text

    @property
    def task_data(self) -> TaskData:
        return TaskData(_("Extract text"), ExtractPdfTextData)

    @property
    def handler(self) -> CallbackQueryHandler:
        return CallbackQueryHandler(self.process_file, pattern=ExtractPdfTextData)

    @asynccontextmanager
    async def process_file_task(self, file_data: FileData) -> AsyncGenerator[FileTaskResult, None]:
        async with self.pdf_service.extract_pdf_text(file_data.id) as path:
            yield FileTaskResult(path)
