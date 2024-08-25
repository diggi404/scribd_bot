import os
from telebot import types, TeleBot
import re
import requests


def scribd(bot: TeleBot, message: types.Message, book_dict: dict):
    chat_id = message.from_user.id
    take_link = bot.send_message(
        chat_id,
        "<b>Send your scribd document link.</b>\n\neg. <code>https://www.scribd.com/document/519698629/the-seven-husbands-of-evelyn-hugo-a-novel</code>",
        parse_mode="HTML",
    )
    bot.register_next_step_handler(
        take_link, lambda message: step_scribd(message, bot, book_dict)
    )


def step_scribd(message: types.Message, bot: TeleBot, book_dict: dict):
    chat_id = message.from_user.id

    pattern = r"https:\/\/www\.scribd\.com\/document\/\d+\/[a-zA-Z0-9\-]+"
    match = re.match(pattern, message.text.strip())
    if not match:
        bot.send_message(
            chat_id,
            "Your document link is not valid. Kindly recheck.\n\neg. <code>https://www.scribd.com/document/519698629/the-seven-husbands-of-evelyn-hugo-a-novel</code>",
            parse_mode="HTML",
        )
    else:
        try:
            doc_id = message.text.strip().split("/")[4]
        except:
            bot.send_message(
                chat_id,
                "Your document link is not valid. Kindly recheck.\n\neg. <code>https://www.scribd.com/document/519698629/the-seven-husbands-of-evelyn-hugo-a-novel</code>",
                parse_mode="HTML",
            )
        else:
            doc_lookup_url = (
                f"https://www.scribd.com/doc-page/download-receipt-modal-props/{doc_id}"
            )
            msg = bot.send_message(chat_id, "Verifying link...")
            try:
                req = requests.get(
                    doc_lookup_url,
                    headers={
                        "accept": "*/*",
                        "accept-language": "en-GB,en;q=0.5",
                        "cookie": "scribd_ubtc=u%3Db1e29dd2-eebe-4537-b941-34da20465a36%26h%3DNpPs7DXffEFXKctp7wkMSiSDohUfBciKAjLmpEA0OpM%3D; _fs_sample_user=false; osano_consentmanager_uuid=3d144ae3-274a-4a1c-a811-8c802aa7dbd1; osano_consentmanager=yWoJTiV4XHQxve705lD6oYwLowCkmNI4MidVshKGLFrKuedJ1RfHMoXAVYLmezfd6T4uO3Ktm4Tfv01VwuTI28_2fAO9wsDyHFYR5jgBNCHXzvHGDeLpur7c7xeNyM21NvjgMFiKbJP_PFyDZBfDqRxuLtH_iSVQHKOgNUnmw25uFIfzfeKiAsKdEbVSHoSwHetBFGgTsV81iC64UJ4Npdj4Ckwp1dZyyFiRjS-8HmFDcaPA4CIsD1uz4Pt_8XFcYT6CLPLBqPSqdZTRDsHJWL2twO3Pcp93hGaGWM66httF-LpfqPVZrwd1oFs01Z8pyBKJZCx5RzM_EtN46pCEQ-CCz1Kn49rsrq-GrYWRIKq862PNQi-4Xs1ge7jP4EJPsD6YpqFuZz_DVClKWlvK03NwjOIbtrDORHoQAI9XxNY1GOB1TPrnde2OGKyWFlC-jHDj-34c_BVf5FwQRKjTAJA7sJiIwooFKcjhnyil86ysuxTl7MYE97xXgoNoP30lLMGTl7NRbFU989viFNYatFCcO675vc63lfXxzKyGmA8LyaiA4NTytp1Ulm78jeHamcJg0_x66-6Zbox5obK-CzPONVUVCi-8; _scribd_user_id=Nzc3NzM0NTE1--fb6e8059aadd0fe2e1cd7ce425d6dd981032d677; annual_upsell_trialer_cookie=seen; __CJ_parchive_offer=%7B%22avail_height%22%3A790%2C%22avail_width%22%3A868%2C%22color_depth%22%3A30%2C%22cookie_uuid%22%3A%222dcc0944-3c13-4311-84e5-47a3f2044fbe%22%2C%22cookies_enabled%22%3Atrue%2C%22hardware_concurrency%22%3A7%2C%22height%22%3A790%2C%22java_enabled%22%3Afalse%2C%22left%22%3A8%2C%22max_touch_points%22%3A0%2C%22orientation%22%3A%22landscape-primary%22%2C%22pixel_depth%22%3A30%2C%22platform%22%3A%22MacIntel%22%2C%22referrer%22%3A%22%22%2C%22time_zone%22%3A%22America%2FNew_York%22%2C%22top%22%3A3%2C%22width%22%3A868%7D; __CJ_DOC_PAGE_SUBNAV_VARIANT_TRACKED=true; __CJ_nwt=%7B%22nw2624%22%3A6648%2C%22nw2868%22%3A7327%2C%22nw3022%22%3A7863%2C%22nw3008%22%3A7820%7D; _scribd_session=Kzg1RUJZYlM5ZzhuZS92NitrblJqRU55ZDZHa0FMd3hHZ1Z2K1I1Tis0Nm1WS1doUzhLRHJuT040T2tBYUQ2NEgxWVlrblVMVXVuQjlzOHVRMFBEcEFNRGJvM1YzSUNMckxheThsTWk3RjdON0EzdWxYWUYvaFNPUnlrNnYrd3cyK2NQRXZ6K0hXeWxNK2RhVWxnRVFpQkYwVHFBeHpZbTh1Y3BsUUpWam8wcFlsSmwwRUpKUTk2bWtDSE5mRVcyNlNLSlJqZjFZUW8wclBraUFOaWJGMVRmakd4RlJjWEZjNkhpQWhtdHR4N1BmYU5PMnpZS2s2NEpNbVcvS1B0TExNQ2pWWlJFM3hEYk9lOHBVN0Fvb3krZlV5Z2hhRmozNWFqeWh0SUVzOWVrQS9MY3pkS0Y5cG5udUl1RE53MDR4bFI5MHB0bjZLUnNSSFRyRlY4NEQ3UHBGSzZRWTBDQ1Q0dTkwQ0Z4dmhXWXJtcVplUHRyejV6d1NwZitZZHEyWVM4RDhiZm9sTERKWnI4VzRPN3JnWHk5TytOWDBqbHdhSldyaUVObTJjMHZXNGo2TXBXbENaTElURkxFNm1HOGFtYXYzVUdnSVlUNHgrdjJSMFlBNWc9PS0tOWplZThpZG1LUmpNRi9JL0hYY0JYdz09--08b21238bfd3b3248e5b5258c5d47e7f7486de8d; _dd_s=rum=0&expire=1724591719112",
                        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
                        "x-requested-with": "XMLHttpRequest",
                    },
                )
            except:
                bot.send_message(
                    chat_id,
                    "error checking link. Kindly restart.",
                )
            else:
                doc_key = req.json()["document"]["access_key"]
                doc_img = req.json()["document"]["retina_image_url"]
                title = req.json()["document"]["title"]
                author = req.json()["document"]["author"]["name"]
                book_dict[chat_id] = title

                try:
                    img_req = requests.get(doc_img)
                except:
                    bot.send_message(
                        chat_id,
                        "error checking link. Kindly restart.",
                    )
                else:
                    with open(f"{doc_id}.jpg", "wb") as file:
                        file.write(img_req.content)

                    d_markup = types.InlineKeyboardMarkup()
                    d_btn = types.InlineKeyboardButton(
                        "Download ⬇️", callback_data=f"scribd down_{doc_id}_{doc_key}"
                    )
                    d_markup.add(d_btn)
                    bot.delete_message(chat_id, msg.id)
                    with open(f"{doc_id}.jpg", "rb") as photo:
                        bot.send_photo(
                            chat_id,
                            photo,
                            f"Title`: <b>{title}</b>\nAuthor: <b>{author}</b>",
                            reply_markup=d_markup,
                            parse_mode="HTML",
                        )
                    os.remove(f"{doc_id}.jpg")


