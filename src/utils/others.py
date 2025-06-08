import yaml
from env import ENV

def format_api_url(endpoint: str) -> str:
	"""Formata a URL da API.
	Args:
		endpoint (`str`): Endpoint da API.
	Returns:
		str: URL formatada.
	"""
	url = ENV.INTERNAL_API + endpoint
	return url

def Permissions() -> dict:
	"""Carrega as permissões em Português do arquivo permissions.yml."""
	with open('./src/utils/resources/permissions.yml', 'r', encoding='utf-8') as file:
		return yaml.safe_load(file) or {}