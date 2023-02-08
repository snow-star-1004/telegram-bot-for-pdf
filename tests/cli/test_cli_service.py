import shlex
from subprocess import Popen
from unittest.mock import MagicMock, patch

import pytest

from pdf_bot.cli import CLIService, CLIServiceError
from tests.path_test_mixin import PathTestMixin


class TestCLIService(PathTestMixin):
    PERCENT = 0.1
    MARGIN_SIZE = 10

    def setup_method(self) -> None:
        self.input_path = self.mock_file_path()
        self.output_path = self.mock_file_path()

        self.process = MagicMock(spec=Popen)
        self.process.communicate.return_value = (
            b"0",
            b"1",
        )

        self.popen_patcher = patch("pdf_bot.cli.cli_service.Popen", return_value=self.process)
        self.popen = self.popen_patcher.start()

        self.sut = CLIService()

    def teardown_method(self) -> None:
        self.popen_patcher.stop()

    @pytest.mark.asyncio
    async def test_compress_pdf(self) -> None:
        self.process.returncode = 0
        self.sut.compress_pdf(self.input_path, self.output_path)
        self._assert_compress_command()

    @pytest.mark.asyncio
    async def test_compress_pdf_error(self) -> None:
        self.process.returncode = 1

        with pytest.raises(CLIServiceError):
            self.sut.compress_pdf(self.input_path, self.output_path)

        self._assert_compress_command()

    @pytest.mark.asyncio
    async def test_extract_pdf_images(self) -> None:
        self.process.returncode = 0
        self.sut.extract_pdf_images(self.input_path, self.output_path)
        self._assert_get_pdf_images_command()

    @pytest.mark.asyncio
    async def test_extract_pdf_images_error(self) -> None:
        self.process.returncode = 1

        with pytest.raises(CLIServiceError):
            self.sut.extract_pdf_images(self.input_path, self.output_path)

        self._assert_get_pdf_images_command()

    def _assert_compress_command(self) -> None:
        args = self.popen.call_args.args[0]
        assert args == shlex.split(
            "gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/default "
            f'-dNOPAUSE -dQUIET -dBATCH -sOutputFile="{self.output_path}" '
            f'"{self.input_path}"'
        )

    def _assert_crop_pdf_percentage_command(self) -> None:
        args = self.popen.call_args.args[0]
        assert args == shlex.split(
            f'pdfcropmargins -o "{self.output_path}" "{self.input_path}" -p {self.PERCENT}'
        )

    def _assert_crop_pdf_margin_size_command(self) -> None:
        args = self.popen.call_args.args[0]
        assert args == shlex.split(
            f'pdfcropmargins -o "{self.output_path}" "{self.input_path}" -a {self.MARGIN_SIZE}'
        )

    def _assert_get_pdf_images_command(self) -> None:
        args = self.popen.call_args.args[0]
        assert args == shlex.split(
            f'pdfimages -png "{self.input_path}" "{self.output_path}/images"'
        )
