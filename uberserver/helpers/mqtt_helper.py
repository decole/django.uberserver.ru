from django.core.cache import cache


# functional mqtt-client
def on_message_print(client, userdata, message):
    # print("%s %s" % (message.topic, message.payload))
    processor(message)


def processor(message):
    # print("processor - %s %s" % (message.topic, message.payload))
    print(str(message.payload.decode("utf-8")))

    # cache.set('underground/temperature', str(message.payload), 30)
    # Можно использовать кэш
    # var = cache.get('underground/temperature')
    # print(var)
    # в кэше храним дату последнего обноаления конфига, если оперделенное время не обновлялось то обновляем и в кэш
    # записываем новое время
