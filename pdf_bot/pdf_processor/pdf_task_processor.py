from pdf_bot.file_processor import AbstractFileTaskProcessor

from .abstract_pdf_processor import AbstractPdfProcessor


class PdfTaskProcessor(AbstractFileTaskProcessor):
    @property
    def processor_type(self) -> type[AbstractPdfProcessor]:
        return AbstractPdfProcessor
