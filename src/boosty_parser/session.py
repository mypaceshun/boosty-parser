from logging import getLogger

import requests
from bs4 import BeautifulSoup, Tag

from boosty_parser import __name__
from boosty_parser.chat import Chat
from boosty_parser.exceptions import ParseError

logger = getLogger(__name__)


class Session:
    BASEURL = "https://rika-n24x.boosty.app"

    def __init__(self, verbose: bool = False):
        self.session = requests.Session()

    def login(self, username: str, password: str):
        login_url, data = self._pre_login()
        logger.debug(f"POST {login_url} {data=}")
        res = self.session.post(login_url, data=data, allow_redirects=True)
        soup = BeautifulSoup(res.text, "xml")
        form_el = soup.find("form")
        if not isinstance(form_el, Tag):
            msg = "login form not found [{login_url}]"
            raise ParseError(msg)
        postdata = self._get_hidden_value_dict(form_el)
        postdata["username"] = username
        postdata["password"] = "xxx"
        logger.debug(f"{postdata=}")
        postdata["password"] = password
        res = self.session.post(res.url, data=postdata, allow_redirects=True)

    def _pre_login(self) -> tuple[str, dict[str, str]]:
        pre_login_url = f"{self.BASEURL}/auth/login"
        logger.debug(f"GET {pre_login_url}")
        res = self.session.get(pre_login_url, allow_redirects=True)
        soup = BeautifulSoup(res.text, "xml")
        form_el = soup.find("form", id="form_sign_in")
        if not isinstance(form_el, Tag):
            msg = "login form not found [{pre_login_url}]"
            raise ParseError(msg)
        login_url = f"{self.BASEURL}{form_el['action']}"
        hidden_value_dict = self._get_hidden_value_dict(form_el)
        logger.debug(f"{hidden_value_dict=}")
        return login_url, hidden_value_dict

    def get_chats(self, chatid: str = "8"):
        chats_url = f"{self.BASEURL}/chats/{chatid}"
        logger.debug(f"POST {chats_url}")
        res = self.session.get(chats_url)
        try:
            chat_list: list[Chat] = Chat.parse_chats(res.text)
        except ParseError as error:
            raise ParseError(f"{error} [{chats_url}]")
        return chat_list

    def _get_hidden_value_dict(self, form_el: Tag) -> dict[str, str]:
        hidden_els = form_el.find_all("input", attrs={"type": "hidden"})
        hidden_value_dict: dict[str, str] = {}
        for hidden_el in hidden_els:
            hidden_value_dict[hidden_el["name"]] = hidden_el["value"]
        return hidden_value_dict
