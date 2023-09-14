import re
from unidecode import unidecode


class DataNormalizer:

    @staticmethod
    def normalize_address(endereco):
        words_adress = endereco.split()

        # Retira caracteres especiais
        standardized_address = " ".join(
            [unidecode(palavra) for palavra in words_adress])
        standardized_address = standardized_address.upper()

        # Padroniza o name dos logradouros sem abreviação
        standardized_address = re.sub(r"\bR\.?\b", "RUA", standardized_address)
        standardized_address = re.sub(
            r"\bAV\.?\b", "AVENIDA", standardized_address)
        standardized_address = re.sub(
            r"\bTR\.?\b", "TRAVESSA", standardized_address)
        standardized_address = re.sub(
            r"\bESTR\.?\b", "ESTRADA", standardized_address)
        standardized_address = re.sub(
            r"\bPÇA\.?\b", "ESTRADA", standardized_address)

        return standardized_address.replace(".", "")

    @staticmethod
    def normalize_subprefectures(subprefectures):
        words_subprefectures = subprefectures.split()

        # Retira caracteres especiais
        subprefectures_standardized = " ".join(
            [unidecode(words) for words in words_subprefectures])
        return subprefectures_standardized.upper()

    @staticmethod
    def normalize_schools(schools):
        name = schools.upper().strip()

        if "CIEP" in name or "CENTRO INTEGRADO DE EDUCACAO PUBLICA" in name:
            return "CIEP"
        elif name.startswith("EM ") or name.startswith("E.M. ") or name.startswith("E.M ") or "ESCOLA MUNICIPAL" in name:
            return "EM"
        else:
            return "COLÉGIO"
