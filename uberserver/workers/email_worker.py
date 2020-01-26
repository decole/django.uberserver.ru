from .base_worker import BaseWorker


class EmailWorker(BaseWorker):
    # отправка сообщения через воркер
    def send(self, user, message):
        pass

    # вытаскиваем пачку задач
    def get_scope(self):
        pass

    # запуск воркера
    # стартуем, забираем пачку задач и рассылаем их
    def run(self):
        pass
