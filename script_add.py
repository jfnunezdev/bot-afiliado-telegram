with open('bot.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = 'CODIGO_AFILIADO_MERCADOLIBRE = "j20251105190222"'
new = 'CODIGO_AFILIADO_MERCADOLIBRE = "j20251105190222"\n\n\n# Chat privado para recibir notificaciones de publicaciones automáticas\nADMIN_CHAT_ID = 0  # Reemplaza con tu ID numérico de Telegram para recibir avisos'

if old in content:
    content = content.replace(old, new)
    with open('bot.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('ok')
else:
    print('no')
