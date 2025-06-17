TariffsNotFoundError = (1, "Lance as tarifas para realizar a análise")
NotEnoughEnergyBills = (2, "Lance ao menos %d faturas para realizar a análise")
NotEnoughEnergyBillsWithAtypical = (
    3,
    f'{NotEnoughEnergyBills[1]}.\nSomente faturas marcadas como "incluir na análise" são consideradas.',
)
PendingBillsWarnning = (4, "Lance mais %d %s dos últimos 12 meses para aumentar a precisão da análise")
ExpiredTariffWarnning = (5, "Atualize as tarifas vencidas para aumentar a precisão da análise")
DuplicatedDateError = (6, "Este mês está duplicado na planilha")
DateNotCoverByContractError = (7, "Selecione uma data a partir de %s. Não existem contratos registrados antes disso.")
FormatDateError = (8, 'O mês deve ser uma data nos formatos "mm/aaaa", "mmm/aaaa" como "abr/2024"')
ValueMaxError = (9, "Valores de Consumo e Demanda devem ser números entre 0,1 e 9.999.999,99")
AlreadyHasEnergyBill = (10, "Já existe uma fatura lançada neste mês")
EnergyBillValueError = (11, "O valor da fatura deve ser um número entre 0,1 e 99.999.999,99")


class ErrorMensageParser:
    @classmethod
    def parse(cls, errorCode: tuple[int, str], subs=None):
        return (errorCode[0], errorCode[1] % subs)
