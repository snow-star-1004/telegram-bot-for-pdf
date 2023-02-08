from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from gettext import gettext as _

from telegram.ext import CallbackQueryHandler

from pdf_bot.analytics import TaskType
from pdf_bot.models import FileData, FileTaskResult, TaskData

from .abstract_image_processor import AbstractImageProcessor


class ImageToPdfData(FileData):
    pass


class ImageToPdfProcessor(AbstractImageProcessor):
    @property
    def task_type(self) -> TaskType:
        return TaskType.image_to_pdf

    @property
    def task_data(self) -> TaskData:
        return TaskData(_("To PDF"), ImageToPdfData)

    @property
    def handler(self) -> CallbackQueryHandler:
        return CallbackQueryHandler(self.process_file, pattern=ImageToPdfData)

    @asynccontextmanager
    async def process_file_task(self, file_data: FileData) -> AsyncGenerator[FileTaskResult, None]:
        async with self.image_service.convert_images_to_pdf([file_data]) as path:
            yield FileTaskResult(path)
