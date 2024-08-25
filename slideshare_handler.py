import os
from telebot import types, TeleBot
import re
import requests


def slideshare(bot: TeleBot, message: types.Message):
    chat_id = message.from_user.id
    take_link = bot.send_message(
        chat_id,
        "<b>Send your slidehsare document link.</b>\n\neg. <code>https://www.slideshare.net/slideshow/networks-classification/42998147</code>",
        parse_mode="HTML",
    )
    bot.register_next_step_handler(
        take_link, lambda message: step_slideshare(message, bot)
    )


def step_slideshare(message: types.Message, bot: TeleBot):
    chat_id = message.from_user.id

    pattern = r"https:\/\/www\.slideshare\.net\/slideshow\/[a-zA-Z0-9\-]+\/\d+"
    match = re.match(pattern, message.text.strip())
    if not match:
        bot.send_message(
            chat_id,
            "Your document link is not valid. Kindly recheck.\n\neg. <code>https://www.slideshare.net/slideshow/networks-classification/42998147</code>",
            parse_mode="HTML",
        )
    else:
        doc_url = message.text.strip()
        try:
            doc_id = int(doc_url.split("/")[-1])
        except:
            bot.send_message(
                chat_id,
                "Your document link is not valid. Kindly recheck.\n\neg. <code>https://www.slideshare.net/slideshow/networks-classification/42998147</code>",
                parse_mode="HTML",
            )

        msg = bot.send_message(chat_id, "Downloading...")
        try:
            main_req = requests.get(
                doc_url,
                headers={
                    "accept": "application/json, text/plain, */*",
                    "accept-encoding": "gzip, deflate, br, zstd",
                    "accept-language": "en-GB,en;q=0.8",
                    "content-length": "0",
                    "cookie": "browser_id=df6fd3e1-cdfe-4226-84ee-e958d8dd2212; country_code=GH; flash=BAh7BkkiC25vdGljZQY6BkVGMA%3D%3D--b8587ccce3f7c9553ab2422163b5d1964e1909e1; _cookie_id=eb7db9b6d45d88742df54df32908b37c; logged_in=MjU4NDE3ODI5--32a0449a9f4e4841be80bfff196096d20462e675",
                    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
                },
            )
        except:
            bot.edit_message_text("error downloading. Kindly restart.", chat_id, msg.id)
        else:
            f = main_req.text.split('"downloadKey":"')[1]
            down_key = f.split('"')[0]

            try:
                token_req = requests.get(
                    "https://www.slideshare.net/csrf_token",
                    headers={
                        "accept": "application/json, text/plain, */*",
                        "accept-encoding": "gzip, deflate, br, zstd",
                        "accept-language": "en-GB,en;q=0.8",
                        "content-length": "0",
                        "cookie": "browser_id=df6fd3e1-cdfe-4226-84ee-e958d8dd2212; country_code=GH; _cookie_id=eb7db9b6d45d88742df54df32908b37c; logged_in=MjU4NDE3ODI5--32a0449a9f4e4841be80bfff196096d20462e675; split=%7B%22download_on_slide%22%3A%22control%22%7D; flash=BAh7DEkiC25vdGljZQY6BkVGMEkiDHdhcm5pbmcGOwBGMEkiDG1lc3NhZ2UGOwBGMEkiDHN1Y2Nlc3MGOwBGMEkiCmVycm9yBjsARjBJIg5wZXJtYW5lbnQGOwBGMEkiEW1vZGFsX25vdGljZQY7AEYw--4d44737d8a4b0fb4535d68df321d9eff6a31ba96; _uv_id=78790485",
                        "origin": "https://www.slideshare.net",
                        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
                    },
                )
            except:
                bot.edit_message_text(
                    "error downloading. Kindly restart.", chat_id, msg.id
                )
            else:
                token = token_req.json()["csrf_token"]

                try:
                    down_url_req = requests.post(
                        f"https://www.slideshare.net/slideshow/download?download_key={down_key}&slideshow_id={doc_id}",
                        headers={
                            "accept": "application/json, text/plain, */*",
                            "accept-encoding": "gzip, deflate, br, zstd",
                            "accept-language": "en-GB,en;q=0.8",
                            "content-length": "0",
                            "cookie": "browser_id=df6fd3e1-cdfe-4226-84ee-e958d8dd2212; country_code=GH; _cookie_id=eb7db9b6d45d88742df54df32908b37c; logged_in=MjU4NDE3ODI5--32a0449a9f4e4841be80bfff196096d20462e675; split=%7B%22download_on_slide%22%3A%22control%22%7D; flash=BAh7DEkiC25vdGljZQY6BkVGMEkiDHdhcm5pbmcGOwBGMEkiDG1lc3NhZ2UGOwBGMEkiDHN1Y2Nlc3MGOwBGMEkiCmVycm9yBjsARjBJIg5wZXJtYW5lbnQGOwBGMEkiEW1vZGFsX25vdGljZQY7AEYw--4d44737d8a4b0fb4535d68df321d9eff6a31ba96; _uv_id=78790485",
                            "origin": "https://www.slideshare.net",
                            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
                            "x-csrf-token": token,
                        },
                    )
                except:
                    bot.edit_message_text(
                        "error downloading. Kindly restart.", chat_id, msg.id
                    )
                else:
                    down_url_escaped = down_url_req.json()["url"]
                    down_url = down_url_escaped.encode("utf-8").decode("unicode_escape")

                    try:
                        last_req = requests.get(
                            down_url,
                            headers={
                                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                                "accept-encoding": "gzip, deflate, br, zstd",
                                "accept-language": "en-GB,en;q=0.9",
                                "connection": "keep-alive",
                                "host": "slideshare-downloads.s3.amazonaws.com",
                                "referer": "https://www.slideshare.net/",
                                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
                            },
                        )
                    except:
                        bot.edit_message_text(
                            "error downloading. Kindly restart.", chat_id, msg.id
                        )
                    else:
                        file_name = doc_url.split("/")[4]
                        with open(f"{file_name}.pdf", "wb") as file:
                            file.write(last_req.content)

                        with open(f"{file_name}.pdf", "rb") as document:
                            bot.send_document(chat_id, document)

                        bot.edit_message_text("Download Complete ✅", chat_id, msg.id)
                        os.remove(f"{file_name}.pdf")
