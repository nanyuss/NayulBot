from __future__ import annotations

import yaml
from dataclasses import dataclass

def Permissions() -> dict:
	"""Carrega as permissões em Português do arquivo permissions.yml."""
	with open('./nayul/utils/resources/permissions.yml', 'r', encoding='utf-8') as file:
		return yaml.safe_load(file) or {}

@dataclass
class Emoji:
    """Classe para armazenar os emojis do bot."""
    add = '<:add:1373741312221904956>'
    annotation = '<:annotation:1373741328118317077>'
    hypesquad = '<:hypesquad:1373741344056410114>'
    icon_edit = '<:icon_edit:1373741360129249472>'
    icon_role = '<:icon_role:1373741375786451104>'
    icon_settings = '<:icon_settings:1373741391175483514>'
    image = '<:image:1373741407503646880>'
    left = '<:left:1373741423589068950>'
    list = '<:list:1373741439380357120>'
    members = '<:members:1373741455016722455>'
    paleta = '<:paleta:1373741470674194589>'
    paper = '<:paper:1373741486742704190>'
    partner = '<:partner:1373741501909041184>'
    right = '<:right:1373741518195654698>'
    send = '<:send:1373741534100328468>'
    staff = '<:staff:1373741550177091765>'
    webhook = '<:webhook:1373741566149001298>'
    accept = '<:accept:1373741581798080653>'
    active_developer = '<:active_developer:1373741596712894505>'
    back = '<:back:1373741611640688792>'
    banner = '<:banner:1373741626958020660>'
    booster_lv1 = '<:booster_lv1:1373741642259103804>'
    bug_hunter = '<:bug_hunter:1373741657207341076>'
    bug_hunter_level_2 = '<:bug_hunter_level_2:1373741672319680642>'
    check = '<:check:1373741688442323165>'
    crown = '<:crown:1373741703458062560>'
    delete = '<:delete:1373744298264100924>'
    discord_certified_moderator = '<:discord_certified_moderator:1373741719153279071>'
    discord_icon = '<:discord_icon:1373741735410139166>'
    early_supporter = '<:early_supporter:1373741749993996432>'
    error = '<:error:1373741765093359747>'
    exportar = '<:exportar:1373741780939440148>'
    footer = '<:footer:1373741795787411456>'
    hypesquad_balance = '<:hypesquad_balance:1373741810765135963>'
    hypesquad_bravery = '<:hypesquad_bravery:1373741825868824746>'
    hypesquad_brilliance = '<:hypesquad_brilliance:1373741840708141147>'
    icon_badge = '<:icon_badge:1373741855887589499>'
    icon_calendar = '<:icon_calendar:1373741871288815627>'
    icon_category = '<:icon_category:1373741886237442189>'
    icon_emoji = '<:icon_emoji:1373741902742159471>'
    icon_user = '<:icon_user:1373741918109962322>'
    id_icon = '<:id_icon:1373741933830082672>'
    importar = '<:importar:1373741949428699217>'
    info = '<:info:1373741965295751319>'
    loading_v1 = '<a:loading_v1:1373741980852682812>'
    loading_v2 = '<a:loading_v2:1373741995679285269>'
    mention = '<:mention:1373742010762264639>'
    new_member = '<:new_member:1373744312658956444>'
    python = '<:python:1373742028231409694>'
    redwarn = '<:redwarn:1373742044207648890>'
    reject = '<:reject:1373744327792267315>'
    settings_animated = '<a:settings_animated:1373742061765001248>'
    spammer = '<:spammer:1373742076612837496>'
    splash = '<:splash:1373742092534415513>'
    terminal = '<:terminal:1373742108762046484>'
    unverified_bot = '<:unverified_bot:1373742123798630562>'
    verified_bot = '<:verified_bot:1373742138835079310>'
    verified_bot_developer = '<:verified_bot_developer:1373742154031173652>'
    wumpus_helper = '<:wumpus_helper:1373742169096982568>'

    @classmethod
    def as_dict(cls) -> dict:
        """Retorna os emojis como um dicionário."""
        return {k: v for k, v in cls.__dict__.items() if not k.startswith("__")}
