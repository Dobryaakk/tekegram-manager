def who_text(name, user_id, words_after_bot_kto):
    who = [
        f"Я думаю что <a href='tg://user?id={user_id}'>{name}</a> {words_after_bot_kto}"
        f"Легенда гласит, что <a href='tg://user?id={user_id}'>{name}</a> {words_after_bot_kto}",
        f"Мой кот думает, что <a href='tg://user?id={user_id}'>{name}</a> {words_after_bot_kto}",
        f"По всей видимости <a href='tg://user?id={user_id}'>{name}</a> {words_after_bot_kto}",
        f"Безусловно <a href='tg://user?id={user_id}'>{name}</a> {words_after_bot_kto}",
        f"Слухи утверждают, что <a href='tg://user?id={user_id}'>{name}</a> {words_after_bot_kto}",
        f"Согласно моим данным <a href='tg://user?id={user_id}'>{name}</a> {words_after_bot_kto}",
        f"Загадочный мир ботов утверждает, что <a href='tg://user?id={user_id}'>{name}</a> {words_after_bot_kto}",
        f"Мои боты-коллеги утверждают, что <a href='tg://user?id={user_id}'>{name}</a> {words_after_bot_kto}",
        f"Моя интуиция подсказывает, что <a href='tg://user?id={user_id}'>{name}</a> {words_after_bot_kto}",
        f"Ясно вижу, что <a href='tg://user?id={user_id}'>{name}</a> {words_after_bot_kto}",
        f"Ну тут даже мне понятно, что <a href='tg://user?id={user_id}'>{name}</a> {words_after_bot_kto}"
    ]
    return who


def danet_text(user_id, name):
    danet = [
        '🔍 <b>Безусловно, в этом нет сомнений!</b>',
        '⚖️ <b>Да, конечно, это как дважды два пять.</b>',
        '❓ <b>Я бы сказал, что да, но не скажу.</b>',
        '👀 <b>Это возможно, но не гарантировано.</b>',
        '🔮 <b>Похоже на правду.</b>',
        '🔍 <b>Сомневаюсь, но всегда есть шанс.</b>',
        '⚖️ <b>Да, но с нюансами.</b>',
        '❓ <b>Ответ скорее да, чем нет.</b>',
        '👀 <b>Смотря как посмотреть, но скорее да.</b>',
        '🔮 <b>Не думаю, что это возможно.</b>',
        '🔍 <b>Не стоит на это надеяться.</b>',
        '⚖️ <b>Я не могу сказать точно.</b>',
        '❓ <b>Сложный вопрос.</b>',
        '👀 <b>Не вижу причин для сомнений.</b>',
        '🔮 <b>Спорно, но возможно.</b>',
        '🔍 <b>Ну, скорее нет, чем да.</b>',
        '⚖️ <b>Подождите немного, я думаю...</b>',
        '❓ <b>По всей видимости, да.</b>',
        '👀 <b>Это не исключено.</b>',
        '🔮 <b>Возможно, но не факт.</b>',
        '🔍 <b>Я бы сказал - да, но...</b>',
        '⚖️ <b>Лучше не рассчитывать на это.</b>',
        '❓ <b>Наверное, нет.</b>',
        '👀 <b>Похоже, что да.</b>',
        f"🔮 <b>Спроси у <a href='tg://user?id={user_id}'>{name}</a>.</b>",
        f"🔍 <b>Я уверен, что <a href='tg://user?id={user_id}'>{name}</a> знает ответ.</b>"
    ]
    return danet