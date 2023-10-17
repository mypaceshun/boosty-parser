from logging import basicConfig, getLogger

import click
from rich.console import Console
from rich.logging import RichHandler

from boosty_parser import __name__, __version__
from boosty_parser.session import Session

FORMAT = "%(name)s[%(levelname)s]: %(message)s"
basicConfig(level="INFO", format=FORMAT, handlers=[RichHandler()])
logger = getLogger(__name__)


@click.command()
@click.option(
    "-u",
    "--username",
    envvar="BOOSTY_USERNAME",
    help="boosty login username",
    required=True,
)
@click.option(
    "-p",
    "--password",
    envvar="BOOSTY_PASSWORD",
    help="boosty login password",
    required=True,
)
@click.option("--verbose", envvar="BOOSTY_VERBOSE", help="verbose output", is_flag=True)
@click.version_option(__version__, "-v", "--version", package_name=__name__)
@click.help_option("-h", "--help")
def cli(username: str, password: str, verbose: bool):
    console = Console()
    console.rule("[bold red]run script")
    logger.setLevel("INFO")
    if verbose:
        logger.setLevel("DEBUG")
    session = Session()
    session.login(username, password)
    chat_list = session.get_chats(chatid="8")
    for chat in chat_list:
        logger.info(chat.get_text())
