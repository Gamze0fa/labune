from highrise import BaseBot
from highrise.models import SessionMetadata, User, Position, AnchorPosition
from main.emotes import all_emote_list

DANCE_MAP = {}
for i, (name, emote_id) in enumerate(all_emote_list):
    DANCE_MAP[str(i)] = emote_id
    DANCE_MAP[name.lower()] = emote_id

class Bot(BaseBot):
    def __init__(self):
        super().__init__()
        self.follow_target_id = None
        self.room_owner_id = None
        self.song_queue = []

    async def on_start(self, session_metadata: SessionMetadata) -> None:
        print(f"Labnem bot başlatıldı! Bot ID: {session_metadata.user_id}")
        room = await self.highrise.get_room()
        self.room_owner_id = room.content.owner_id

    async def on_chat(self, user: User, message: str) -> None:
        msg = message.lower().strip()

        # Dans - sayı veya dans adı yazılınca
        if msg in DANCE_MAP:
            emote_id = DANCE_MAP[msg]
            if msg.isdigit():
                idx = int(msg)
                if 0 <= idx < len(all_emote_list):
                    name = all_emote_list[idx][0]
                    await self.highrise.chat(f"@{user.username} → {name} (#{msg})")
            else:
                await self.highrise.chat(f"@{user.username} → {msg}")
            await self.highrise.send_emote(emote_id, user.id)
            return

        if msg == "takip et":
            self.follow_target_id = user.id
            await self.highrise.chat(f"@{user.username} seni takip ediyorum!")
            room_users = await self.highrise.get_room_users()
            for room_user, pos in room_users.content:
                if room_user.id == user.id and isinstance(pos, Position):
                    await self.highrise.walk_to(pos)
                    break

        elif msg == "dur":
            self.follow_target_id = None
            await self.highrise.chat(f"@{user.username} olduğum yerde duruyorum.")

        elif message.startswith("-p "):
            song_name = message[3:].strip()
            if not song_name:
                await self.highrise.chat("Lütfen bir şarkı adı girin. Örnek: -p şarkı adı")
                return
            if user.id == self.room_owner_id:
                self.song_queue.insert(0, (user.id, user.username, song_name))
                await self.highrise.chat(f"@{user.username} şarkın 1. sıraya eklendi! (Öncelikli)")
            else:
                self.song_queue.append((user.id, user.username, song_name))
                sıra = next(i + 1 for i, e in enumerate(self.song_queue) if e[0] == user.id)
                await self.highrise.chat(f"@{user.username} şarkın sıraya eklendi! (Sıra: {sıra})")

        elif msg == "!up":
            if not self.song_queue:
                await self.highrise.chat("Sırada şarkı yok.")
                return
            if user.id == self.room_owner_id:
                await self.highrise.chat(f"@{user.username} zaten 1. sıradasınız!")
                return
            idx = next((i for i, e in enumerate(self.song_queue) if e[0] == user.id), None)
            if idx is None:
                await self.highrise.chat(f"@{user.username} sıranız bulunamadı. Önce -p ile şarkı ekleyin.")
                return
            owner_count = sum(1 for e in self.song_queue if e[0] == self.room_owner_id)
            if idx <= owner_count:
                await self.highrise.chat(f"@{user.username} oda sahibinin önüne geçemezsiniz!")
                return
            self.song_queue[idx], self.song_queue[idx - 1] = self.song_queue[idx - 1], self.song_queue[idx]
            await self.highrise.chat(f"@{user.username} bir sıra yükseldiniz! (Sıra: {idx})")

        elif msg.startswith("all dance ") or msg.startswith("all dans "):
            if user.id != self.room_owner_id:
                await self.highrise.chat(f"@{user.username} bu komutu sadece oda sahibi kullanabilir!")
                return
            parts = msg.split(" ", 2)
            if len(parts) < 3:
                await self.highrise.chat("Kullanım: all dance <sayı/isim>")
                return
            dance_input = parts[2].strip()
            emote_id = DANCE_MAP.get(dance_input)
            if not emote_id:
                await self.highrise.chat(f"Geçersiz dans! Kullanılabilir: {', '.join(DANCE_MAP.keys())}")
                return
            room_users = await self.highrise.get_room_users()
            for room_user, _ in room_users.content:
                await self.highrise.send_emote(emote_id, room_user.id)
            await self.highrise.chat(f"@{user.username} herkese {dance_input} dansı yaptırdı!")

        elif msg == "!sira" or msg == "!queue":
            if not self.song_queue:
                await self.highrise.chat("Sırada şarkı yok.")
                return
            lines = [f"{i+1}. {e[1]}: {e[2]}" for i, e in enumerate(self.song_queue)]
            await self.highrise.chat("🎵 Sıra: " + " | ".join(lines))

        elif msg == "!danslar" or msg == "!emotes":
            page = 0
            items_per_page = 20
            total_pages = (len(all_emote_list) + items_per_page - 1) // items_per_page
            start = page * items_per_page
            end = start + items_per_page
            lines = [f"{i}. {all_emote_list[i][0]}" for i in range(start, min(end, len(all_emote_list)))]
            await self.highrise.chat(f"Danslar (Sayfa {page+1}/{total_pages}): " + " | ".join(lines))

    async def on_user_move(self, user: User, pos: Position | AnchorPosition) -> None:
        if self.follow_target_id == user.id and isinstance(pos, Position):
            await self.highrise.walk_to(pos)
