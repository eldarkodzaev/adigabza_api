from .settings import MIN_NUMERAL, MAX_NUMERAL


class NumberToKab:
    """
    Translates a numbers from 1 to 999_999_999 into Kabardian
    """

    DIGITS = {
        1: 'зы',
        2: 'тIу',
        3: 'щы',
        4: 'плIы',
        5: 'тху',
        6: 'хы',
        7: 'блы',
        8: 'и',
        9: 'бгъу',
    }

    TEN_TO_NINETEEN = {
        0: 'пщIы',
        1: 'пщыкIуз',
        2: 'пщыкIутI',
        3: 'пщыкIущ',
        4: 'пщыкIуплI',
        5: 'пщыкIутху',
        6: 'пщыкIух',
        7: 'пщыкIубл',
        8: 'пщыкIуий',
        9: 'пщыкIубгъу',
    }

    TENS = {
        2: 'тIощI',
        3: 'щыщI',
        4: 'плIыщI',
        5: 'тхущI',
        6: 'хыщI',
        7: 'блыщI',
        8: 'ищI',
        9: 'бгъущI',
    }

    HUNDREDS = {
        1: 'щэ',
        2: 'щитI',
        3: 'щищ',
        4: 'щиплI',
        5: 'щитху',
        6: 'щих',
        7: 'щибл',
        8: 'щий',
        9: 'щибгъу',
    }

    THOUSANDS_AND_MILLIONS = {
        1: {
            0: '',
            1: 'мин',
            2: 'минитI',
            3: 'минищ',
            4: 'миниплI',
            5: 'минитху',
            6: 'миних',
            7: 'минибл',
            8: 'миний',
            9: 'минибгъу',
            10: 'минипщI',
            100: 'минищэ',
        },

        2: {
            0: '',
            1: 'мелуан',
            2: 'мелуанитI',
            3: 'мелуанищ',
            4: 'мелуаниплI',
            5: 'мелуанитху',
            6: 'мелуаних',
            7: 'мелуанибл',
            8: 'мелуаний',
            9: 'мелуанибгъу',
            10: 'мелуанипщI',
            100: 'мелуанищэ',
        },
    }

    prefixes = {
        0: '',
        1: 'мин',
        2: 'мелуан',
    }

    def __init__(self, number: int):
        if not isinstance(number, int):
            raise TypeError(f"Number must be an integer, got {type(number)} instead")
        if number < MIN_NUMERAL or number > MAX_NUMERAL:
            raise ValueError(f"Number must be in range [{MIN_NUMERAL}, {MAX_NUMERAL}]")
        self.__number = number

    def translate(self) -> str:
        result = self._translate_triad(triad=self.__number % 1000)

        triads = self._split_for_triads()
        for index, triad in triads.items():
            if (triad > 10) and (triad != 100):
                if result:
                    result = f"{self.prefixes[index]} {self._translate_triad(triad)}рэ {result}"
                else:
                    result = f"{self.prefixes[index]} {self._translate_triad(triad)}{result}"
            else:
                if result:
                    suffix = 'рэ ' if triad else ''
                    result = f"{self.THOUSANDS_AND_MILLIONS[index][triad]}{suffix}{result}"
                else:
                    result = f"{self.THOUSANDS_AND_MILLIONS[index][triad]}"

        return result

    def _split_for_triads(self) -> dict:
        """
        Splits a number into triads (groups of 3 digits)
        @return: dict
        """
        # Examples:
        # 23 -> {0: 23}
        # 123 -> {0: 123}
        # 5234 -> {0: 234, 1: 5}
        # 12345 -> {0: 345, 1: 12}
        # 123456 -> {0: 456, 1: 123}

        result = {}
        number = self.__number // 1000
        index = 0
        while number > 0:
            index += 1
            result[index] = number % 1000
            number //= 1000
        return result

    def _translate_triad(self, triad: int) -> str:
        """
        Translates a triad
        @param triad: triad
        @return: str
        """
        result = ""

        if digit := triad % 10:
            result = self.DIGITS[digit]

        if (ten := triad // 10 % 10) > 1:
            tens = self.TENS[ten]
            result = f"{tens}рэ {result}" if digit else f"{tens}{result}"
        elif ten == 1:
            result = self.TEN_TO_NINETEEN[digit]

        if triad := triad // 100:
            hundreds = self.HUNDREDS[triad]
            result = f"{hundreds}рэ {result}" if (ten or digit) else f"{hundreds}{result}"

        return result
