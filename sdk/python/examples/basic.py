from openobserve import OpenObserve


logger = OpenObserve(

    api_url="https://logs.muvysystem.com.br/logs",

    token="176825516a56246a6d1092cf635d608056ee330051245ca8968045090c5406dc",

    application="customer-platform",

    service="sdk-test",

    environment="development"

)


#logger.info(
#    "SDK funcionando!"
#)
#
#
#logger.warning(
#    "CPU acima de 80%",
#    {
#        "cpu": 84
#    }
#)
#
#
#logger.error(
#    "Erro ao salvar pedido",
#    {
#        "pedido": 154
#    }
#)