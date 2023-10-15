from click.testing import CliRunner

from boosty_parser.command import cli


def test_command_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["-h"])
    assert result.exit_code == 0


def test_command_version():
    runner = CliRunner()
    result = runner.invoke(cli, ["-v"])
    assert result.exit_code == 0
