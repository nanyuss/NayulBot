class Emoji:
    """Classe para armazenar os emojis do bot."""
    accept = '<:accept:1379554735899541588>'
    add = '<:add:1379554735022931969>'
    annotation = '<:annotation:1379554737153900626>'
    banner = '<:banner:1379554737455894579>'
    bug_hunter = '<:bug_hunter:1379554733731352647>'
    check = '<:check:1379554738529636463>'
    delete = '<:delete:1379554740383514794>'
    discord_icon = '<:discord_icon:1379554739762757652>'
    early_supporter = '<:early_supporter:1379554740983042100>'
    exportar = '<:exportar:1379554742023229601>'
    hypesquad = '<:hypesquad:1379554741285027982>'
    icon_user = '<:icon_user:1379554742807564461>'
    info = '<:info:1379554743482847418>'
    loading_v1 = '<a:loading_v1:1379554744174907602>'
    mention = '<:mention:1379554752454725833>'
    paper = '<:paper:1379554745349312515>'
    hypesquad_bravery = '<:hypesquad_bravery:1379554746548883658>'
    hypesquad_brilliance = '<:hypesquad_brilliance:1379554747396128971>'
    icon_badge = '<:icon_badge:1379554747945717818>'
    icon_calendar = '<:icon_calendar:1379554748470136994>'
    icon_category = '<:icon_category:1379554751024201918>'
    icon_edit = '<:icon_edit:1379554750009315339>'
    icon_emoji = '<:icon_emoji:1379554751452024934>'
    icon_role = '<:icon_role:1379554751645093932>'
    icon_settings = '<:icon_settings:1379554752794202182>'
    id_icon = '<:id_icon:1379554753184534649>'
    importar = '<:importar:1379554754027327608>'
    list = '<:list:1379554753880785159>'
    members = '<:members:1379554757865115668>'
    paleta = '<:paleta:1379554755445260438>'
    partner = '<:partner:1379554755931803840>'
    active_developer = '<:active_developer:1379554756493578432>'
    back = '<:back:1379554756942368778>'
    booster_lv1 = '<:booster_lv1:1379554758406443159>'
    bug_hunter_level_2 = '<:bug_hunter_level_2:1379554759782170768>'
    crown = '<:crown:1379554758821417121>'
    discord_certified_moderator = '<:discord_certified_moderator:1379554759564066834>'
    error = '<:error:1379554760478167193>'
    footer = '<:footer:1379554761254371519>'
    hypesquad_balance = '<:hypesquad_balance:1379554761774469304>'
    image = '<:image:1379554762315272212>'
    left = '<:left:1379554763057660156>'
    loading_v2 = '<a:loading_v2:1379554763871354900>'
    new_member = '<:new_member:1379554764752162857>'
    python = '<:python:1379554766027231333>'
    redwarn = '<:redwarn:1379554764332732690>'
    reject = '<:reject:1379554766321094726>'
    right = '<:right:1379554766350192834>'
    send = '<:send:1379554767193505863>'
    settings_animated = '<a:settings_animated:1379554768678027335>'
    spammer = '<:spammer:1379554768342618192>'
    splash = '<:splash:1379554769873404167>'
    staff = '<:staff:1379554768833482934>'
    terminal = '<:terminal:1379554770163073157>'
    unverified_bot = '<:unverified_bot:1379554771165511680>'
    verified_bot = '<:verified_bot:1379554771689537598>'
    verified_bot_developer = '<:verified_bot_developer:1379554772197052427>'
    webhook = '<:webhook:1379554772884918442>'
    wumpus_helper = '<:wumpus_helper:1379554773518389360>'

    @classmethod
    def update(cls, **kwargs):
        """Atualiza os emojis dinamicamente.
        Args:
            kwargs (`dict`): Dicionário de emojis.
        """
        for key, value in kwargs.items():
            setattr(cls, key, value)

    @classmethod
    def as_dict(cls) -> dict:
        """Retorna os emojis como um dicionário."""
        return {k: v for k, v in cls.__dict__.items() if not k.startswith("__")}
