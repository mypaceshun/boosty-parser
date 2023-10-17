import re
from logging import getLogger

from bs4 import BeautifulSoup, Tag

from boosty_parser import __name__
from boosty_parser.exceptions import ParseError

logger = getLogger(__name__)


class Chat:
    def __init__(
        self,
        message_id: str,
        text: str,
        image_url: str | list[str] | None = None,
        video_url: str | list[str] | None = None,
    ):
        self.message_id = message_id
        self.text = text
        self.image_url = image_url
        self.video_url = video_url

    def get_text(self) -> str:
        str_list: list[str] = []
        if len(self.text) > 0:
            str_list.append(self.text)
        if isinstance(self.image_url, str):
            str_list.append(self.image_url)
        if isinstance(self.image_url, list):
            str_list += self.image_url
        if isinstance(self.video_url, str):
            str_list.append(self.video_url)
        if isinstance(self.video_url, list):
            str_list += self.video_url
        return ",".join(str_list)

    @staticmethod
    def parse_chats(htmltext: str):
        idmatch = re.compile(r"^message-[\d\-_]+$")
        soup = BeautifulSoup(htmltext, "xml")
        messages_el = soup.find("turbo-frame", id="messages")
        if not isinstance(messages_el, Tag):
            msg = "messages not found"
            raise ParseError(msg)
        message_els = messages_el.find_all("div", id=idmatch)
        chat_list: list[Chat] = []
        for message_el in message_els:
            message_id = message_el["id"]

            flex_els = message_el.select("div.flex")
            if len(flex_els) != 2:
                logger.warning(f"flex_els not found {message_el=}, {flex_els=}")
                continue
            content_el = flex_els[0]
            content_body_el = content_el.find("div")
            text = ""
            if isinstance(content_body_el, Tag):
                text_str = content_body_el.get_text()
                if text_str is None:
                    text_str = ""
                text = text_str.strip()

            image_url = None
            image_el = content_el.find("img")
            if isinstance(image_el, Tag):
                image_url = image_el["src"]

            video_url = None
            video_el = content_el.find("video")
            if isinstance(video_el, Tag):
                video_url = video_el["src"]

            chat_list.append(
                Chat(
                    message_id=message_id,
                    text=text,
                    image_url=image_url,
                    video_url=video_url,
                )
            )
        return chat_list
