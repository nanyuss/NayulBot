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
    reject = '<:reject:1379240667963855039>'
    right = '<:right:1379240666177081438>'
    send = '<:send:1379240666844106865>'
    settings_animated = '<a:settings_animated:1379240666009305139>'
    spammer = '<:spammer:1379240664700813393>'
    splash = '<:splash:1379240667133382728>'
    staff = '<:staff:1379240668639002715>'
    terminal = '<:terminal:1379240669536587776>'
    unverified_bot = '<:unverified_bot:1379240670241493075>'
    verified_bot = '<:verified_bot:1379240671415762964>'
    verified_bot_developer = '<:verified_bot_developer:1379240670639951994>'
    webhook = '<:webhook:1379240672762265611>'
    wumpus_helper = '<:wumpus_helper:1379240673911378032>'
    accept = '<:accept:1379240676293742714>'
    add = '<:add:1379240674477477940>'
    annotation = '<:annotation:1379240676004466719>'
    banner = '<:banner:1379240675098492963>'
    bug_hunter = '<:bug_hunter:1379240677203902485>'
    check = '<:check:1379240677568680087>'
    delete = '<:delete:1379240678508204112>'
    discord_icon = '<:discord_icon:1379240678873366670>'
    early_supporter = '<:early_supporter:1379240679573684275>'
    exportar = '<:exportar:1379240680282394726>'
    hypesquad = '<:hypesquad:1379240681280635002>'
    icon_user = '<:icon_user:1379240683780444213>'
    info = '<:info:1379240684707385424>'
    loading_v1 = '<a:loading_v1:1379240682744578158>'
    mention = '<:mention:1379240683348426782>'
    paper = '<:paper:1379240685152239666>'
    redwarn = '<:redwarn:1379240685634322495>'
    hypesquad_bravery = '<:hypesquad_bravery:1379240686594949181>'
    hypesquad_brilliance = '<:hypesquad_brilliance:1379240686704132180>'
    icon_badge = '<:icon_badge:1379240688323133581>'
    icon_calendar = '<:icon_calendar:1379240687605776476>'
    icon_category = '<:icon_category:1379240688511746090>'
    icon_edit = '<:icon_edit:1379240689468178482>'
    icon_emoji = '<:icon_emoji:1379240689820242010>'
    icon_role = '<:icon_role:1379240691145904239>'
    icon_settings = '<:icon_settings:1379240690810228796>'
    id_icon = '<:id_icon:1379240694203547719>'
    importar = '<:importar:1379240691988697191>'
    list = '<:list:1379240692278362156>'
    members = '<:members:1379240693251444829>'
    paleta = '<:paleta:1379240693632860210>'
    partner = '<:partner:1379240694690091129>'
    active_developer = '<:active_developer:1379240695251861524>'
    back = '<:back:1379240695981670543>'
    booster_lv1 = '<:booster_lv1:1379240696598364291>'
    bug_hunter_level_2 = '<:bug_hunter_level_2:1379240697101549588>'
    crown = '<:crown:1379240697428971614>'
    discord_certified_moderator = '<:discord_certified_moderator:1379240698062176338>'
    error = '<:error:1379240698800373781>'
    footer = '<:footer:1379240699169603656>'
    hypesquad_balance = '<:hypesquad_balance:1379240699605811291>'
    image = '<:image:1379240700155002923>'
    left = '<:left:1379240701195456574>'
    loading_v2 = '<a:loading_v2:1379240703175032930>'
    new_member = '<:new_member:1379240701669150760>'
    python = '<:python:1379240702524915743>'

    @classmethod
    def as_dict(cls) -> dict:
        """Retorna os emojis como um dicionário."""
        return {k: v for k, v in cls.__dict__.items() if not k.startswith("__")}