def scribd_download(
    bot: TeleBot, chat_id: int, msg_id: int, button_data: str, book_dict: dict
):
    doc_id = button_data.split("_")[1]
    doc_key = button_data.split("_")[2]
    msg = bot.send_message(chat_id, "Downloading...")
    try:
        req = requests.get(
            f"https://www.scribd.com/document_downloads/{doc_id}/?secret_password={doc_key}&extension=pdf",
            headers={
                "accept": "*/*",
                "accept-language": "en-GB,en;q=0.5",
                "cookie": "scribd_ubtc=u%3Db1e29dd2-eebe-4537-b941-34da20465a36%26h%3DNpPs7DXffEFXKctp7wkMSiSDohUfBciKAjLmpEA0OpM%3D; _fs_sample_user=false; osano_consentmanager_uuid=3d144ae3-274a-4a1c-a811-8c802aa7dbd1; osano_consentmanager=yWoJTiV4XHQxve705lD6oYwLowCkmNI4MidVshKGLFrKuedJ1RfHMoXAVYLmezfd6T4uO3Ktm4Tfv01VwuTI28_2fAO9wsDyHFYR5jgBNCHXzvHGDeLpur7c7xeNyM21NvjgMFiKbJP_PFyDZBfDqRxuLtH_iSVQHKOgNUnmw25uFIfzfeKiAsKdEbVSHoSwHetBFGgTsV81iC64UJ4Npdj4Ckwp1dZyyFiRjS-8HmFDcaPA4CIsD1uz4Pt_8XFcYT6CLPLBqPSqdZTRDsHJWL2twO3Pcp93hGaGWM66httF-LpfqPVZrwd1oFs01Z8pyBKJZCx5RzM_EtN46pCEQ-CCz1Kn49rsrq-GrYWRIKq862PNQi-4Xs1ge7jP4EJPsD6YpqFuZz_DVClKWlvK03NwjOIbtrDORHoQAI9XxNY1GOB1TPrnde2OGKyWFlC-jHDj-34c_BVf5FwQRKjTAJA7sJiIwooFKcjhnyil86ysuxTl7MYE97xXgoNoP30lLMGTl7NRbFU989viFNYatFCcO675vc63lfXxzKyGmA8LyaiA4NTytp1Ulm78jeHamcJg0_x66-6Zbox5obK-CzPONVUVCi-8; _scribd_user_id=Nzc3NzM0NTE1--fb6e8059aadd0fe2e1cd7ce425d6dd981032d677; annual_upsell_trialer_cookie=seen; __CJ_parchive_offer=%7B%22avail_height%22%3A790%2C%22avail_width%22%3A868%2C%22color_depth%22%3A30%2C%22cookie_uuid%22%3A%222dcc0944-3c13-4311-84e5-47a3f2044fbe%22%2C%22cookies_enabled%22%3Atrue%2C%22hardware_concurrency%22%3A7%2C%22height%22%3A790%2C%22java_enabled%22%3Afalse%2C%22left%22%3A8%2C%22max_touch_points%22%3A0%2C%22orientation%22%3A%22landscape-primary%22%2C%22pixel_depth%22%3A30%2C%22platform%22%3A%22MacIntel%22%2C%22referrer%22%3A%22%22%2C%22time_zone%22%3A%22America%2FNew_York%22%2C%22top%22%3A3%2C%22width%22%3A868%7D; __CJ_DOC_PAGE_SUBNAV_VARIANT_TRACKED=true; __CJ_nwt=%7B%22nw2624%22%3A6648%2C%22nw2868%22%3A7327%2C%22nw3022%22%3A7863%2C%22nw3008%22%3A7820%7D; _scribd_session=Kzg1RUJZYlM5ZzhuZS92NitrblJqRU55ZDZHa0FMd3hHZ1Z2K1I1Tis0Nm1WS1doUzhLRHJuT040T2tBYUQ2NEgxWVlrblVMVXVuQjlzOHVRMFBEcEFNRGJvM1YzSUNMckxheThsTWk3RjdON0EzdWxYWUYvaFNPUnlrNnYrd3cyK2NQRXZ6K0hXeWxNK2RhVWxnRVFpQkYwVHFBeHpZbTh1Y3BsUUpWam8wcFlsSmwwRUpKUTk2bWtDSE5mRVcyNlNLSlJqZjFZUW8wclBraUFOaWJGMVRmakd4RlJjWEZjNkhpQWhtdHR4N1BmYU5PMnpZS2s2NEpNbVcvS1B0TExNQ2pWWlJFM3hEYk9lOHBVN0Fvb3krZlV5Z2hhRmozNWFqeWh0SUVzOWVrQS9MY3pkS0Y5cG5udUl1RE53MDR4bFI5MHB0bjZLUnNSSFRyRlY4NEQ3UHBGSzZRWTBDQ1Q0dTkwQ0Z4dmhXWXJtcVplUHRyejV6d1NwZitZZHEyWVM4RDhiZm9sTERKWnI4VzRPN3JnWHk5TytOWDBqbHdhSldyaUVObTJjMHZXNGo2TXBXbENaTElURkxFNm1HOGFtYXYzVUdnSVlUNHgrdjJSMFlBNWc9PS0tOWplZThpZG1LUmpNRi9JL0hYY0JYdz09--08b21238bfd3b3248e5b5258c5d47e7f7486de8d; _dd_s=rum=0&expire=1724591719112",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
                "x-requested-with": "XMLHttpRequest",
            },
            allow_redirects=True,
        )
    except:
        bot.edit_message_text(
            "Error downloading document. Kindly redownload.", chat_id, msg.id
        )
    else:
        title = book_dict[chat_id]
        with open(f"{title}.pdf", "wb") as file:
            file.write(req.content)

        with open(f"{title}.pdf", "rb") as document:
            bot.send_document(chat_id, document)
        bot.edit_message_reply_markup(chat_id, msg_id, reply_markup=None)
        bot.edit_message_text("Download Complete ✅", chat_id, msg.id)
        os.remove(f"my_book.pdf")
