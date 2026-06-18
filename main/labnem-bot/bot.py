import json
import os
import random
import re
import asyncio
import tempfile
import zipfile
import shutil
import urllib.request
import threading
from datetime import datetime
from highrise import BaseBot
from highrise.models import SessionMetadata, User, Position, AnchorPosition, CurrencyItem, Item
from main.emotes import all_emote_list, DANCE_MAP, DANCE_NAME_MAP
import sounddevice as sd
import soundfile as sf
import numpy as np
from pycaw.pycaw import AudioUtilities, EDataFlow, ERole

DATA_FILE = "data.json"

MAX_SONG_DURATION = 480

LANG = {
    "tr": {
        "bot_started": "Labnem bot başlatıldı!",
        "follow": "seni takip ediyorum!",
        "stop": "duruyorum.",
        "not_following": "kimseyi takip etmiyorum.",
        "pinned": "bulunduğum yere sabitlendim!",
        "unpinned": "sabitleme kaldırıldı.",
        "pin_help": "Kullanım: !pin (bulunduğun yere sabitler)",
        "not_owner": "bu komutu sadece oda sahibi kullanabilir!",
        "no_permission": "yetkiniz yok!",
        "invalid_dance": "Geçersiz dans! Kullanılabilir: {dances}",
        "dance_list_header": "Danslar (Sayfa {page}/{total})",
        "all_dance_done": "{count} kişi {dance} dansı yaptı!",
        "outfit_changed": "bot rastgele {count} parça giydirildi!",
        "inventory_empty": "Envanter boş.",
        "inventory_error": "Kıyafetler alınamadı.",
        "outfit_error": "Kıyafet değiştirilemedi: {msg}",
        "lang_set": "Dil Türkçe olarak ayarlandı!",
        "lang_en": "Dil İngilizce olarak ayarlandı!",
        "tele_created": "Teleport '{name}' oluşturuldu!",
        "tele_removed": "Teleport '{name}' kaldırıldı!",
        "tele_not_found": "Teleport '{name}' bulunamadı.",
        "tele_list": "Teleportlar: {list}",
        "tele_no_teleports": "Hiç teleport yok.",
        "teleported": "{user} {name} konumuna ışınlandı!",
        "teleported_all": "herkes {name} konumuna ışınlandı!",
        "tele_vip_set": "Teleport '{name}' VIP oldu!",
        "tele_vip_unset": "Teleport '{name}' VIP kaldırıldı!",
        "tele_vip_only": "Bu teleport sadece VIP üyeler içindir!",
        "tele_name_req": "Teleport adı gerekli. Kullanım: !create tele <ad>",
        "boost_started": "Oda boostu başlatılıyor...",
        "boost_success": "Oda boostu başarıyla satın alındı! ({count}x)",
        "boost_fail": "Boost satın alınamadı: {reason}",
        "wallet_info": "Cüzdanımda {gold} altın var.",
        "wallet_no_gold": "Cüzdanımda altın yok.",
        "tip_summary_title": "Bahşiş Özeti:",
        "tip_summary_total": "Toplam harcanan altın: {gold}",
        "tip_summary_people": "Bahşiş veren kişi: {count}",
        "tip_summary_none": "Henüz bahşiş alınmadı.",
        "tip_thanks_small": "Teşekkürler {user} bahşiş için!",
        "tip_thanks_big": "Teşekkürler {user} cömert {amount} altın bahşişi için!",
        "tip_leaderboard": "En Çok Bahşiş Verenler:\n{list}",
        "tip_get": "{user} toplam {amount} altın bahşiş vermiş.",
        "tip_get_none": "{user} henüz bahşiş vermemiş.",
        "help_title": "Kullanılabilir Komutlar:",
        "help_music": "-p <şarkı/tür> | -up | -like | !queue | !skip | !shuffle | !repeat | !mylib",
        "mic_on": "Mikrofon {user} için açıldı!",
        "mic_off": "Mikrofon {user} için kapatıldı!",
        "dj_not_found": "{user} bulunamadı veya rolde değil.",
        "role_created": "Rol '{role}' oluşturuldu!",
        "role_deleted": "Rol '{role}' silindi!",
        "role_given": "{role} rolü {user}'e verildi!",
        "role_list": "Roller: {list}",
        "role_users": "{role} rolündekiler: {list}",
        "role_no_users": "{role} rolünde kimse yok.",
        "no_roles": "Hiç rol yok.",
        "vip_added": "{user} VIP yapıldı!",
        "vip_removed": "{user} VIP'likten çıkarıldı!",
        "vip_list": "VIP Listesi: {list}",
        "no_vip": "Hiç VIP yok.",
        "not_vip": "{user} VIP değil.",
        "already_vip": "{user} zaten VIP.",
        "sayso_loop": "sayso döngüsü başlatıldı!",
        "loop_stop_emote": "Duygu döngüsü durduruldu.",
        "custom_emote": "Özel duygu: {emotes}",
        "custom_help": "Kullanım: !custom <emote1> <emote2> ...",
        "autoreact_on": "Otomatik tepki açıldı!",
        "autoreact_off": "Otomatik tepki kapatıldı!",
        "bot_emote_set": "Bot döngü duygusu: {emote}",
        "alert_set": "Uyarı mesajı: {msg}",
        "thank_set": "Teşekkür mesajı: {msg}",
        "save_outfit": "Kıyafet #{num} kaydedildi!",
        "load_outfit": "Kıyafet #{num} yüklendi!",
        "no_outfit": "Kıyafet #{num} bulunamadı.",
        "copy_outfit": "Bot {user} kıyafetini kopyaladı!",
        "bring": "{user} yanıma ışınlandı!",
        "bring_all": "Herkes yanıma ışınlandı!",
        "switch_done": "Yer değiştirildi!",
        "goto": "{user}'e gidiyorum!",
        "setpos_done": "Bot konumu ayarlandı!",
        "setjoin_set": "Katılma mesajı: {msg}",
        "setleave_set": "Ayrılma mesajı: {msg}",
        "setvipjoin_set": "VIP katılma mesajı ayarlandı",
        "setvipleave_set": "VIP ayrılma mesajı ayarlandı",
        "spam_warn": "Çok fazla! Maks: 5",
        "spam_done": "Mesaj {count} kez gönderildi!",
        "8ball_responses": ["Kesinlikle.", "Evet.", "Hayır.", "Belki.", "Pek değil.", "Kesinlikle hayır.", "Olabilir.", "Bence evet."],
        "8ball_result": "{question} -> {answer}",
        "roast_list": ["{user} yeteneklerin... yok.", "{user} aynada kendine baktığında ne görüyorsun?", "{user} çok özelsin, herkes gibi.", "{user} zeka seviyen oda sıcaklığına eşit.", "{user} seni seviyorum derdim ama yalan söyleyemem."],
        "love_match": "{user1} \u2764\ufe0f {user2} = Aşk: {score}%!",
        "match_result": "{user} için en iyi eş: {match} ({score}%)",
        "fight_start": "{user1} vs {user2} - KAVGA!",
        "duel_start": "{user1} ve {user2} düello başladı!",
        "duel_result": "{winner} düelloyu kazandı!",
        "muted": "{user} susturuldu!",
        "unmuted": "{user} susturulması kaldırıldı!",
        "kicked": "{user} odadan atıldı!",
        "banned": "{user} odadan yasaklandı!",
        "flashmode_on": "Işınlanma modu açık! Bir yere tıkla ışınlan.",
        "flashmode_off": "Işınlanma modu kapalı.",
        "welcome_msg": "Hoş geldin {user}!",
        "loop_started": "Döngülü mesaj başlatıldı: {msg}",
        "loop_stopped": "Döngülü mesaj durduruldu.",
        "welcome_set": "Hoş geldin mesajı: {msg}",
        "welcome_disabled": "Hoş geldin mesajı devre dışı.",
        "coin_flip": "Yazı tura: {result}",
        "coin_heads": "Yazı",
        "coin_tails": "Tura",
        "dice_roll": "Zar: {result}",
        "choose_result": "Ben {choice} seçtim!",
        "rate_result": "{user} puanım: {score}/10 {emoji}",
        "subscribe": "Abone oldunuz!",
        "unsubscribe": "Abonelikten çıktınız!",
        "already_sub": "Zaten abonesiniz.",
        "not_sub": "Abone değilsiniz.",
        "broadcast": "Duyuru: {msg}",
        "sub_whisper_tr": "Abone oldunuz! Benden haber bekleyin. 🙏",
        "sub_whisper_en": "You are subscribed! Wait for news from me. 🙏",
        "already_sub_whisper_tr": "Zaten abonesiniz!",
        "already_sub_whisper_en": "You are already subscribed!",
        "invite_all": "Tüm abonelere davet gönderildi! ({count} kişi)",
        "invite_all_en": "Invite sent to all subscribers! ({count} people)",
        "sub_list": "Aboneler: {count} kişi",
        "no_subs": "Hiç abone yok.",
        "invite_sent": "Davet gönderildi!",
        "tip_received": "Bahşiş: {user} -> {amount} altın",
        "tip_sent": "{user}'e {amount} altın gönderildi!",
        "tip_self": "Kendine bahşiş gönderemezsin!",
        "tip_no_gold": "Yeterli altın yok!",
        "insufficient_funds": "Yetersiz bakiye!",
        "only_token_bought": "Token alındı ancak uygulanamadı.",
        "voice_bought": "Ses süresi satın alındı!",
        "dancefloor_corners": "Dans pisti köşeleri ayarlandı!",
        "dancefloor_emote": "Dans pisti: '{emote}'",
        "music_queue_title": "Müzik Sırası ({count} şarkı):",
        "music_queue_empty": "Sırada şarkı yok.",
        "music_now_playing": "Şu Anda: {song}",
        "music_added": "#{num} {song} sıraya eklendi!",
        "music_removed": "#{num} sıradan çıkarıldı!",
        "music_skipped": "Atlandı! Sıradaki: {song}",
        "music_cleared": "Sıra temizlendi!",
        "music_upvoted": "'{song}' öne alındı! ({count} oy)",
        "music_liked": "'{song}' beğenildi! ({count} oy)",
        "music_unliked": "'{song}' beğenisi kaldırıldı!",
        "music_played": "'{song}' çalınıyor!",
        "music_event_started": "Müzik yarışması başladı! {duration} dakika.",
        "music_event_ended": "Müzik yarışması sona erdi!",
        "music_event_status": "{remaining} dk kaldı, {participants} kişi katılıyor.",
        "music_event_winners": "Kazananlar:\n{list}",
        "music_event_no_winners": "Kazanan yok.",
        "music_saved": "'{song}' kütüphanene kaydedildi!",
        "music_library": "Kütüphanen ({count}): {list}",
        "music_library_empty": "Kütüphanen boş.",
        "music_removed_lib": "'{song}' kütüphanenden çıkarıldı!",
        "music_from_lib": "Kütüphanenden '{song}' çalınıyor!",
        "music_filter_set": "Efekt: {effect}",
        "music_filter_cleared": "Efekt kaldırıldı.",
        "shuffle_on": "Karışık mod açık!",
        "shuffle_off": "Karışık mod kapalı!",
        "repeat_on": "Tekrar modu açık!",
        "repeat_off": "Tekrar modu kapalı!",
        "music_not_in_queue": "Bu numara sırada yok.",
        "music_no_current": "Çalan şarkı yok.",
        "music_help": "-p <şarkı/tür> | -up | -like | !queue | !add | !skip | !shuffle | !repeat | !voice | !mylib | !filter | !event",
        "voice_on": "Sesli mod açık! Müzik sesli yayınlanacak.",
        "voice_off": "Sesli mod kapalı.",
        "voice_error": "Sesli sohbet hatası: {msg}",
        "music_voice_help": "Sesli Müzik: !voice",
        "time_limit": "Maksimum şarkı süresi: {limit} saniye",
        "invalid_args": "Geçersiz argümanlar!",
        "heart_sent": "Kalp gönderildi!",
        "emote_list_title": "Kullanılabilir Danslar:",
        "loop_stopped_all": "Tüm döngüler durduruldu.",
        "welcome_role": "Hoş geldin rolü ayarlandı.",
        "access_on": "Herkes erişim açık!",
        "access_off": "Herkes erişim kapalı!",
        "bot_already_following": "Zaten seni takip ediyorum!",
        "follow_toggle_on": "Takip açıldı!",
        "follow_toggle_off": "Takip kapatıldı!",
    },
    "en": {
        "bot_started": "Labnem bot started!",
        "follow": "I am following you!",
        "stop": "I am stopping.",
        "not_following": "Not following anyone.",
        "pinned": "Pinned to my location!",
        "unpinned": "Unpinned, I can move now.",
        "pin_help": "Usage: !pin (pins at your location)",
        "not_owner": "only the room owner can use this!",
        "no_permission": "no permission!",
        "invalid_dance": "Invalid dance! Available: {dances}",
        "dance_list_header": "Dances (Page {page}/{total})",
        "all_dance_done": "{count} people danced {dance}!",
        "outfit_changed": "bot dressed in {count} random items!",
        "inventory_empty": "Inventory empty.",
        "inventory_error": "Could not get inventory.",
        "outfit_error": "Could not change outfit: {msg}",
        "lang_set": "Language set to Turkish!",
        "lang_en": "Language set to English!",
        "tele_created": "Teleport '{name}' created!",
        "tele_removed": "Teleport '{name}' removed!",
        "tele_not_found": "Teleport '{name}' not found.",
        "tele_list": "Teleports: {list}",
        "tele_no_teleports": "No teleports.",
        "teleported": "{user} teleported to {name}!",
        "teleported_all": "everyone teleported to {name}!",
        "tele_vip_set": "Teleport '{name}' set as VIP!",
        "tele_vip_unset": "Teleport '{name}' VIP removed!",
        "tele_vip_only": "This teleport is VIP only!",
        "tele_name_req": "Teleport name required. Usage: !create tele <name>",
        "boost_started": "Starting room boost...",
        "boost_success": "Room boost purchased! ({count}x)",
        "boost_fail": "Boost failed: {reason}",
        "wallet_info": "I have {gold} gold.",
        "wallet_no_gold": "No gold in wallet.",
        "tip_summary_title": "Tip Summary:",
        "tip_summary_total": "Total gold spent: {gold}",
        "tip_summary_people": "People who tipped: {count}",
        "tip_summary_none": "No tips yet.",
        "tip_thanks_small": "Thanks {user} for the tip!",
        "tip_thanks_big": "Thanks {user} for the generous {amount} gold tip!",
        "tip_leaderboard": "Top Tippers:\n{list}",
        "tip_get": "{user} tipped {amount} gold total.",
        "tip_get_none": "{user} hasn't tipped yet.",
        "help_title": "Available Commands:",
        "help_music": "-p <song/genre> | -up | -like | !queue | !skip | !shuffle | !repeat | !mylib",
        "mic_on": "Mic on for {user}!",
        "mic_off": "Mic off for {user}!",
        "dj_not_found": "{user} not found or not in role.",
        "role_created": "Role '{role}' created!",
        "role_deleted": "Role '{role}' deleted!",
        "role_given": "Role '{role}' given to {user}!",
        "role_list": "Roles: {list}",
        "role_users": "Users in '{role}': {list}",
        "role_no_users": "No users in '{role}'.",
        "no_roles": "No roles.",
        "vip_added": "{user} is now VIP!",
        "vip_removed": "{user} removed from VIP!",
        "vip_list": "VIP List: {list}",
        "no_vip": "No VIP members.",
        "not_vip": "{user} is not VIP.",
        "already_vip": "{user} is already VIP.",
        "sayso_loop": "sayso loop started!",
        "loop_stop_emote": "Emote loop stopped.",
        "custom_emote": "Custom emote: {emotes}",
        "custom_help": "Usage: !custom <emote1> <emote2> ...",
        "autoreact_on": "Auto-react on!",
        "autoreact_off": "Auto-react off!",
        "bot_emote_set": "Bot loop emote: {emote}",
        "alert_set": "Alert message: {msg}",
        "thank_set": "Thank message: {msg}",
        "save_outfit": "Outfit #{num} saved!",
        "load_outfit": "Outfit #{num} loaded!",
        "no_outfit": "Outfit #{num} not found.",
        "copy_outfit": "Bot copied {user}'s outfit!",
        "bring": "{user} brought to me!",
        "bring_all": "Everyone brought to me!",
        "switch_done": "Switched places!",
        "goto": "Going to {user}!",
        "setpos_done": "Bot position set!",
        "setjoin_set": "Join message: {msg}",
        "setleave_set": "Leave message: {msg}",
        "setvipjoin_set": "VIP join message set",
        "setvipleave_set": "VIP leave message set",
        "spam_warn": "Too many! Max: 5",
        "spam_done": "Message sent {count} times!",
        "8ball_responses": ["Definitely.", "Yes.", "No.", "Maybe.", "Not really.", "Definitely not.", "Could be.", "I think so."],
        "8ball_result": "{question} -> {answer}",
        "roast_list": ["{user} your talents are... non-existent.", "{user} what do you see in the mirror?", "{user} you're so special, just like everyone else.", "{user} your IQ is room temperature.", "{user} I wanted to say I love you but I can't lie."],
        "love_match": "{user1} \u2764\ufe0f {user2} = Love: {score}%!",
        "match_result": "{user}'s best match: {match} ({score}%)",
        "fight_start": "{user1} vs {user2} - FIGHT!",
        "duel_start": "Duel between {user1} and {user2} started!",
        "duel_result": "{winner} won the duel!",
        "muted": "{user} muted!",
        "unmuted": "{user} unmuted!",
        "kicked": "{user} kicked!",
        "banned": "{user} banned!",
        "flashmode_on": "Flash mode on! Click to teleport.",
        "flashmode_off": "Flash mode off.",
        "welcome_msg": "Welcome {user}!",
        "loop_started": "Loop message started: {msg}",
        "loop_stopped": "Loop message stopped.",
        "welcome_set": "Welcome message: {msg}",
        "welcome_disabled": "Welcome message disabled.",
        "coin_flip": "Coin flip: {result}",
        "coin_heads": "Heads",
        "coin_tails": "Tails",
        "dice_roll": "Dice: {result}",
        "choose_result": "I choose {choice}!",
        "rate_result": "My rating for {user}: {score}/10 {emoji}",
        "subscribe": "You are now subscribed!",
        "unsubscribe": "You have unsubscribed!",
        "already_sub": "Already subscribed.",
        "not_sub": "Not subscribed.",
        "broadcast": "Announcement: {msg}",
        "sub_whisper_tr": "Abone oldunuz! Benden haber bekleyin. 🙏",
        "sub_whisper_en": "You are subscribed! Wait for news from me. 🙏",
        "already_sub_whisper_tr": "Zaten abonesiniz!",
        "already_sub_whisper_en": "You are already subscribed!",
        "invite_all": "Tüm abonelere davet gönderildi! ({count} kişi)",
        "invite_all_en": "Invite sent to all subscribers! ({count} people)",
        "sub_list": "Subscribers: {count}",
        "no_subs": "No subscribers.",
        "invite_sent": "Invite sent!",
        "tip_received": "Tip: {user} -> {amount} gold",
        "tip_sent": "Sent {amount} gold to {user}!",
        "tip_self": "Can't tip yourself!",
        "tip_no_gold": "Not enough gold!",
        "insufficient_funds": "Insufficient funds!",
        "only_token_bought": "Token purchased but not applied.",
        "voice_bought": "Voice time purchased!",
        "dancefloor_corners": "Dance floor corners set!",
        "dancefloor_emote": "Dance floor emote: '{emote}'",
        "music_queue_title": "Music Queue ({count} songs):",
        "music_queue_empty": "No songs in queue.",
        "music_now_playing": "Now Playing: {song}",
        "music_added": "#{num} {song} added to queue!",
        "music_removed": "#{num} removed from queue!",
        "music_skipped": "Skipped! Next: {song}",
        "music_cleared": "Queue cleared!",
        "music_upvoted": "'{song}' moved up! ({count} votes)",
        "music_liked": "'{song}' liked! ({count} votes)",
        "music_unliked": "'{song}' unliked!",
        "music_played": "Playing '{song}'!",
        "music_event_started": "Music event started! {duration} min.",
        "music_event_ended": "Music event ended!",
        "music_event_status": "{remaining} min left, {participants} participate.",
        "music_event_winners": "Winners:\n{list}",
        "music_event_no_winners": "No winners.",
        "music_saved": "'{song}' saved to your library!",
        "music_library": "Your library ({count}): {list}",
        "music_library_empty": "Your library is empty.",
        "music_removed_lib": "'{song}' removed from library!",
        "music_from_lib": "Playing '{song}' from your library!",
        "music_filter_set": "Effect set: {effect}",
        "music_filter_cleared": "Effect cleared.",
        "shuffle_on": "Shuffle on!",
        "shuffle_off": "Shuffle off!",
        "repeat_on": "Repeat on!",
        "repeat_off": "Repeat off!",
        "music_not_in_queue": "Not in queue.",
        "music_no_current": "No song playing.",
        "music_help": "-p <song/genre> | -up | -like | !queue | !add | !skip | !shuffle | !repeat | !voice | !mylib | !filter | !event",
        "voice_on": "Voice mode on! Music via voice.",
        "voice_off": "Voice mode off.",
        "voice_error": "Voice chat error: {msg}",
        "music_voice_help": "Voice Music: !voice",
        "time_limit": "Maximum song duration: {limit} seconds",
        "invalid_args": "Invalid arguments!",
        "heart_sent": "Heart sent!",
        "emote_list_title": "Available Dances:",
        "loop_stopped_all": "All loops stopped.",
        "welcome_role": "Welcome role set.",
        "access_on": "All-access enabled!",
        "access_off": "All-access disabled!",
        "bot_already_following": "Already following you!",
        "follow_toggle_on": "Follow enabled!",
        "follow_toggle_off": "Follow disabled!",
    }
}

