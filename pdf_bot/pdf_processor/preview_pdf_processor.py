from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from gettext import gettext as _

from telegram.ext import CallbackQueryHandler

from pdf_bot.analytics import TaskType
from pdf_bot.models import FileData, FileTaskResult, TaskData

from .abstract_pdf_processor import AbstractPdfProcessor


class PreviewPdfData(FileData):
    pass


class PreviewPdfProcessor(AbstractPdfProcessor):
    @property
    def task_type(self) -> TaskType:
        return TaskType.preview_pdf

    @property
    def task_data(self) -> TaskData:
        return TaskData(_("Preview"), PreviewPdfData)

    @property
    def handler(self) -> CallbackQueryHandler:
        return CallbackQueryHandler(self.process_file, pattern=PreviewPdfData)

    @asynccontextmanager
    async def process_file_task(self, file_data: FileData) -> AsyncGenerator[FileTaskResult, None]:
        async with self.pdf_service.preview_pdf(file_data.id) as path:
            yield FileTaskResult(path)
