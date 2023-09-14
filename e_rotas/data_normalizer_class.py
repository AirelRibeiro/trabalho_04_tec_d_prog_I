import re
from unidecode import unidecode


class DataNormalizer:

    @staticmethod
    def normalize_endereco(endereco):
        palavras = endereco.split()

        # Retira caracteres especiais
        endereco_padronizado = " ".join(
            [unidecode(palavra) for palavra in palavras])
        endereco_padronizado = endereco_padronizado.upper()

        # Padroniza o nome dos logradouros sem abreviação
        endereco_padronizado = re.sub(r"\bR\.?\b", "RUA", endereco_padronizado)
        endereco_padronizado = re.sub(
            r"\bAV\.?\b", "AVENIDA", endereco_padronizado)
        endereco_padronizado = re.sub(
            r"\bTR\.?\b", "TRAVESSA", endereco_padronizado)
        endereco_padronizado = re.sub(
            r"\bESTR\.?\b", "ESTRADA", endereco_padronizado)
        endereco_padronizado = re.sub(
            r"\bPÇA\.?\b", "ESTRADA", endereco_padronizado)

        return endereco_padronizado.replace(".", "")

    @staticmethod
    def normalize_subprefeituras(subprefeituras):
        palavras = subprefeituras.split()

        # Retira caracteres especiais
        subprefeituras_padronizado = " ".join(
            [unidecode(palavra) for palavra in palavras])
        return subprefeituras_padronizado.upper()

    @staticmethod
    def normalize_escolas(escolas):
        nome = escolas.upper().strip()

        if "CIEP" in nome or "CENTRO INTEGRADO DE EDUCACAO PUBLICA" in nome:
            return "CIEP"
        elif nome.startswith("EM ") or nome.startswith("E.M. ") or nome.startswith("E.M ") or "ESCOLA MUNICIPAL" in nome:
            return "EM"
        else:
            return "COLÉGIO"