BOOST_AMOUNTS = {1: "gold_bar_1k", 2: "gold_bar_2k", 3: "gold_bar_3k", 4: "gold_bar_4k", 5: "gold_bar_5k",
                 6: "gold_bar_6k", 7: "gold_bar_7k", 8: "gold_bar_8k", 9: "gold_bar_9k", 10: "gold_bar_10k"}

GOLD_BARS = {"gold_bar_1": 1, "gold_bar_5": 5, "gold_bar_10": 10, "gold_bar_50": 50, "gold_bar_100": 100,
             "gold_bar_500": 500, "gold_bar_1k": 1000, "gold_bar_5000": 5000, "gold_bar_10k": 10000}

GOLD_BAR_KEYS = list(GOLD_BARS.keys())

GENRES = {
    "pop": ["k-pop dance", "tik tok", "tiktok", "casual dance", "floss", "hands in the air", "macarena", "orange juice dance", "savage dance", "don't start now", "dab", "gangnam style", "disco", "harlem shake", "night fever", "anime dance", "kawaii", "ice cream dance", "wrong dance", "weird dance", "touch", "cute", "cutey", "feel the beat", "boogie swing", "vogue hands"],
    "jazz": ["vogue hands", "smoothwalk", "moonwalk", "tap dance", "boogie swing", "feel the beat", "graceful", "model", "curtsy", "bow", "posh", "chillin'"],
    "rock": ["rock out", "air guitar", "punk guitar"],
    "electronic": ["robotic", "robot", "energy ball", "telekinesis", "float", "levitate", "level up!", "blast off", "teleporting", "timejump"],
    "hiphop": ["breakdance", "savage dance", "dab", "floss", "hands in the air", "harlem shake", "gangnam style"],
    "rnb": ["ring on it", "sexy dance", "flirty wave", "graceful", "model", "moonwalk", "smoothwalk"],
    "chill": ["yoga flow", "chillin'", "daydreaming", "star gazing", "relaxed", "cozy nap", "relaxing", "sleepy", "rest", "laid back", "meditation"],
    "fitness": ["aerobics", "push ups", "jump", "boxer", "karate", "judo chop", "super punch", "headball", "punch"],
    "party": ["disco", "gangnam style", "night fever", "macarena", "harlem shake", "k-pop dance", "raise the roof", "frolic", "hyped"],
    "latin": ["bunny hop", "disco"],
    "soul": ["ring on it", "feel the beat", "graceful", "vogue hands"],
    "folk": ["russian dance", "jinglebell", "sleigh", "penguin dance"],
}

FFMPEG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ffmpeg")
FFMPEG_PATH = os.path.join(FFMPEG_DIR, "ffmpeg.exe")

def _ensure_ffmpeg():
    if os.path.isfile(FFMPEG_PATH):
        return True
    os.makedirs(FFMPEG_DIR, exist_ok=True)
    url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
    zip_path = os.path.join(tempfile.gettempdir(), "ffmpeg.zip")
    try:
        urllib.request.urlretrieve(url, zip_path)
        with zipfile.ZipFile(zip_path, "r") as zf:
            for name in zf.namelist():
                if name.endswith("ffmpeg.exe"):
                    with zf.open(name) as src, open(FFMPEG_PATH, "wb") as dst:
                        shutil.copyfileobj(src, dst)
                    break
        return os.path.isfile(FFMPEG_PATH)
    except:
        return False
    finally:
        if os.path.isfile(zip_path):
            os.unlink(zip_path)

def find_mentioned_user(target_username: str, room_users: list):
    target = target_username.lower().replace("@", "")
    for room_user, _ in room_users:
        if room_user.username.lower() == target:
            return room_user
    return None

def load_data():
    defaults = {
        "teleports": {}, "vip_teleports": [], "vip_list": [], "user_langs": {}, "tips": {},
        "total_tip_gold": 0, "total_tip_count": 0, "roles": {}, "dj_users": [],
        "welcome_message": None, "welcome_mode": "chat", "loop_message": None,
        "loop_interval": 60, "bot_loop_emote": None, "auto_react": False,
        "welcome_role": False, "outfits": {}, "saved_positions": {},
        "subscribers": [], "join_message": None, "leave_message": None,
        "vip_join_message": None, "vip_leave_message": None, "alert_message": None,
        "thank_message": None, "flash_mode": False, "dancefloor": {},
        "music_queue": [], "current_song": None, "music_likes": {},
        "user_liked_songs": {}, "song_library": {},
        "music_settings": {"auto_play": False, "shuffle": False, "repeat": False, "effect": None, "voice": False},
        "event": None, "all_access": False, "custom_emotes": {}, "manager_list": []
    }
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            for key, val in defaults.items():
                if key not in data:
                    data[key] = val
            return data
        except:
            pass
    return defaults

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

