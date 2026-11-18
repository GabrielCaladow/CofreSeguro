# Responsável: João Felipe | Função 4 (Auditoria): data/hora atual formatada e cálculo de dias desde uma data.
from datetime import datetime, date

def agora_texto():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def dias_desde(data_texto):
    """Dias desde a data (aceita 'dd/mm/aaaa' ou 'dd/mm/aaaa hh:mm').
    Retorna None se a data estiver vazia ou inválida."""
    try:
        data = datetime.strptime(data_texto[:10], "%d/%m/%Y").date()
    except (ValueError, TypeError):
        return None
    return (date.today() - data).days