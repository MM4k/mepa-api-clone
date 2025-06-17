class CnpjValidator:
    """
    https://blog.dbins.com.br/como-funciona-a-logica-da-validacao-do-cnpj
    https://www.macoratti.net/alg_cnpj.htm
    """

    multipliers_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    multipliers_2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    @classmethod
    def validate(cls, cnpj: str):
        if cnpj == "00000000000000":
            raise Exception("Invalid CNPJ: CNPJ cannot be all zeros")

        if not cnpj.isdecimal() or len(cnpj) != 14:
            raise Exception("CNPJ must contain exactly 14 numerical digits")

        cnpj_digits = [int(d) for d in cnpj]
        cnpj_base = cnpj_digits[:13]
        expected_verified_digits = cnpj_digits[12:]

        verifier_digit_1 = cls._verify_digit(cls.multipliers_1, cnpj_base)
        verifier_digit_2 = cls._verify_digit(cls.multipliers_2, [*cnpj_base, verifier_digit_1])

        if [verifier_digit_1, verifier_digit_2] != expected_verified_digits:
            raise Exception("Invalid CNPJ")

    @staticmethod
    def _verify_digit(multipliers: list[int], base_digits: list[int]) -> int:
        if all(digit == 0 for digit in base_digits):
            raise Exception("Invalid CNPJ: CNPJ cannot be all zeros")

        multiplication_results = []
        for mult, cnpj_base_digit in zip(multipliers, base_digits):
            multiplication_results.append(mult * cnpj_base_digit)
        sum_result = sum(multiplication_results)

        sum_mod_11 = sum_result % 11
        if sum_mod_11 < 2:
            verifier_digit = 0
        else:
            verifier_digit = 11 - sum_mod_11

        return verifier_digit