class Bot(BaseBot):
    def __init__(self):
        super().__init__()
        self.follow_target_id = None
        self.room_owner_id = None
        self.bot_id = None
        self.pinned_position = None
        self.loop_task_ref = None
        self.data = load_data()
        self.teleport_queue = {}
        self.pending_duels = {}
        self.music_task_ref = None
        self.music_skip_event = asyncio.Event()
        self.following_enabled = True
        self.reminder_task_ref = None
        self.dance_loop_task = None
        self.active_dance_emote_id = None
        self.youtube_playing = False
        self.current_youtube_title = None

    def lang(self, user_id: str, key: str, **kwargs) -> str:
        lang_code = self.data["user_langs"].get(user_id, "tr")
        text = LANG.get(lang_code, LANG["tr"]).get(key, key)
        if kwargs:
            try:
                text = text.format(**kwargs)
            except KeyError:
                pass
        return text

    def owner_lang(self, key: str, **kwargs) -> str:
        return self.lang(self.room_owner_id, key, **kwargs)

    def is_owner(self, user_id: str) -> bool:
        return user_id == self.room_owner_id

    def is_vip(self, user_id: str) -> bool:
        return user_id in self.data.get("vip_list", [])

    def is_manager(self, user_id: str) -> bool:
        return user_id in self.data.get("manager_list", [])

    def get_user_by_id(self, user_id: str, room_users: list):
        for ru, _ in room_users:
            if ru.id == user_id:
                return ru
        return None

    def has_permission(self, user_id: str, required_role: str = "owner") -> bool:
        if required_role == "owner":
            return self.is_owner(user_id)
        if required_role == "vip":
            return self.is_owner(user_id) or self.is_vip(user_id)
        return True

    async def _reply(self, user_id: str, text: str):
        try:
            await self.highrise.send_whisper(user_id, text)
        except:
            try:
                await self.highrise.chat(text)
            except:
                pass

    async def on_start(self, session_metadata: SessionMetadata) -> None:
        print(f"Labnem bot başlatıldı! Bot ID: {session_metadata.user_id}")
        self.bot_id = session_metadata.user_id
        self.room_owner_id = session_metadata.room_info.owner_id
        self.room_id = getattr(session_metadata.room_info, 'room_id', None) or getattr(session_metadata.room_info, 'id', None)
        if _ensure_ffmpeg():
            print("ffmpeg hazır")
        sm = self._find_stereo_mix()
        if sm is not None:
            self._set_stereo_mix_as_default()
        else:
            print("⚠️ Stereo Karışımı bulunamadı. Ses sadece hoparlörden çıkar.")
        if self.data.get("loop_message") and not self.loop_task_ref:
            self.loop_task_ref = asyncio.create_task(self._loop_messages())
        if not self.music_task_ref:
            self.music_task_ref = asyncio.create_task(self._music_player())
        if not self.reminder_task_ref:
            self.reminder_task_ref = asyncio.create_task(self._reminder_loop())

    async def _loop_messages(self):
        while True:
            try:
                msg = self.data.get("loop_message")
                interval = self.data.get("loop_interval", 60)
                if msg:
                    await self.highrise.chat(msg)
                await asyncio.sleep(interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Loop error: {e}")
                await asyncio.sleep(60)

    async def _dance_loop(self, emote_id: str, name: str):
        try:
            while True:
                await self.highrise.send_emote(emote_id)
                await asyncio.sleep(4)
        except asyncio.CancelledError:
            pass

    async def _reminder_loop(self):
        while True:
            try:
                await asyncio.sleep(600)
                await self.highrise.chat("Komutlar için !komutlar yazabilirsiniz! 🎵 Müzik için -p <şarkı adı>")
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Reminder error: {e}")
                await asyncio.sleep(600)

    async def on_user_join(self, user: User, position: Position | AnchorPosition) -> None:
        await self.highrise.chat(f"Hoş geldin @{user.username}! Lütfen @labune takip etmeyi unutmayın, eğlenmenize bakın! Komutlar için !komutlar")
        join_msg = self.data.get("join_message")
        if join_msg:
            msg = join_msg.replace("{user}", f"@{user.username}")
            await self.highrise.chat(msg)
        wlcm = self.data.get("welcome_message")
        if wlcm:
            wlcm_text = wlcm.replace("{user}", f"@{user.username}")
            if self.data.get("welcome_mode") == "whisper":
                await self.highrise.send_whisper(user.id, wlcm_text)
            else:
                await self.highrise.chat(wlcm_text)
        if self.is_vip(user.id):
            vip_join = self.data.get("vip_join_message")
            if vip_join:
                await self.highrise.send_whisper(user.id, vip_join.replace("{user}", f"@{user.username}"))

    async def on_user_leave(self, user: User) -> None:
        leave_msg = self.data.get("leave_message")
        if leave_msg:
            msg = leave_msg.replace("{user}", f"@{user.username}")
            await self.highrise.chat(msg)
        if self.is_vip(user.id):
            vip_leave = self.data.get("vip_leave_message")
            if vip_leave:
                await self.highrise.chat(vip_leave.replace("{user}", f"@{user.username}"))

    async def on_tip(self, sender: User, receiver: User, tip: CurrencyItem | Item) -> None:
        if isinstance(tip, CurrencyItem) and receiver.id == self.bot_id:
            amount = tip.amount
            self.data["total_tip_gold"] += amount
            self.data["total_tip_count"] += 1
            if sender.id not in self.data["tips"]:
                self.data["tips"][sender.id] = {"username": sender.username, "total": 0}
            self.data["tips"][sender.id]["total"] += amount
            self.data["tips"][sender.id]["username"] = sender.username
            save_data(self.data)
            print(f"{sender.username} tipped {amount}g -> bot")
            thank_msg = self.data.get("thank_message")
            if thank_msg:
                await self.highrise.chat(thank_msg.replace("{user}", f"@{sender.username}").replace("{amount}", str(amount)))
            elif amount >= 500:
                await self.highrise.chat(self.lang(self.room_owner_id, "tip_thanks_big", user=f"@{sender.username}", amount=amount))
            else:
                await self.highrise.chat(self.lang(self.room_owner_id, "tip_thanks_small", user=f"@{sender.username}"))

    async def on_user_move(self, user: User, pos: Position | AnchorPosition) -> None:
        if self.following_enabled and self.follow_target_id == user.id and isinstance(pos, Position):
            if self.pinned_position is None:
                await self.highrise.walk_to(pos)

    async def on_chat(self, user: User, message: str) -> None:
        msg = message.strip()
        if not msg:
            return
        if await self._handle_dance(user, message):
            return
        if await self._handle_follow_stop(user, msg):
            return
        if await self._handle_pin(user, msg):
            return
        if await self._handle_teleport(user, msg):
            return
        if await self._handle_lang(user, msg):
            return
        if await self._handle_boost_wallet(user, msg):
            return
        if await self._handle_tips(user, msg):
            return
        if await self._handle_dj_mic(user, msg):
            return
        if await self._handle_roles(user, msg):
            return
        if await self._handle_vip(user, msg):
            return
        if await self._handle_manager(user, msg):
            return
        if await self._handle_fun(user, msg):
            return
        if await self._handle_mod(user, msg):
            return
        if await self._handle_settings(user, msg):
            return
        if await self._handle_outfits(user, msg):
            return
        if await self._handle_movement(user, msg):
            return
        if await self._handle_social(user, msg):
            return
        if await self._handle_dancefloor(user, msg):
            return
        if await self._handle_bot_emote(user, msg):
            return
        if await self._handle_music(user, msg):
            return
        if await self._handle_custom_emote(user, msg):
            return
        if await self._handle_help(user, msg):
            return

    async def on_whisper(self, user: User, message: str) -> None:
        msg = message.strip().lower()
        if msg in ["!sub", "!subscribe", "abone"]:
            if "subscribers" not in self.data:
                self.data["subscribers"] = []
            if user.id not in self.data["subscribers"]:
                self.data["subscribers"].append(user.id)
                save_data(self.data)
            sent = False
            try:
                await self.highrise.send_whisper(user.id, f"@{user.username} {LANG['tr']['sub_whisper_tr']}")
                await self.highrise.send_whisper(user.id, f"@{user.username} {LANG['en']['sub_whisper_en']}")
                sent = True
            except:
                pass
            if not sent:
                try:
                    res = await self.highrise.send_message_bulk([user.id], f"@{user.username} Abone oldunuz! Benden haber bekleyin. 🙏")
                    if res is None:
                        sent = True
                except:
                    pass

    async def on_message(self, user_id: str, conversation_id: str, is_new_conversation: bool) -> None:
        try:
            conversation = await self.highrise.get_messages(conversation_id)
            message = conversation.messages[0].content.lower().strip()
            if message in ["!sub", "!subscribe", "abone"]:
                if "subscribers" not in self.data:
                    self.data["subscribers"] = []
                if user_id not in self.data["subscribers"]:
                    self.data["subscribers"].append(user_id)
                    save_data(self.data)
                    await self.highrise.send_message(conversation_id, "🎉 Tebrikler! Artık ailemizin bir parçasısın! Seni aramızda görmek ne güzel! 💫\n🎉 Congratulations! You're now part of our family! So happy to have you with us! 💫 🙏")
                else:
                    await self.highrise.send_message(conversation_id, "💖 Zaten aramızdasın! Bizi desteklediğin için çok teşekkürler! Seni seviyoruz! 🥰\n💖 You're already with us! Thank you so much for your support! We love you! 🥰")
            elif message in ["!unsub", "!unsubscribe"]:
                if "subscribers" in self.data and user_id in self.data["subscribers"]:
                    self.data["subscribers"].remove(user_id)
                    save_data(self.data)
                    await self.highrise.send_message(conversation_id, "😢 Ayrıldığın için üzgünüz! Umarız tekrar görüşürüz! Her zaman bekleriz! 💔\n😢 Sorry to see you go! Hope to see you again! You're always welcome! 💔")
                else:
                    await self.highrise.send_message(conversation_id, "🤔 Zaten abone değilsin! Abone olmak için: !sub\n🤔 You're not subscribed! To subscribe: !sub")
        except Exception as e:
            print(f"on_message error: {e}")

    async def _handle_custom_emote(self, user: User, msg: str) -> bool:
        match_custom = re.match(r"^!custom\s+(.+)$", msg)
        if match_custom:
            emotes_str = match_custom.group(1).strip()
            emote_names = emotes_str.split()
            emote_ids = []
            for e_name in emote_names:
                en = e_name.lower().strip()
                if en in DANCE_MAP:
                    emote_ids.append(DANCE_MAP[en])
            if emote_ids:
                self.data["custom_emotes"] = {"ids": emote_ids, "names": emote_names}
                save_data(self.data)
                await self._reply(user.id, f"{self.lang(user.id, 'custom_emote', emotes=', '.join(emote_names))}")
            else:
                await self._reply(user.id, f"Geçersiz dans adları! !danslar ile listeye bak.")
            return True

        match_sayso = re.match(r"^sayso loop$", msg)
        if match_sayso:
            sid = DANCE_MAP.get("sayso") or DANCE_MAP.get("yes")
            if sid:
                try:
                    await self.highrise.send_emote(sid)
                    await self._reply(user.id, f"{self.lang(user.id, 'sayso_loop')}")
                except Exception as e:
                    print(f"Emote error: {e}")
            else:
                await self._reply(user.id, f"'sayso' dansı bulunamadı.")
            return True

        return False

    async def _handle_dance(self, user: User, message: str) -> bool:
        msg = message.lower().strip()
        room_users = await self.highrise.get_room_users()
        ru_content = room_users.content if hasattr(room_users, 'content') else room_users

        if msg in ["!danslar", "!emotes"]:
            items_per_page = 20
            total_pages = (len(all_emote_list) + items_per_page - 1) // items_per_page
            parts = msg.split()
            page = 0
            if len(parts) > 1 and parts[1].isdigit():
                page = max(0, min(total_pages - 1, int(parts[1]) - 1))
            start = page * items_per_page
            end = min(start + items_per_page, len(all_emote_list))
            lines = [f"{i}. {all_emote_list[i][0]}" for i in range(start, end)]
            header = self.lang(user.id, 'dance_list_header', page=page+1, total=total_pages)
            text = f"@{user.username} {header} " + " | ".join(lines)
            try:
                await self.highrise.send_whisper(user.id, text)
            except:
                await self._reply(user.id, text)
            return True

        if msg in ["!giydir", "!random"]:
            try:
                inv_resp = await self.highrise.get_inventory()
                inv_items = inv_resp.items if hasattr(inv_resp, 'items') else []
                inv_cats = {}
                for item in inv_items:
                    inv_cats.setdefault(item.id.split("-")[0], []).append(item)

                outfit_resp = await self.highrise.get_user_outfit(user.id)
                user_items = outfit_resp.outfit if hasattr(outfit_resp, 'outfit') else []

                picked = {}
                for item in user_items:
                    cat = item.id.split("-")[0]
                    if cat not in picked:
                        picked[cat] = item

                for cat in ["body", "eye", "eyebrow", "nose", "mouth"]:
                    if cat not in picked and cat in inv_cats:
                        picked[cat] = random.choice(inv_cats[cat])

                has_shirt = "shirt" in picked
                has_pants = "pants" in picked
                has_skirt = "skirt" in picked
                has_dress = "dress" in picked
                has_fullsuit = "fullsuit" in picked
                if not ((has_shirt and (has_pants or has_skirt)) or has_dress or has_fullsuit):
                    for combo in [("shirt", "pants"), ("shirt", "skirt"), ("dress",), ("fullsuit",)]:
                        available = [c for c in combo if c in inv_cats]
                        if len(available) == len(combo):
                            for c in combo:
                                picked[c] = random.choice(inv_cats[c])
                            break

                outfit_list = [Item(id=i.id, type=i.type, amount=1, active_palette=i.active_palette if i.active_palette is not None else 0) for i in picked.values()]
                result = await self.highrise.set_outfit(outfit_list)
                if result is None:
                    await self._reply(user.id, f"bot kıyafetini kopyaladı! ({len(outfit_list)} parça)")
                else:
                    await self._reply(user.id, f"Kopyalanamadı: {result}")
            except Exception as e:
                await self._reply(user.id, self.lang(user.id, 'inventory_error'))
            return True

        if msg.isdigit():
            idx = int(msg) - 1
            if 0 <= idx < len(all_emote_list):
                name, emote_id = all_emote_list[idx]
                if self.dance_loop_task:
                    self.dance_loop_task.cancel()
                    self.dance_loop_task = None
                self.active_dance_emote_id = emote_id
                self.dance_loop_task = asyncio.create_task(self._dance_loop(emote_id, name))
                await self._reply(user.id, f"için {name} dansı başlatıldı! Durdurmak için: !dancestop")
                return True

        if msg in DANCE_MAP:
            emote_id = DANCE_MAP[msg]
            name = DANCE_NAME_MAP.get(msg, msg)
            if self.dance_loop_task:
                self.dance_loop_task.cancel()
                self.dance_loop_task = None
            self.active_dance_emote_id = emote_id
            self.dance_loop_task = asyncio.create_task(self._dance_loop(emote_id, name))
            await self._reply(user.id, f"için {name} dansı başlatıldı! Durdurmak için: !dancestop")
            return True

        if msg in ["!dancestop", "!loopstop", "!dansdur"]:
            if self.dance_loop_task:
                self.dance_loop_task.cancel()
                self.dance_loop_task = None
                self.active_dance_emote_id = None
                await self._reply(user.id, f"Dans döngüsü durduruldu.")
            else:
                await self._reply(user.id, f"Aktif dans döngüsü yok.")
            return True

        if msg.startswith("all dance ") or msg.startswith("all dans "):
            if not self.is_owner(user.id):
                await self._reply(user.id, f"{self.lang(user.id, 'not_owner')}")
                return True
            parts = msg.split(" ", 2)
            if len(parts) < 3:
                await self._reply(user.id, "Kullanım: all dance <sayı/isim>")
                return True
            d_input = parts[2].strip()
            emote_id = DANCE_MAP.get(d_input)
            if not emote_id:
                await self._reply(user.id, f"Geçersiz dans! !danslar ile listeye bak.")
                return True
            dance_name = DANCE_NAME_MAP.get(d_input, d_input)
            success_count = 0
            for room_user, _ in ru_content:
                try:
                    await self.highrise.send_emote(emote_id)
                    success_count += 1
                except:
                    pass
            await self._reply(user.id, self.lang(user.id, 'all_dance_done', count=success_count, dance=dance_name))
            return True

        return False

    async def _handle_follow_stop(self, user: User, msg: str) -> bool:
        def authorized():
            au = user.username.lower()
            return self.is_owner(user.id) or self.is_manager(user.id) or au in ["labune", "labunem"]

        if msg in ["takip et", "!follow", "!takipet"]:
            if not authorized():
                await self.highrise.chat(f"@{user.username} {self.lang(user.id, 'no_permission')}")
                return True
            if not self.following_enabled:
                self.following_enabled = True
            if self.follow_target_id == user.id:
                await self.highrise.chat(f"@{user.username} {self.lang(user.id, 'bot_already_following')}")
                return True
            self.follow_target_id = user.id
            self.pinned_position = None
            await self.highrise.chat(f"@{user.username} {self.lang(user.id, 'follow')}")
            try:
                room_users = await self.highrise.get_room_users()
                ru = room_users.content if hasattr(room_users, 'content') else room_users
                for room_user, pos in ru:
                    if room_user.id == user.id and isinstance(pos, Position):
                        await self.highrise.walk_to(pos)
                        break
            except Exception as e:
                print(f"Follow walk error: {e}")
            return True

        if msg in ["!followtoggle", "!takipac", "!takipkapa"]:
            if not authorized():
                await self.highrise.chat(f"@{user.username} {self.lang(user.id, 'no_permission')}")
                return True
            self.following_enabled = not self.following_enabled
            key = "follow_toggle_on" if self.following_enabled else "follow_toggle_off"
            await self.highrise.chat(f"@{user.username} {self.lang(user.id, key)}")
            return True

        if msg in ["dur", "!stop", "!dur"]:
            if not authorized():
                await self.highrise.chat(f"@{user.username} {self.lang(user.id, 'no_permission')}")
                return True
            self.follow_target_id = None
            await self.highrise.chat(f"@{user.username} {self.lang(user.id, 'stop')}")
            return True

        return False

    async def _handle_pin(self, user: User, msg: str) -> bool:
        if msg in ["!pin", "!sabitle"]:
            try:
                room_users = await self.highrise.get_room_users()
                ru_content = room_users.content if hasattr(room_users, 'content') else room_users
                for room_user, pos in ru_content:
                    if room_user.id == user.id and isinstance(pos, Position):
                        self.pinned_position = pos
                        self.follow_target_id = None
                        await self._reply(user.id, f"{self.lang(user.id, 'pinned')}")
                        return True
            except Exception as e:
                print(f"Pin error: {e}")
            return True

        if msg in ["!unpin", "!kaldir"]:
            self.pinned_position = None
            self.follow_target_id = None
            await self._reply(user.id, f"{self.lang(user.id, 'unpinned')}")
            return True

        if msg == "!setpos":
            try:
                room_users = await self.highrise.get_room_users()
                ru_content = room_users.content if hasattr(room_users, 'content') else room_users
                for room_user, pos in ru_content:
                    if room_user.id == user.id and isinstance(pos, Position):
                        await self.highrise.walk_to(pos)
                        self.pinned_position = pos
                        await self._reply(user.id, f"{self.lang(user.id, 'setpos_done')}")
                        break
            except Exception as e:
                print(f"Setpos error: {e}")
            return True

        return False

    async def _handle_teleport(self, user: User, msg: str) -> bool:
        if msg == "!flashmode":
            self.data["flash_mode"] = not self.data.get("flash_mode", False)
            save_data(self.data)
            key = "flashmode_on" if self.data["flash_mode"] else "flashmode_off"
            await self._reply(user.id, f"{self.lang(user.id, key)}")
            return True

        match_create = re.match(r"^!create tele (.+)$", msg)
        if match_create:
            if not self.is_owner(user.id):
                await self._reply(user.id, f"{self.lang(user.id, 'not_owner')}")
                return True
            name = match_create.group(1).strip()
            try:
                room_users = await self.highrise.get_room_users()
                ru_content = room_users.content if hasattr(room_users, 'content') else room_users
                for room_user, pos in ru_content:
                    if room_user.id == user.id and isinstance(pos, Position):
                        self.data["teleports"][name] = {"x": pos.x, "y": pos.y, "z": pos.z,
                                                        "facing": pos.facing, "created_by": user.username}
                        if name in self.data["vip_teleports"]:
                            self.data["vip_teleports"].remove(name)
                        save_data(self.data)
                        await self._reply(user.id, self.lang(user.id, 'tele_created', name=name))
                        break
            except Exception as e:
                print(f"Tele create error: {e}")
            return True

        match_remove = re.match(r"^!remove tele (.+)$", msg)
        if match_remove:
            if not self.is_owner(user.id):
                await self._reply(user.id, f"{self.lang(user.id, 'not_owner')}")
                return True
            name = match_remove.group(1).strip()
            if name in self.data["teleports"]:
                del self.data["teleports"][name]
                if name in self.data["vip_teleports"]:
                    self.data["vip_teleports"].remove(name)
                save_data(self.data)
                await self._reply(user.id, self.lang(user.id, 'tele_removed', name=name))
            else:
                await self._reply(user.id, self.lang(user.id, 'tele_not_found', name=name))
            return True

        match_vip = re.match(r"^!vip tele (.+)$", msg)
        if match_vip:
            if not self.is_owner(user.id):
                await self._reply(user.id, f"{self.lang(user.id, 'not_owner')}")
                return True
            name = match_vip.group(1).strip()
            if name in self.data["teleports"]:
                if name in self.data["vip_teleports"]:
                    self.data["vip_teleports"].remove(name)
                    await self._reply(user.id, self.lang(user.id, 'tele_vip_unset', name=name))
                else:
                    self.data["vip_teleports"].append(name)
                    await self._reply(user.id, self.lang(user.id, 'tele_vip_set', name=name))
                save_data(self.data)
            else:
                await self._reply(user.id, self.lang(user.id, 'tele_not_found', name=name))
            return True

        match_tele = re.match(r"^!tele (.+?)(?: (.+))?$", msg)
        if match_tele:
            name = match_tele.group(1).strip()
            target_name = match_tele.group(2).strip() if match_tele.group(2) else None
            if name not in self.data["teleports"]:
                await self._reply(user.id, f"{self.lang(user.id, 'tele_not_found', name=name)}")
                return True
            if name in self.data["vip_teleports"] and not self.is_vip(user.id) and not self.is_owner(user.id):
                await self._reply(user.id, self.lang(user.id, 'tele_vip_only'))
                return True
            tp = self.data["teleports"][name]
            pos = Position(tp["x"], tp["y"], tp["z"], tp.get("facing", "FrontRight"))
            try:
                if target_name == "all":
                    await self.highrise.walk_to(pos)
                    await self._reply(user.id, self.lang(user.id, 'teleported_all', name=name))
                elif target_name:
                    room_users = await self.highrise.get_room_users()
                    ru_content = room_users.content if hasattr(room_users, 'content') else room_users
                    tu = find_mentioned_user(target_name, ru_content)
                    if tu:
                        await self.highrise.walk_to(pos)
                        await self._reply(user.id, self.lang(user.id, 'teleported', user=f"@{tu.username}", name=name))
                    else:
                        await self._reply(user.id, f"Kullanıcı bulunamadı.")
                else:
                    await self.highrise.walk_to(pos)
                    await self._reply(user.id, self.lang(user.id, 'teleported', user=f"@{user.username}", name=name))
            except Exception as e:
                print(f"Tele error: {e}")
            return True

        if msg in ["!teleports", "!telelist"]:
            tels = list(self.data["teleports"].keys())
            if tels:
                marked = [f"{t} {'VIP' if t in self.data.get('vip_teleports', []) else ''}" for t in tels]
                await self._reply(user.id, f"{self.lang(user.id, 'tele_list', list=', '.join(marked))}")
            else:
                await self._reply(user.id, f"{self.lang(user.id, 'tele_no_teleports')}")
            return True

        return False

    async def _handle_lang(self, user: User, msg: str) -> bool:
        if msg in ["!lang tr", "!dil tr", "!dil türkçe", "!lang turkish"]:
            self.data["user_langs"][user.id] = "tr"
            save_data(self.data)
            await self._reply(user.id, f"{LANG['tr']['lang_set']}")
            return True
        if msg in ["!lang en", "!dil en", "!dil ingilizce", "!lang english"]:
            self.data["user_langs"][user.id] = "en"
            save_data(self.data)
            await self._reply(user.id, f"{LANG['en']['lang_set']}")
            return True
        if msg in ["!lang", "!dil"]:
            current = self.data["user_langs"].get(user.id, "tr")
            await self._reply(user.id, f"Diliniz: {current.upper()} | !lang tr/en veya !dil tr/en")
            return True
        return False

    async def _handle_boost_wallet(self, user: User, msg: str) -> bool:
        match_boost = re.match(r"^!boost\s*(\d*)$", msg)
        if match_boost:
            if not self.is_owner(user.id):
                await self._reply(user.id, f"{self.lang(user.id, 'not_owner')}")
                return True
            count = int(match_boost.group(1)) if match_boost.group(1) else 1
            count = max(1, min(10, count))
            await self._reply(user.id, self.lang(user.id, 'boost_started'))
            try:
                result = await self.highrise.buy_room_boost("bot_wallet_priority", count)
                if result == "success":
                    await self._reply(user.id, self.lang(user.id, 'boost_success', count=count))
                elif result == "insufficient_funds":
                    await self._reply(user.id, self.lang(user.id, 'boost_fail', reason=self.lang(user.id, 'insufficient_funds')))
                elif result == "only_token_bought":
                    await self._reply(user.id, self.lang(user.id, 'only_token_bought'))
                else:
                    await self._reply(user.id, self.lang(user.id, 'boost_fail', reason=str(result)))
            except Exception as e:
                await self._reply(user.id, self.lang(user.id, 'boost_fail', reason=str(e)))
            return True

        if msg in ["!wallet", "!cash", "!cuzdan"]:
            try:
                wallet = await self.highrise.get_wallet()
                gold = 0
                for currency in wallet.content:
                    if hasattr(currency, 'type') and currency.type == 'gold':
                        gold = currency.amount
                    elif hasattr(currency, 'amount'):
                        gold = currency.amount
                if gold > 0:
                    await self._reply(user.id, self.lang(user.id, 'wallet_info', gold=gold))
                else:
                    await self._reply(user.id, self.lang(user.id, 'wallet_no_gold'))
            except Exception as e:
                print(f"Wallet error: {e}")
            return True

        match_voice = re.match(r"^!voicetime(?:\s+(.+))?$", msg)
        if match_voice:
            if not self.is_owner(user.id):
                await self._reply(user.id, f"{self.lang(user.id, 'not_owner')}")
                return True
            try:
                result = await self.highrise.buy_voice_time("bot_wallet_priority")
                if result == "success":
                    await self._reply(user.id, self.lang(user.id, 'voice_bought'))
                else:
                    await self._reply(user.id, self.lang(user.id, 'boost_fail', reason=str(result)))
            except Exception as e:
                await self._reply(user.id, self.lang(user.id, 'boost_fail', reason=str(e)))
            return True

        return False

    async def _handle_tips(self, user: User, msg: str) -> bool:
        if msg in ["!tips", "!tipsummary", "!bahsis"]:
            tips_data = self.data.get("tips", {})
            total_gold = self.data.get("total_tip_gold", 0)
            total_people = len(tips_data)
            if total_people == 0:
                await self._reply(user.id, f"{self.lang(user.id, 'tip_summary_none')}")
                return True
            title = self.lang(user.id, 'tip_summary_title')
            total = self.lang(user.id, 'tip_summary_total', gold=total_gold)
            people = self.lang(user.id, 'tip_summary_people', count=total_people)
            await self._reply(user.id, f"{title} {total} | {people}")
            return True

        if msg in ["!tiptop", "!top", "!toplist"]:
            tips = self.data.get("tips", {})
            if not tips:
                await self._reply(user.id, self.lang(user.id, 'tip_summary_none'))
                return True
            sorted_tips = sorted(tips.items(), key=lambda x: x[1]["total"], reverse=True)[:10]
            lines = [f"{i+1}. {t[1]['username']} ({t[1]['total']}g)" for i, t in enumerate(sorted_tips)]
            await self._reply(user.id, f"{self.lang(user.id, 'tip_leaderboard', list=' | '.join(lines))}")
            return True

        match_get = re.match(r"^!tipget\s+@?(\w+)$", msg)
        if match_get:
            name = match_get.group(1)
            found = False
            for uid, tdata in self.data.get("tips", {}).items():
                if tdata["username"].lower() == name.lower():
                    await self._reply(user.id, self.lang(user.id, 'tip_get', user=f"@{tdata['username']}", amount=tdata['total']))
                    found = True
                    break
            if not found:
                await self._reply(user.id, self.lang(user.id, 'tip_get_none', user=f"@{name}"))
            return True

        match_tip = re.match(r"^!tip\s+@?(\w+)\s+(\d+)$", msg)
        if match_tip:
            if not self.is_owner(user.id) and not self.is_manager(user.id):
                await self._reply(user.id, f"{self.lang(user.id, 'not_owner')}")
                return True
            target_name = match_tip.group(1)
            amount = int(match_tip.group(2))
            bar_key = None
            for bk in GOLD_BAR_KEYS:
                if GOLD_BARS[bk] == amount:
                    bar_key = bk
                    break
            if not bar_key:
                closest = min(GOLD_BARS.keys(), key=lambda k: abs(GOLD_BARS[k] - amount))
                bar_key = closest
            try:
                room_users = await self.highrise.get_room_users()
                ru_content = room_users.content if hasattr(room_users, 'content') else room_users
                tu = find_mentioned_user(target_name, ru_content)
                if tu:
                    if tu.id == self.bot_id:
                        await self._reply(user.id, self.lang(user.id, 'tip_self'))
                        return True
                    await self.highrise.tip_user(tu.id, bar_key)
                    await self._reply(user.id, self.lang(user.id, 'tip_sent', user=f"@{tu.username}", amount=amount))
                else:
                    await self._reply(user.id, f"Kullanıcı bulunamadı.")
            except Exception as e:
                await self._reply(user.id, f"Hata: {str(e)}")
            return True

        if msg == "!tipall":
            if not self.is_owner(user.id):
                await self._reply(user.id, f"{self.lang(user.id, 'not_owner')}")
                return True
            try:
                room_users = await self.highrise.get_room_users()
                ru_content = room_users.content if hasattr(room_users, 'content') else room_users
                bar_key = "gold_bar_1"
                for ru, _ in ru_content:
                    if ru.id != self.bot_id:
                        try:
                            await self.highrise.tip_user(ru.id, bar_key)
                        except:
                            pass
                await self._reply(user.id, self.lang(user.id, 'tip_all', amount=1))
            except Exception as e:
                print(f"Tip all error: {e}")
            return True

        return False

    async def _handle_dj_mic(self, user: User, msg: str) -> bool:
        match_dj = re.match(r"^!dj\s+@?(\w+)$", msg)
        if match_dj:
            if not self.is_owner(user.id):
                await self._reply(user.id, f"{self.lang(user.id, 'not_owner')}")
                return True
            name = match_dj.group(1)
            try:
                room_users = await self.highrise.get_room_users()
                ru_content = room_users.content if hasattr(room_users, 'content') else room_users
                tu = find_mentioned_user(name, ru_content)
                if tu:
                    if tu.id in self.data.get("dj_users", []):
                        self.data["dj_users"].remove(tu.id)
                        await self._reply(user.id, f"DJ {tu.username} çıkarıldı.")
                    else:
                        if "dj_users" not in self.data:
                            self.data["dj_users"] = []
                        self.data["dj_users"].append(tu.id)
                        await self._reply(user.id, f"DJ {tu.username} eklendi!")
                    save_data(self.data)
                else:
                    await self._reply(user.id, f"Kullanıcı bulunamadı.")
            except Exception as e:
                print(f"DJ error: {e}")
            return True

        match_mic = re.match(r"^!mic\s+@?(\w+)$", msg)
        if match_mic:
            if not self.is_owner(user.id):
                await self._reply(user.id, f"{self.lang(user.id, 'not_owner')}")
                return True
            name = match_mic.group(1)
            try:
                room_users = await self.highrise.get_room_users()
                ru_content = room_users.content if hasattr(room_users, 'content') else room_users
                tu = find_mentioned_user(name, ru_content)
                if tu:
                    try:
                        await self.highrise.invite_to_voice(tu.id)
                        await self._reply(user.id, self.lang(user.id, 'mic_on', user=f"@{tu.username}"))
                    except:
                        try:
                            await self.highrise.remove_from_voice(tu.id)
                            await self._reply(user.id, self.lang(user.id, 'mic_off', user=f"@{tu.username}"))
                        except:
                            await self._reply(user.id, self.lang(user.id, 'dj_not_found', user=f"@{tu.username}"))
                else:
                    await self._reply(user.id, f"Kullanıcı bulunamadı.")
            except Exception as e:
                print(f"Mic error: {e}")
            return True

        return False

    async def _handle_roles(self, user: User, msg: str) -> bool:
        if msg == "!role":
            roles = list(self.data.get("roles", {}).keys())
            if roles:
                await self._reply(user.id, f"{self.lang(user.id, 'role_list', list=', '.join(roles))}")
            else:
                await self._reply(user.id, f"{self.lang(user.id, 'no_roles')}")
            return True

        match_create = re.match(r"^!createrole\s+(.+)$", msg)
        if match_create:
            if not self.is_owner(user.id):
                await self._reply(user.id, f"{self.lang(user.id, 'not_owner')}")
                return True
            role = match_create.group(1).strip()
            if "roles" not in self.data:
                self.data["roles"] = {}
            self.data["roles"][role] = []
            save_data(self.data)
            await self._reply(user.id, self.lang(user.id, 'role_created', role=role))
            return True

        match_delete = re.match(r"^!deleterole\s+(.+)$", msg)
        if match_delete:
            if not self.is_owner(user.id):
                await self._reply(user.id, f"{self.lang(user.id, 'not_owner')}")
                return True
            role = match_delete.group(1).strip()
            if role in self.data.get("roles", {}):
                del self.data["roles"][role]
                save_data(self.data)
                await self._reply(user.id, self.lang(user.id, 'role_deleted', role=role))
            return True

        match_give = re.match(r"^!giverole\s+@?(\w+)\s+(.+)$", msg)
        if match_give:
            if not self.is_owner(user.id):
                await self._reply(user.id, f"{self.lang(user.id, 'not_owner')}")
                return True
            name = match_give.group(1)
            role = match_give.group(2).strip()
            if role in self.data.get("roles", {}):
                room_users = await self.highrise.get_room_users()
                ru_content = room_users.content if hasattr(room_users, 'content') else room_users
                tu = find_mentioned_user(name, ru_content)
                if tu:
                    if tu.id not in self.data["roles"][role]:
                        self.data["roles"][role].append(tu.id)
                        save_data(self.data)
                    await self._reply(user.id, self.lang(user.id, 'role_given', role=role, user=f"@{tu.username}"))
            return True

        match_role_users = re.match(r"^!role\s+(.+)$", msg)
        if match_role_users:
            role = match_role_users.group(1).strip()
            if role in self.data.get("roles", {}):
                users = self.data["roles"][role]
                if users:
                    names = []
                    try:
                        room_users = await self.highrise.get_room_users()
                        ru_content = room_users.content if hasattr(room_users, 'content') else room_users
                        for ru, _ in ru_content:
                            if ru.id in users:
                                names.append(f"@{ru.username}")
                    except:
                        pass
                    if names:
                        await self._reply(user.id, self.lang(user.id, 'role_users', role=role, list=', '.join(names)))
                    else:
                        await self._reply(user.id, self.lang(user.id, 'role_no_users', role=role))
                else:
                    await self._reply(user.id, self.lang(user.id, 'role_no_users', role=role))
            return True

        return False

    async def _handle_vip(self, user: User, msg: str) -> bool:
        match_add = re.match(r"^!addvip\s+@?(\w+)$", msg)
        if match_add:
            if not self.is_owner(user.id):
                await self._reply(user.id, f"{self.lang(user.id, 'not_owner')}")
                return True
            name = match_add.group(1)
            try:
                room_users = await self.highrise.get_room_users()
                ru_content = room_users.content if hasattr(room_users, 'content') else room_users
                tu = find_mentioned_user(name, ru_content)
                if tu:
                    if "vip_list" not in self.data:
                        self.data["vip_list"] = []
                    if tu.id in self.data["vip_list"]:
                        await self._reply(user.id, self.lang(user.id, 'already_vip', user=f"@{tu.username}"))
                    else:
                        self.data["vip_list"].append(tu.id)
                        save_data(self.data)
                        await self._reply(user.id, self.lang(user.id, 'vip_added', user=f"@{tu.username}"))
                else:
                    await self._reply(user.id, f"Kullanıcı bulunamadı.")
            except Exception as e:
                print(f"Add VIP error: {e}")
            return True

        match_rem = re.match(r"^!removevip\s+@?(\w+)$", msg)
        if match_rem:
            if not self.is_owner(user.id):
                await self._reply(user.id, f"{self.lang(user.id, 'not_owner')}")
                return True
            name = match_rem.group(1)
            try:
                room_users = await self.highrise.get_room_users()
                ru_content = room_users.content if hasattr(room_users, 'content') else room_users
                tu = find_mentioned_user(name, ru_content)
                if tu and "vip_list" in self.data and tu.id in self.data["vip_list"]:
                    self.data["vip_list"].remove(tu.id)
                    save_data(self.data)
                    await self._reply(user.id, self.lang(user.id, 'vip_removed', user=f"@{tu.username}"))
                else:
                    await self._reply(user.id, self.lang(user.id, 'not_vip', user=f"@{name}"))
            except Exception as e:
                print(f"Remove VIP error: {e}")
            return True

        if msg in ["!viplist", "!vips"]:
            vip_list = self.data.get("vip_list", [])
            if vip_list:
                names = []
                try:
                    room_users = await self.highrise.get_room_users()
                    ru_content = room_users.content if hasattr(room_users, 'content') else room_users
                    for ru, _ in ru_content:
                        if ru.id in vip_list:
                            names.append(f"@{ru.username}")
                except:
                    pass
                if names:
                    await self._reply(user.id, self.lang(user.id, 'vip_list', list=', '.join(names)))
                else:
                    await self._reply(user.id, self.lang(user.id, 'no_vip'))
            else:
                await self._reply(user.id, self.lang(user.id, 'no_vip'))
            return True

        return False

    async def _handle_manager(self, user: User, msg: str) -> bool:
        match_add = re.match(r"^!addmanager\s+@?(\w+)$", msg)
        if match_add:
            if not self.is_owner(user.id):
                await self._reply(user.id, f"{self.lang(user.id, 'not_owner')}")
                return True
            name = match_add.group(1)
            try:
                room_users = await self.highrise.get_room_users()
                ru_content = room_users.content if hasattr(room_users, 'content') else room_users
                tu = find_mentioned_user(name, ru_content)
                if tu:
                    if tu.id in self.data.get("manager_list", []):
                        await self._reply(user.id, f"{tu.username} zaten yönetici.")
                    else:
                        self.data.setdefault("manager_list", []).append(tu.id)
                        save_data(self.data)
                        await self._reply(user.id, f"{tu.username} yönetici yapıldı!")
                else:
                    await self._reply(user.id, f"Kullanıcı bulunamadı.")
            except Exception as e:
                print(f"Add manager error: {e}")
            return True

        match_rem = re.match(r"^!removemanager\s+@?(\w+)$", msg)
        if match_rem:
            if not self.is_owner(user.id):
                await self._reply(user.id, f"{self.lang(user.id, 'not_owner')}")
                return True
            name = match_rem.group(1)
            try:
                room_users = await self.highrise.get_room_users()
                ru_content = room_users.content if hasattr(room_users, 'content') else room_users
                tu = find_mentioned_user(name, ru_content)
                if tu and tu.id in self.data.get("manager_list", []):
                    self.data["manager_list"].remove(tu.id)
                    save_data(self.data)
                    await self._reply(user.id, f"{tu.username} yöneticilikten çıkarıldı!")
                else:
                    await self._reply(user.id, f"Kullanıcı bulunamadı veya yönetici değil.")
            except Exception as e:
                print(f"Remove manager error: {e}")
            return True

        if msg in ["!managers", "!yoneticiler"]:
            mgr_list = self.data.get("manager_list", [])
            names = ["labune", "labunem"]
            try:
                room_users = await self.highrise.get_room_users()
                ru_content = room_users.content if hasattr(room_users, 'content') else room_users
                for ru, _ in ru_content:
                    if ru.id in mgr_list and ru.username.lower() not in [n.lower() for n in names]:
                        names.append(f"@{ru.username}")
            except:
                pass
            await self._reply(user.id, f"Yöneticiler: {', '.join(names)}")
            return True

        return False

    async def _handle_fun(self, user: User, msg: str) -> bool:
        if msg == "!flip":
            result = random.choice(["yazi", "tura"])
            text = self.lang(user.id, 'coin_heads') if result == "yazi" else self.lang(user.id, 'coin_tails')
            await self._reply(user.id, f"{self.lang(user.id, 'coin_flip', result=text)}")
            return True

        match_roll = re.match(r"^!roll\s*(\d*)$", msg)
        if match_roll:
            max_num = int(match_roll.group(1)) if match_roll.group(1) else 6
            max_num = max(1, min(1000, max_num))
            result = random.randint(1, max_num)
            await self._reply(user.id, f"{self.lang(user.id, 'dice_roll', result=result)}")
            return True

        match_choose = re.match(r"^!choose\s+(.+)$", msg)
        if match_choose:
            options = [o.strip() for o in match_choose.group(1).split() if o.strip()]
            if options:
                choice = random.choice(options)
                await self._reply(user.id, f"{self.lang(user.id, 'choose_result', choice=choice)}")
            return True

        match_8ball = re.match(r"^!8ball\s+(.+)$", msg)
        if match_8ball:
            question = match_8ball.group(1).strip()
            answers = LANG.get(self.data["user_langs"].get(user.id, "tr"), LANG["tr"])["8ball_responses"]
            answer = random.choice(answers)
            await self._reply(user.id, self.lang(user.id, '8ball_result', question=question, answer=answer))
            return True

        match_rate = re.match(r"^!rate\s+@?(\w+)$", msg)
        if match_rate:
            name = match_rate.group(1)
            score = random.randint(1, 10)
            emojis = ["😭", "😢", "😕", "😐", "🙂", "😊", "😄", "🤩", "😍", "💖", "🌟"]
            await self._reply(user.id, self.lang(user.id, 'rate_result', user=f"@{name}", score=score, emoji=emojis[score]))
            return True

        match_roast = re.match(r"^!roast\s+@?(\w+)$", msg)
        if match_roast:
            name = match_roast.group(1)
            roasts = LANG.get(self.data["user_langs"].get(user.id, "tr"), LANG["tr"])["roast_list"]
            roast = random.choice(roasts).format(user=f"@{name}")
            await self._reply(user.id, f"{roast}")
            return True

        match_love = re.match(r"^!love\s+@?(\w+)\s+@?(\w+)$", msg)
        if match_love:
            u1, u2 = match_love.group(1), match_love.group(2)
            score = random.randint(0, 100)
            await self._reply(user.id, self.lang(user.id, 'love_match', user1=f"@{u1}", user2=f"@{u2}", score=score))
            return True

        match_duel = re.match(r"^!duel\s+@?(\w+)$", msg)
        if match_duel:
            opp = match_duel.group(1)
            winner = random.choice([user.username, opp])
            await self._reply(user.id, f"{self.lang(user.id, 'duel_start', user1=f'@{user.username}', user2=f'@{opp}')}")
            await asyncio.sleep(1)
            await self._reply(user.id, self.lang(user.id, 'duel_result', winner=f"@{winner}"))
            return True

        return False

    async def _handle_mod(self, user: User, msg: str) -> bool:
        if not self.is_owner(user.id):
            return False

        match_mute = re.match(r"^!mute\s+@?(\w+)$", msg)
        if match_mute:
            name = match_mute.group(1)
            try:
                room_users = await self.highrise.get_room_users()
                ru_content = room_users.content if hasattr(room_users, 'content') else room_users
                tu = find_mentioned_user(name, ru_content)
                if tu:
                    await self.highrise.moderate_room(tu.id, "mute", 300)
                    await self._reply(user.id, self.lang(user.id, 'muted', user=f"@{tu.username}"))
            except Exception as e:
                print(f"Mute error: {e}")
            return True

        match_unmute = re.match(r"^!unmute\s+@?(\w+)$", msg)
        if match_unmute:
            name = match_unmute.group(1)
            try:
                room_users = await self.highrise.get_room_users()
                ru_content = room_users.content if hasattr(room_users, 'content') else room_users
                tu = find_mentioned_user(name, ru_content)
                if tu:
                    await self.highrise.moderate_room(tu.id, "unmute")
                    await self._reply(user.id, self.lang(user.id, 'unmuted', user=f"@{tu.username}"))
            except Exception as e:
                print(f"Unmute error: {e}")
            return True

        match_kick = re.match(r"^!kick\s+@?(\w+)$", msg)
        if match_kick:
            name = match_kick.group(1)
            try:
                room_users = await self.highrise.get_room_users()
                ru_content = room_users.content if hasattr(room_users, 'content') else room_users
                tu = find_mentioned_user(name, ru_content)
                if tu:
                    await self.highrise.moderate_room(tu.id, "kick")
                    await self._reply(user.id, self.lang(user.id, 'kicked', user=f"@{tu.username}"))
            except Exception as e:
                print(f"Kick error: {e}")
            return True

        match_ban = re.match(r"^!ban\s+@?(\w+)$", msg)
        if match_ban:
            name = match_ban.group(1)
            try:
                room_users = await self.highrise.get_room_users()
                ru_content = room_users.content if hasattr(room_users, 'content') else room_users
                tu = find_mentioned_user(name, ru_content)
                if tu:
                    await self.highrise.moderate_room(tu.id, "ban")
                    await self._reply(user.id, self.lang(user.id, 'banned', user=f"@{tu.username}"))
            except Exception as e:
                print(f"Ban error: {e}")
            return True

        return False

    async def _handle_settings(self, user: User, msg: str) -> bool:
        if not self.is_owner(user.id):
            return False

        match_welcome = re.match(r"^!welcome\s+(.+)$", msg)
        if match_welcome:
            text = match_welcome.group(1).strip()
            if text.lower() in ["off", "stop", "kapat"]:
                self.data["welcome_message"] = None
                save_data(self.data)
                await self._reply(user.id, self.lang(user.id, 'welcome_disabled'))
            else:
                self.data["welcome_message"] = text
                save_data(self.data)
                await self._reply(user.id, self.lang(user.id, 'welcome_set', msg=text))
            return True

        if msg == "!welcome chat":
            self.data["welcome_mode"] = "chat"
            save_data(self.data)
            await self._reply(user.id, "Welcome mesajları sohbette gönderilecek.")
            return True

        if msg == "!welcome whisper":
            self.data["welcome_mode"] = "whisper"
            save_data(self.data)
            await self._reply(user.id, "Welcome mesajları fısıltı ile gönderilecek.")
            return True

        match_loop = re.match(r"^!loop\s+(.+)$", msg)
        if match_loop:
            text = match_loop.group(1).strip()
            if text.lower() in ["stop", "durdur"]:
                self.data["loop_message"] = None
                save_data(self.data)
                if self.loop_task_ref:
                    self.loop_task_ref.cancel()
                    self.loop_task_ref = None
                await self._reply(user.id, self.lang(user.id, 'loop_stopped'))
            else:
                match_interval = re.match(r"^(\d+)\s+(.+)$", text)
                if match_interval:
                    interval = int(match_interval.group(1))
                    msg_text = match_interval.group(2)
                    self.data["loop_interval"] = interval
                    self.data["loop_message"] = msg_text
                else:
                    self.data["loop_message"] = text
                save_data(self.data)
                if self.loop_task_ref:
                    self.loop_task_ref.cancel()
                self.loop_task_ref = asyncio.create_task(self._loop_messages())
                await self._reply(user.id, self.lang(user.id, 'loop_started', msg=self.data["loop_message"]))
            return True

        match_setjoin = re.match(r"^!setjoin\s+(.+)$", msg)
        if match_setjoin:
            text = match_setjoin.group(1).strip()
            if text.lower() in ["off", "kapat"]:
                self.data["join_message"] = None
                await self._reply(user.id, "Katılma mesajı kaldırıldı.")
            else:
                self.data["join_message"] = text
                save_data(self.data)
                await self._reply(user.id, self.lang(user.id, 'setjoin_set', msg=text))
            return True

        match_setleave = re.match(r"^!setleave\s+(.+)$", msg)
        if match_setleave:
            text = match_setleave.group(1).strip()
            if text.lower() in ["off", "kapat"]:
                self.data["leave_message"] = None
                await self._reply(user.id, "Ayrılma mesajı kaldırıldı.")
            else:
                self.data["leave_message"] = text
                save_data(self.data)
                await self._reply(user.id, self.lang(user.id, 'setleave_set', msg=text))
            return True

        match_alert = re.match(r"^!alert\s+(.+)$", msg)
        if match_alert:
            text = match_alert.group(1).strip()
            self.data["alert_message"] = text
            save_data(self.data)
            await self._reply(user.id, self.lang(user.id, 'alert_set', msg=text))
            return True

        match_thank = re.match(r"^!thank\s+(.+)$", msg)
        if match_thank:
            text = match_thank.group(1).strip()
            self.data["thank_message"] = text
            save_data(self.data)
            await self._reply(user.id, self.lang(user.id, 'thank_set', msg=text))
            return True

        if msg == "!react":
            self.data["auto_react"] = not self.data.get("auto_react", False)
            save_data(self.data)
            key = "autoreact_on" if self.data["auto_react"] else "autoreact_off"
            await self._reply(user.id, self.lang(user.id, key))
            return True

        if msg == "!access":
            self.data["all_access"] = not self.data.get("all_access", False)
            save_data(self.data)
            key = "access_on" if self.data["all_access"] else "access_off"
            await self._reply(user.id, self.lang(user.id, key))
            return True

        return False

    async def _handle_outfits(self, user: User, msg: str) -> bool:
        if not self.is_owner(user.id):
            return False

        match_save = re.match(r"^!savefit\s*(\d*)$", msg)
        if match_save:
            num = int(match_save.group(1)) if match_save.group(1) else 1
            num = max(1, min(10, num))
            try:
                outfit_resp = await self.highrise.get_my_outfit()
                items = outfit_resp.outfit if hasattr(outfit_resp, 'outfit') else []
                if items:
                    wearable = [i for i in items if not getattr(i, 'account_bound', False)]
                    if wearable:
                        self.data["outfits"][str(num)] = [{"id": i.id, "type": i.type, "amount": getattr(i, 'amount', 1), "active_palette": getattr(i, 'active_palette', 0) or 0} for i in wearable]
                        save_data(self.data)
                        await self._reply(user.id, self.lang(user.id, 'save_outfit', num=num))
                    else:
                        await self._reply(user.id, f"Giydirilebilir eşya yok!")
                else:
                    await self._reply(user.id, f"Botun üzerinde eşya yok!")
            except Exception as e:
                print(f"Save outfit error: {e}")
            return True

        match_load = re.match(r"^!loadfit\s*(\d*)$", msg)
        if match_load:
            num = int(match_load.group(1)) if match_load.group(1) else 1
            num = max(1, min(10, num))
            outfit_data = self.data.get("outfits", {}).get(str(num))
            if outfit_data:
                try:
                    items = [Item(id=o["id"], type=o["type"], amount=o.get("amount", 1), active_palette=o.get("active_palette", 0) or 0) for o in outfit_data]
                    await self.highrise.set_outfit(items)
                    await self._reply(user.id, self.lang(user.id, 'load_outfit', num=num))
                except Exception as e:
                    print(f"Load outfit error: {e}")
                    await self._reply(user.id, self.lang(user.id, 'outfit_error', msg=str(e)))
            else:
                await self._reply(user.id, self.lang(user.id, 'no_outfit', num=num))
            return True

        match_copy = re.match(r"^!copy\s+@?(\w+)$", msg)
        if match_copy:
            name = match_copy.group(1)
            try:
                room_users = await self.highrise.get_room_users()
                ru_content = room_users.content if hasattr(room_users, 'content') else room_users
                tu = find_mentioned_user(name, ru_content)
                if tu:
                    outfit_resp = await self.highrise.get_user_outfit(tu.id)
                    items = outfit_resp.outfit if hasattr(outfit_resp, 'outfit') else []
                    if items:
                        wearable = [Item(id=i.id, type=i.type, amount=getattr(i, 'amount', 1), active_palette=getattr(i, 'active_palette', 0) or 0) for i in items if not getattr(i, 'account_bound', False)]
                        if wearable:
                            result = await self.highrise.set_outfit(wearable)
                            if result is None:
                                await self._reply(user.id, self.lang(user.id, 'copy_outfit', user=f"@{tu.username}"))
                    else:
                        await self._reply(user.id, f"{tu.username} üzerinde eşya yok!")
            except Exception as e:
                print(f"Copy outfit error: {e}")
            return True

        return False

    async def _handle_movement(self, user: User, msg: str) -> bool:
        match_goto = re.match(r"^!goto\s+@?(\w+)$", msg)
        if match_goto:
            name = match_goto.group(1)
            try:
                room_users = await self.highrise.get_room_users()
                ru_content = room_users.content if hasattr(room_users, 'content') else room_users
                tu = find_mentioned_user(name, ru_content)
                if tu:
                    for ru, pos in ru_content:
                        if ru.id == tu.id and isinstance(pos, Position):
                            await self.highrise.walk_to(pos)
                            await self._reply(user.id, self.lang(user.id, 'goto', user=f"@{tu.username}"))
                            break
            except Exception as e:
                print(f"Goto error: {e}")
            return True

        match_bring = re.match(r"^!bring\s+@?(\w+)$", msg)
        if match_bring:
            if not self.is_owner(user.id):
                await self._reply(user.id, f"{self.lang(user.id, 'not_owner')}")
                return True
            name = match_bring.group(1)
            try:
                room_users = await self.highrise.get_room_users()
                ru_content = room_users.content if hasattr(room_users, 'content') else room_users
                tu = find_mentioned_user(name, ru_content)
                if tu:
                    for ru, p in ru_content:
                        if ru.id == tu.id and isinstance(p, Position):
                            await self.highrise.walk_to(p)
                            self.follow_target_id = tu.id
                            self.pinned_position = None
                            await self._reply(user.id, self.lang(user.id, 'bring', user=f"@{tu.username}"))
                            break
            except Exception as e:
                print(f"Bring error: {e}")
            return True

        if msg == "!switch":
            try:
                room_users = await self.highrise.get_room_users()
                ru_content = room_users.content if hasattr(room_users, 'content') else room_users
                user_pos = None
                bot_pos = None
                for ru, pos in ru_content:
                    if ru.id == user.id and isinstance(pos, Position):
                        user_pos = pos
                    if ru.id == self.bot_id and isinstance(pos, Position):
                        bot_pos = pos
                if user_pos and bot_pos:
                    await self.highrise.walk_to(user_pos)
                    await self._reply(user.id, self.lang(user.id, 'switch_done'))
            except Exception as e:
                print(f"Switch error: {e}")
            return True

        return False

    async def _handle_social(self, user: User, msg: str) -> bool:
        if msg in ["!sub", "!subscribe"]:
            if "subscribers" not in self.data:
                self.data["subscribers"] = []
            if user.id not in self.data["subscribers"]:
                self.data["subscribers"].append(user.id)
                save_data(self.data)
                try:
                    await self.highrise.send_whisper(user.id, f"@{user.username} 🎉 Tebrikler! Artık ailemizin bir parçasısın! Seni aramızda görmek ne güzel! 💫\n🎉 Congratulations! You're now part of our family! So happy to have you with us! 💫 🙏")
                except:
                    pass
                try:
                    await self.highrise.send_message_bulk([user.id], f"@{user.username} 🎉 Tebrikler! Artık ailemizin bir parçasısın! Seni aramızda görmek ne güzel! 💫\n🎉 Congratulations! You're now part of our family! So happy to have you with us! 💫 🙏")
                except:
                    pass
            else:
                try:
                    await self.highrise.send_whisper(user.id, f"@{user.username} 💖 Zaten aramızdasın! Bizi desteklediğin için çok teşekkürler! Seni seviyoruz! 🥰\n💖 You're already with us! Thank you so much for your support! We love you! 🥰")
                except:
                    pass
                try:
                    await self.highrise.send_message_bulk([user.id], f"@{user.username} 💖 Zaten aramızdasın! Bizi desteklediğin için çok teşekkürler! Seni seviyoruz! 🥰\n💖 You're already with us! Thank you so much for your support! We love you! 🥰")
                except:
                    pass
            return True

        if msg in ["!unsub", "!unsubscribe"]:
            if "subscribers" in self.data and user.id in self.data["subscribers"]:
                self.data["subscribers"].remove(user.id)
                save_data(self.data)
                try:
                    await self.highrise.send_whisper(user.id, f"@{user.username} 😢 Ayrıldığın için üzgünüz! Umarız tekrar görüşürüz! Her zaman bekleriz! 💔\n😢 Sorry to see you go! Hope to see you again! You're always welcome! 💔")
                except:
                    pass
                try:
                    await self.highrise.send_message_bulk([user.id], f"@{user.username} 😢 Ayrıldığın için üzgünüz! Umarız tekrar görüşürüz! Her zaman bekleriz! 💔\n😢 Sorry to see you go! Hope to see you again! You're always welcome! 💔")
                except:
                    pass
            else:
                try:
                    await self.highrise.send_whisper(user.id, f"@{user.username} 🤔 Zaten abone değilsin! Abone olmak için: !sub\n🤔 You're not subscribed! To subscribe: !sub")
                except:
                    pass
                try:
                    await self.highrise.send_message_bulk([user.id], f"@{user.username} 🤔 Zaten abone değilsin! Abone olmak için: !sub\n🤔 You're not subscribed! To subscribe: !sub")
                except:
                    pass
            return True

        if msg in ["!davetetherkesi", "!inviteall"]:
            if not self.is_owner(user.id) and not self.is_manager(user.id):
                await self._reply(user.id, f"{self.lang(user.id, 'no_permission')}")
                return True
            subs = self.data.get("subscribers", [])
            for sid in subs:
                try:
                    await self.highrise.send_whisper(sid, f"📨 @{user.username} sizi odaya davet ediyor! / {user.username} invites you!")
                except:
                    pass
            if subs:
                try:
                    kwargs = {"message_type": "invite"}
                    if self.room_id:
                        kwargs["room_id"] = self.room_id
                    await self.highrise.send_message_bulk(subs, f"@{user.username} sizi odaya davet ediyor!", **kwargs)
                except:
                    pass
            await self._reply(user.id, f"Tüm abonelere davet gönderildi! ({len(subs)} kişi)")
            return True

        match_broadcast = re.match(r"^!broadcast\s+(.+)$", msg)
        if match_broadcast:
            if not self.is_owner(user.id) and not self.is_manager(user.id):
                await self._reply(user.id, f"{self.lang(user.id, 'no_permission')}")
                return True
            text = match_broadcast.group(1).strip()
            subs = self.data.get("subscribers", [])
            count = 0
            for sid in subs:
                try:
                    await self.highrise.send_whisper(sid, f"[Duyuru/Announcement] {text}")
                    count += 1
                except:
                    pass
            if subs:
                try:
                    await self.highrise.send_message_bulk(subs, f"Duyuru/Announcement: {text}")
                except:
                    pass
            await self._reply(user.id, self.lang(user.id, 'broadcast', msg=f"{count} kişiye duyuru yapıldı."))
            return True

        if msg == "!subs":
            count = len(self.data.get("subscribers", []))
            await self._reply(user.id, self.lang(user.id, 'sub_list' if count > 0 else 'no_subs', count=count))
            return True

        if msg == "!invite":
            await self._reply(user.id, f"{self.lang(user.id, 'invite_sent')}")
            return True

        return False

    async def _handle_dancefloor(self, user: User, msg: str) -> bool:
        if not self.is_owner(user.id):
            return False
        match_df = re.match(r"^!dancefloor\s+(.+)$", msg)
        if match_df:
            df_arg = match_df.group(1).strip()
            if df_arg.isdigit() or re.match(r"^\d+-\d+$", df_arg):
                self.data["dancefloor"] = {"corners": df_arg}
                save_data(self.data)
                await self._reply(user.id, self.lang(user.id, 'dancefloor_corners'))
            elif df_arg in DANCE_MAP:
                self.data["dancefloor"] = self.data.get("dancefloor", {})
                self.data["dancefloor"]["emote"] = DANCE_MAP[df_arg]
                save_data(self.data)
                await self._reply(user.id, self.lang(user.id, 'dancefloor_emote', emote=df_arg))
            return True
        return False

    async def _handle_bot_emote(self, user: User, msg: str) -> bool:
        if not self.is_owner(user.id):
            return False
        match_emote = re.match(r"^!emote bot\s+(.+)$", msg)
        if match_emote:
            emote_input = match_emote.group(1).strip().lower()
            if emote_input in DANCE_MAP:
                emote_id = DANCE_MAP[emote_input]
                name = DANCE_NAME_MAP.get(emote_input, emote_input)
                self.data["bot_loop_emote"] = emote_id
                save_data(self.data)
                try:
                    await self.highrise.send_emote(emote_id, user.id)
                except Exception as e:
                    print(f"Bot emote error: {e}")
                await self._reply(user.id, self.lang(user.id, 'bot_emote_set', emote=name))
            else:
                await self._reply(user.id, self.lang(user.id, 'invalid_dance', dances=", ".join(list(DANCE_NAME_MAP.values())[:10])))
            return True
        return False

    async def _stop_youtube(self):
        self.youtube_playing = False
        self.current_youtube_title = None
        sd.stop()

    def _get_best_device(self) -> int:
        devices = sd.query_devices()
        for i, d in enumerate(devices):
            name = d["name"].lower()
            if "cable" in name or "virtual" in name or "vb-" in name:
                if d["max_output_channels"] > 0:
                    return i
        return sd.default.device[1] if sd.default.device[1] >= 0 else 0

    def _find_stereo_mix(self) -> int | None:
        devices = sd.query_devices()
        for i, d in enumerate(devices):
            name = d["name"].lower()
            if d["max_input_channels"] > 0 and ("stereo" in name or "karış" in name or "mix" in name or "what u hear" in name):
                return i
        return None

    def _set_stereo_mix_as_default(self):
        sm_idx = self._find_stereo_mix()
        if sm_idx is None:
            print("⚠️ Stereo Karışımı bulunamadı, varsayılan ayar yapılamadı.")
            return False
        sm_name = sd.query_devices(sm_idx)["name"]
        try:
            import comtypes
            comtypes.CoInitialize()
            devices = AudioUtilities.GetAllDevices(EDataFlow.eCapture.value)
            for dev in devices:
                if sm_name.lower().strip() == dev.FriendlyName.lower().strip():
                    AudioUtilities.SetDefaultDevice(dev.id)
                    print(f"✅ Stereo Karışımı ('{sm_name}') varsayılan kayıt cihazı yapıldı.")
                    return True
            print(f"⚠️ Stereo Karışımı ('{sm_name}') pycaw'da bulunamadı.")
            return False
        except Exception as e:
            print(f"⚠️ Stereo Karışımı varsayılan yapılamadı: {e}")
            return False

    async def _play_youtube(self, query: str, user: User, is_url: bool = False) -> bool:
        def search():
            import yt_dlp
            opts = {"quiet": True, "no_warnings": True, "format": "bestaudio/best", "noplaylist": True}
            with yt_dlp.YoutubeDL(opts) as ydl:
                if is_url:
                    info = ydl.extract_info(query, download=False)
                    return info if info else None
                else:
                    info = ydl.extract_info(f"ytsearch1:{query}", download=False)
                    if not info or "entries" not in info or not info["entries"]:
                        return None
                    return info["entries"][0]

        loop = asyncio.get_event_loop()
        video = await loop.run_in_executor(None, search)
        if video is None:
            return False

        title = video.get("title", query)
        url = video["webpage_url"]
        await self._stop_youtube()

        try:
            await self.highrise.chat(f"🎵 YouTube'da '{title}' bulundu, indiriliyor...")
            await self.highrise.add_user_to_voice(user.id)
        except:
            pass

        def download_and_get_wav():
            import yt_dlp
            out = os.path.join(tempfile.gettempdir(), f"bot_{user.id}")
            opts = {
                "quiet": True, "no_warnings": True, "format": "bestaudio/best",
                "outtmpl": out + ".%(ext)s",
                "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "wav"}],
                "ffmpeg_location": FFMPEG_DIR,
                "max_filesize": 50_000_000,
            }
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
            wav = out + ".wav"
            if os.path.isfile(wav):
                return wav
            for f in os.listdir(tempfile.gettempdir()):
                if f.startswith(f"bot_{user.id}") and f.endswith(".wav"):
                    return os.path.join(tempfile.gettempdir(), f)
            return None

        wav_path = await loop.run_in_executor(None, download_and_get_wav)
        if wav_path is None:
            await self.highrise.chat("❌ Ses indirilemedi.")
            return False

        try:
            data, samplerate = sf.read(wav_path)
            device = self._get_best_device()
            device_name = sd.query_devices(device)["name"]
            sd.play(data, samplerate, device=device)
            self.youtube_playing = True
            self.current_youtube_title = title
            threading.Thread(target=self._cleanup_after_playback, args=(wav_path,), daemon=True).start()
            await self.highrise.chat(f"🎵 Şimdi çalıyor: {title} (🎧 {device_name})")
            return True
        except Exception as e:
            print(f"Playback error: {e}")
            await self.highrise.chat("❌ Ses çalınamadı.")
            return False

    def _cleanup_after_playback(self, wav_path: str):
        try:
            sd.wait()
            self.youtube_playing = False
            self.current_youtube_title = None
        except:
            self.youtube_playing = False
            self.current_youtube_title = None
        finally:
            try:
                if os.path.isfile(wav_path):
                    os.unlink(wav_path)
            except:
                pass

    async def _handle_music(self, user: User, msg: str) -> bool:
        if msg in ["!queue", "!sira"]:
            queue = self.data.get("music_queue", [])
            cs = self.data.get("current_song")
            if not queue and not cs:
                await self._reply(user.id, f"{self.lang(user.id, 'music_queue_empty')}")
                return True
            lines = []
            if cs:
                lines.append(f"▶️ {cs['emote_name']} (@{cs.get('added_by_username', '?')})")
            for i, s in enumerate(queue):
                lines.append(f"{i+1}. {s['emote_name']} (@{s.get('added_by_username', '?')})")
            await self._reply(user.id, f"{self.lang(user.id, 'music_queue_title', count=len(queue))} {' | '.join(lines)}")
            return True

        match_p = re.match(r"^-p\s+(.+)$", msg)
        if match_p:
            song_input = match_p.group(1).strip().lower()
            genre_match = None
            for genre, songs in GENRES.items():
                if song_input == genre or (song_input + " music") == genre or genre.startswith(song_input):
                    genre_match = genre
                    break
            if genre_match:
                genre_songs = [s.capitalize() for s in GENRES[genre_match]]
                if genre_songs:
                    display = ", ".join(genre_songs[:8])
                    extra = f" ve {len(genre_songs)-8} daha" if len(genre_songs) > 8 else ""
                    await self._reply(user.id, f"**{genre_match.upper()}** türü: {display}{extra}")
                    first_song = genre_songs[0].lower()
                    for key in DANCE_MAP:
                        if key == first_song:
                            queue = self.data.setdefault("music_queue", [])
                            queue.append({"emote_id": DANCE_MAP[key], "emote_name": genre_songs[0], "added_by": user.id, "added_by_username": user.username, "genre": genre_match})
                            save_data(self.data)
                            await self._reply(user.id, f"{self.lang(user.id, 'music_added', num=len(queue), song=genre_songs[0])}")
                            break
            elif song_input in DANCE_MAP:
                emote_id = DANCE_MAP[song_input]
                name = DANCE_NAME_MAP.get(song_input, song_input)
                queue = self.data.setdefault("music_queue", [])
                queue.append({"emote_id": emote_id, "emote_name": name, "added_by": user.id, "added_by_username": user.username})
                save_data(self.data)
                await self._reply(user.id, f"{self.lang(user.id, 'music_added', num=len(queue), song=name)}")
            else:
                name = match_p.group(1).strip()
                is_url = name.startswith("http://") or name.startswith("https://")
                if is_url:
                    await self.highrise.chat(f"🎵 YouTube URL indiriliyor...")
                    ok = await self._play_youtube(name, user, is_url=True)
                else:
                    await self.highrise.chat(f"🎵 YouTube'da '{name}' aranıyor...")
                    ok = await self._play_youtube(name, user)
                if not ok:
                    await self.highrise.chat(f"'{name}' YouTube'da bulunamadı.")
            return True

        is_upvote = msg.strip() in ["-up", "-upvote"]
        if msg.startswith("-like ") or msg in ["-like", "!like"] or is_upvote:
            cs = self.data.get("current_song")
            if not cs:
                await self._reply(user.id, f"{self.lang(user.id, 'music_no_current')}")
                return True
            song_key = cs["emote_name"].lower()
            likes = self.data.setdefault("music_likes", {})
            liked = self.data.setdefault("user_liked_songs", {})
            user_id = user.id
            if user_id not in liked:
                liked[user_id] = []
            if song_key in liked[user_id]:
                liked[user_id].remove(song_key)
                likes[song_key] = max(0, likes.get(song_key, 0) - 1)
                await self._reply(user.id, f"{self.lang(user.id, 'music_unliked', song=cs['emote_name'])}")
            else:
                liked[user_id].append(song_key)
                likes[song_key] = likes.get(song_key, 0) + 1
                lib = self.data.setdefault("song_library", {})
                if user_id not in lib:
                    lib[user_id] = []
                if cs["emote_name"] not in lib[user_id]:
                    lib[user_id].append(cs["emote_name"])
                event = self.data.get("event")
                if event and event.get("active"):
                    participants = event.setdefault("participants", {})
                    for pid, pdata in participants.items():
                        if cs["emote_name"].lower() in {s.lower() for s in pdata.get("songs", {})}:
                            pdata["songs"][cs["emote_name"].lower()] = pdata["songs"].get(cs["emote_name"].lower(), 0) + 1
                if is_upvote:
                    queue = self.data.get("music_queue", [])
                    queue.insert(0, {"emote_id": cs["emote_id"], "emote_name": cs["emote_name"], "added_by": user.id, "added_by_username": user.username})
                save_data(self.data)
                key = "music_upvoted" if is_upvote else "music_liked"
                await self._reply(user.id, f"{self.lang(user.id, key, song=cs['emote_name'], count=likes.get(song_key, 0))}")
            return True

        if msg in ["!likes", "!begeniler"]:
            likes = self.data.get("music_likes", {})
            if likes:
                sorted_likes = sorted(likes.items(), key=lambda x: x[1], reverse=True)[:10]
                lines = [f"{s[0]}: {s[1]}❤️" for s in sorted_likes]
                await self._reply(user.id, f"{' | '.join(lines)}")
            else:
                await self._reply(user.id, f"Henüz beğeni yok.")
            return True

        match_add = re.match(r"^!(?:add|ekle)\s+(.+)$", msg)
        if match_add:
            song_input = match_add.group(1).strip().lower()
            if song_input in DANCE_MAP:
                emote_id = DANCE_MAP[song_input]
                name = DANCE_NAME_MAP.get(song_input, song_input)
                queue = self.data.setdefault("music_queue", [])
                queue.append({"emote_id": emote_id, "emote_name": name, "added_by": user.id, "added_by_username": user.username})
                save_data(self.data)
                await self._reply(user.id, f"{self.lang(user.id, 'music_added', num=len(queue), song=name)}")
            else:
                name = match_add.group(1).strip()
                queue = self.data.setdefault("music_queue", [])
                queue.append({"emote_id": None, "emote_name": name, "added_by": user.id, "added_by_username": user.username, "is_song": True})
                save_data(self.data)
                await self._reply(user.id, f"Şarkı sıraya eklendi: '{name}'")
            return True

        match_rem = re.match(r"^!(?:remove|cikar)\s+(\d+)$", msg)
        if match_rem:
            idx = int(match_rem.group(1)) - 1
            queue = self.data.get("music_queue", [])
            if 0 <= idx < len(queue):
                song = queue.pop(idx)
                save_data(self.data)
                await self._reply(user.id, f"{self.lang(user.id, 'music_removed', num=idx+1, song=song['emote_name'])}")
            else:
                await self._reply(user.id, f"{self.lang(user.id, 'music_not_in_queue')}")
            return True

        if msg in ["!skip", "!gec"]:
            if not self.is_owner(user.id):
                await self._reply(user.id, f"{self.lang(user.id, 'not_owner')}")
                return True
            queue = self.data.get("music_queue", [])
            next_song = queue[0]["emote_name"] if queue else self.lang(user.id, 'music_queue_empty')
            self.data["current_song"] = None
            save_data(self.data)
            self.music_skip_event.set()
            await self._reply(user.id, f"{self.lang(user.id, 'music_skipped', song=next_song)}")
            return True

        if msg in ["!clear", "!temizle"]:
            if not self.is_owner(user.id):
                await self._reply(user.id, f"{self.lang(user.id, 'not_owner')}")
                return True
            self.data["music_queue"] = []
            self.data["current_song"] = None
            save_data(self.data)
            await self._reply(user.id, f"{self.lang(user.id, 'music_cleared')}")
            return True

        if msg in ["!nowplaying", "!calan"]:
            cs = self.data.get("current_song")
            if cs:
                await self._reply(user.id, f"{self.lang(user.id, 'music_now_playing', song=cs['emote_name'])}")
            else:
                await self._reply(user.id, f"{self.lang(user.id, 'music_no_current')}")
            return True

        if msg in ["!stopmusic", "!muzikdur"]:
            await self._stop_youtube()
            await self._reply(user.id, "🎵 YouTube müziği durduruldu.")
            return True

        if msg == "!device":
            devices = sd.query_devices()
            out = [f"{i}: {d['name']}" for i, d in enumerate(devices) if d['max_output_channels'] > 0]
            sm = self._find_stereo_mix()
            if sm is not None:
                sm_name = sd.query_devices(sm)["name"]
                await self._reply(user.id, f"🎧 Çıkış: {' | '.join(out[:3])}\n📢 Highrise Ayarlar > Mikrofon > '{sm_name}' seç. Hoparlörünü kısabilirsin, ses yine oyuna gider.")
            else:
                await self._reply(user.id, f"🎧 Çıkış: {' | '.join(out[:3])}\n⚠️ Stereo Karışımı bulunamadı. Ses sadece hoparlörden çıkar.")
            return True

        if msg in ["!shuffle", "!karistir"]:
            settings = self.data.setdefault("music_settings", {})
            settings["shuffle"] = not settings.get("shuffle", False)
            save_data(self.data)
            key = "shuffle_on" if settings["shuffle"] else "shuffle_off"
            await self._reply(user.id, f"{self.lang(user.id, key)}")
            return True

        if msg in ["!repeat", "!tekrar"]:
            settings = self.data.setdefault("music_settings", {})
            settings["repeat"] = not settings.get("repeat", False)
            save_data(self.data)
            key = "repeat_on" if settings["repeat"] else "repeat_off"
            await self._reply(user.id, f"{self.lang(user.id, key)}")
            return True

        match_save_lib = re.match(r"^!savelib\s+(.+)$", msg)
        if match_save_lib:
            name = match_save_lib.group(1).strip().lower()
            cs = self.data.get("current_song")
            song_to_save = name if not cs else cs["emote_name"]
            lib = self.data.setdefault("song_library", {})
            user_id = user.id
            if user_id not in lib:
                lib[user_id] = []
            if song_to_save not in lib[user_id]:
                lib[user_id].append(song_to_save)
                save_data(self.data)
                await self._reply(user.id, f"{self.lang(user.id, 'music_saved', song=song_to_save)}")
            return True

        if msg in ["!mylib", "!kutuphane"]:
            lib = self.data.get("song_library", {})
            user_lib = lib.get(user.id, [])
            if user_lib:
                await self._reply(user.id, f"{self.lang(user.id, 'music_library', count=len(user_lib), list=', '.join(user_lib))}")
            else:
                await self._reply(user.id, f"{self.lang(user.id, 'music_library_empty')}")
            return True

        match_remlib = re.match(r"^!removelib\s+(.+)$", msg)
        if match_remlib:
            name = match_remlib.group(1).strip().lower()
            lib = self.data.get("song_library", {})
            user_lib = lib.get(user.id, [])
            found = None
            for s in user_lib:
                if s.lower() == name:
                    found = s
                    break
            if found:
                user_lib.remove(found)
                save_data(self.data)
                await self._reply(user.id, f"{self.lang(user.id, 'music_removed_lib', song=found)}")
            return True

        match_playlib = re.match(r"^!playlib\s+(.+)$", msg)
        if match_playlib:
            name = match_playlib.group(1).strip().lower()
            lib = self.data.get("song_library", {})
            user_lib = lib.get(user.id, [])
            found_song = None
            for s in user_lib:
                if s.lower() == name:
                    found_song = s
                    break
            if found_song:
                for key, emote_id in DANCE_MAP.items():
                    if key == found_song.lower():
                        queue = self.data.setdefault("music_queue", [])
                        qname = DANCE_NAME_MAP.get(key, found_song)
                        queue.append({"emote_id": emote_id, "emote_name": qname, "added_by": user.id, "added_by_username": user.username})
                        save_data(self.data)
                        await self._reply(user.id, f"{self.lang(user.id, 'music_from_lib', song=qname)}")
                        break
            return True

        match_filter = re.match(r"^!(?:filter|efekt)\s+(.+)$", msg)
        if match_filter:
            effect = match_filter.group(1).strip().lower()
            if effect in ["off", "kapat", "none", "yok"]:
                settings = self.data.setdefault("music_settings", {})
                settings["effect"] = None
                save_data(self.data)
                await self._reply(user.id, f"{self.lang(user.id, 'music_filter_cleared')}")
            elif effect in DANCE_MAP:
                settings = self.data.setdefault("music_settings", {})
                settings["effect"] = DANCE_MAP[effect]
                save_data(self.data)
                await self._reply(user.id, f"{self.lang(user.id, 'music_filter_set', effect=effect)}")
            return True

        match_event_start = re.match(r"^!event\s+start\s+(\d+)$", msg)
        if match_event_start:
            if not self.is_owner(user.id):
                await self._reply(user.id, f"{self.lang(user.id, 'not_owner')}")
                return True
            duration = int(match_event_start.group(1))
            self.data["event"] = {
                "active": True, "start_time": datetime.now().timestamp(),
                "duration": duration, "participants": {}
            }
            save_data(self.data)
            await self._reply(user.id, f"{self.lang(user.id, 'music_event_started', duration=duration)}")
            return True

        if msg in ["!event stop", "!event bitir"]:
            if not self.is_owner(user.id):
                await self._reply(user.id, f"{self.lang(user.id, 'not_owner')}")
                return True
            if self.data.get("event", {}).get("active"):
                self.data["event"]["active"] = False
                save_data(self.data)
                await self._reply(user.id, f"{self.lang(user.id, 'music_event_ended')}")
            return True

        if msg in ["!event status", "!event durum"]:
            event = self.data.get("event")
            if event and event.get("active"):
                elapsed = (datetime.now().timestamp() - event["start_time"]) / 60
                remaining = max(0, event["duration"] - elapsed)
                pcount = len(event.get("participants", {}))
                await self._reply(user.id, f"{self.lang(user.id, 'music_event_status', remaining=int(remaining), participants=pcount)}")
            else:
                await self._reply(user.id, f"Aktif yarışma yok.")
            return True

        if msg in ["!event winners", "!event kazananlar"]:
            event = self.data.get("event")
            if event and event.get("participants"):
                participants = event.get("participants", {})
                if participants:
                    scores = {}
                    for pid, pdata in participants.items():
                        total = sum(pdata.get("songs", {}).values())
                        scores[pid] = {"username": pdata.get("username", "?"), "score": total}
                    sorted_scores = sorted(scores.items(), key=lambda x: x[1]["score"], reverse=True)[:3]
                    lines = [f"{i+1}. {s[1]['username']} ({s[1]['score']} beğeni)" for i, s in enumerate(sorted_scores)]
                    await self._reply(user.id, f"{self.lang(user.id, 'music_event_winners', list=' | '.join(lines))}")
                else:
                    await self._reply(user.id, f"{self.lang(user.id, 'music_event_no_winners')}")
            else:
                await self._reply(user.id, f"{self.lang(user.id, 'music_event_no_winners')}")
            return True

        if msg in ["!voice", "!mikrofon"]:
            settings = self.data.setdefault("music_settings", {})
            settings["voice"] = not settings.get("voice", False)
            save_data(self.data)
            key = "voice_on" if settings["voice"] else "voice_off"
            await self._reply(user.id, f"{self.lang(user.id, key)}")
            return True

        if msg in ["!music", "!muzik"]:
            await self._reply(user.id, f"{self.lang(user.id, 'music_help')}")
            return True

        if msg == "!timelimit":
            await self._reply(user.id, f"{self.lang(user.id, 'time_limit', limit=MAX_SONG_DURATION)}")
            return True

        return False

    async def _music_player(self):
        while True:
            try:
                queue = self.data.get("music_queue", [])
                settings = self.data.get("music_settings", {})
                if queue:
                    if settings.get("shuffle"):
                        idx = random.randint(0, len(queue) - 1)
                        song = queue.pop(idx)
                    else:
                        song = queue.pop(0)
                    if self.dance_loop_task:
                        self.dance_loop_task.cancel()
                        self.dance_loop_task = None
                        self.active_dance_emote_id = None
                    self.data["current_song"] = song
                    save_data(self.data)
                    if song.get("is_song") or song.get("emote_id") is None:
                        random_dance = random.choice(list(DANCE_MAP.values()))
                        await self.highrise.send_emote(random_dance)
                        await self.highrise.chat(f"🎵 Şimdi Çalıyor: {song['emote_name']}")
                    else:
                        emote_id = song["emote_id"]
                        await self.highrise.send_emote(emote_id)
                        effect = settings.get("effect")
                        if effect:
                            await self.highrise.send_emote(effect)
                        await self.highrise.chat(self.owner_lang("music_now_playing", song=song["emote_name"]))
                    event = self.data.get("event")
                    if event and event.get("active"):
                        added_by = song.get("added_by")
                        if added_by:
                            participants = event.setdefault("participants", {})
                            if added_by not in participants:
                                participants[added_by] = {"username": song.get("added_by_username", "?"), "songs": {}}
                            if song["emote_name"].lower() not in participants[added_by]["songs"]:
                                participants[added_by]["songs"][song["emote_name"].lower()] = 0
                            save_data(self.data)
                    try:
                        await asyncio.wait_for(self.music_skip_event.wait(), timeout=min(MAX_SONG_DURATION, 25))
                        self.music_skip_event.clear()
                    except asyncio.TimeoutError:
                        pass
                    if settings.get("repeat"):
                        queue.append(song)
                    self.data["current_song"] = None
                    save_data(self.data)
                else:
                    try:
                        await asyncio.wait_for(self.music_skip_event.wait(), timeout=2)
                        self.music_skip_event.clear()
                    except asyncio.TimeoutError:
                        pass
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Music player error: {e}")
                await asyncio.sleep(5)

    async def _handle_help(self, user: User, msg: str) -> bool:
        if msg in ["!help", "!yardim", "!commands", "!komutlar", "komutlar", "listele", "commands"]:
            dl = self.data["user_langs"].get(user.id, "tr")
            if dl == "tr":
                help_lines = [
                    "Labnem Bot Komutları:",
                    "Dans: <dans_adi/#> | all dance <dans>",
                    "Takip: !follow / !takipet | !stop / !dur | !followtoggle",
                    "Sabitle: !pin / !sabitle | !unpin / !kaldir | !setpos",
                    "Teleport: !create tele <ad> | !tele <ad> [kullanici]",
                    "VIP Tele: !vip tele <ad> | !teleports | !flashmode",
                    "Boost: !boost <sayi> | !wallet | !voicetime",
                    "Bahşiş: !tips | !tiptop | !tipget @user | !tip @user <miktar>",
                    "Müzik: -p <şarkı/tür> (YouTube) | !stopmusic | !device | -up | -like | !queue | !skip | !shuffle | !repeat | !voice",
                    "Müzik: !add/!remove | !filter | !mylib/!playlib | !event | !timelimit",
                    "DJ: !dj @kullanici | !mic @kullanici",
                    "Eğlence: !flip | !roll | !choose | !8ball | !rate | !roast | !love | !duel",
                    "Yetkili: !mute | !unmute | !kick | !ban",
                    "VIP: !addvip | !removevip | !viplist",
                    "Roller: !role | !createrole | !giverole | !deleterole",
                    "Kıyafet: !savefit | !loadfit | !copy @user",
                    "Ayarlar: !welcome | !loop | !setjoin | !setleave | !alert | !thank | !react | !access",
                    "Sosyal: !sub | !unsub | !broadcast | !invite",
                    "Hareket: !goto | !bring | !switch | !flashmode",
                    "Özel: !custom <dans1> <dans2> ... | sayso loop",
                    "Dil: !lang tr/en",
                ]
            else:
                help_lines = [
                    "Labnem Bot Commands:",
                    "Dance: <dance_name/#> | all dance <dance>",
                    "Follow: !follow / !takipet | !stop / !dur | !followtoggle",
                    "Pin: !pin / !sabitle | !unpin / !kaldir | !setpos",
                    "Teleport: !create tele <name> | !tele <name> [user]",
                    "VIP Tele: !vip tele <name> | !teleports | !flashmode",
                    "Boost: !boost <num> | !wallet | !voicetime",
                    "Tips: !tips | !tiptop | !tipget @user | !tip @user <amount>",
                    "Music: -p <song/genre> (YouTube) | !stopmusic | !device | -up | -like | !queue | !skip | !shuffle | !repeat | !voice",
                    "Music: !add/!remove | !filter | !mylib/!playlib | !event | !timelimit",
                    "DJ: !dj @user | !mic @user",
                    "Fun: !flip | !roll | !choose | !8ball | !rate | !roast | !love | !duel",
                    "Mod: !mute | !unmute | !kick | !ban",
                    "VIP: !addvip | !removevip | !viplist",
                    "Roles: !role | !createrole | !giverole | !deleterole",
                    "Outfit: !savefit | !loadfit | !copy @user",
                    "Settings: !welcome | !loop | !setjoin | !setleave | !alert | !thank | !react | !access",
                    "Social: !sub | !unsub | !broadcast | !invite",
                    "Movement: !goto | !bring | !switch | !flashmode",
                    "Custom: !custom <dance1> <dance2> ... | sayso loop",
                    "Language: !lang tr/en",
                ]
            await self._reply(user.id, "\n".join(help_lines))
            return True
        return False
