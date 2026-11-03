# Responsável: João Felipe | Função 4 (Auditoria): data/hora atual formatada e cálculo de dias desde uma data.
# Detalhes em ARQUITETURA.md.
from datetime import datetime, date

def agora_texto ( ):
    return datetime.now().strftime("%d/%m/%Y %H:%M")

def dias_desde (data_texto):
    data = datetime.strptime(data_texto[:10], "%Y-%m-%d").date()
    return (date.today() - data).days