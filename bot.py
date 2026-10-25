import logging
import re
import html
import random
import asyncio
import aiohttp
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ======================== CONFIGURACIÓN ========================
TOKEN = "8920122535:AAELJ-cvDDChqhLp-Boz7tGHt_Xdth9zwJc"
CANAL_ID = "@achadinhos_pixencode"
CODIGO_AFILIADO_SHOPEE = "18339800321"
CODIGO_AFILIADO_MERCADOLIBRE = "j20251105190222"
TIEMPO_ESPERA_PUBLICACION = 1800
# ============================================================

LISTA_INICIAL_REFERENCIA = [
    {"url": "https://shopee.com.br/m/ofertas-diarias", "plataforma": "shopee", "imagen": "https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da?w=800"},
    {"url": "https://shopee.com.br/search?keyword=celular", "plataforma": "shopee", "imagen": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800"},
    {"url": "https://shopee.com.br/search?keyword=smartphone", "plataforma": "shopee", "imagen": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=800"},
    {"url": "https://shopee.com.br/search?keyword=fone%20bluetooth", "plataforma": "shopee", "imagen": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800"},
    {"url": "https://shopee.com.br/search?keyword=notebook", "plataforma": "shopee", "imagen": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800"},
    {"url": "https://shopee.com.br/search?keyword=smart%20tv", "plataforma": "shopee", "imagen": "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=800"},
    {"url": "https://shopee.com.br/search?keyword=air%20fryer", "plataforma": "shopee", "imagen": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=800"},
    {"url": "https://shopee.com.br/search?keyword=ventilador", "plataforma": "shopee", "imagen": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800"},
    {"url": "https://shopee.com.br/search?keyword=geladeira", "plataforma": "shopee", "imagen": "https://images.unsplash.com/photo-1574269909862-7e1d70bb8078?w=800"},
    {"url": "https://shopee.com.br/search?keyword=microondas", "plataforma": "shopee", "imagen": "https://images.unsplash.com/photo-1584269909862-7e1d70bb8078?w=800"},
    {"url": "https://shopee.com.br/search?keyword=tenis%20masculino", "plataforma": "shopee", "imagen": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800"},
    {"url": "https://shopee.com.br/search?keyword=tenis%20feminino", "plataforma": "shopee", "imagen": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=800"},
    {"url": "https://shopee.com.br/search?keyword=mochila", "plataforma": "shopee", "imagen": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800"},
    {"url": "https://shopee.com.br/search?keyword=smartwatch", "plataforma": "shopee", "imagen": "https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=800"},
    {"url": "https://shopee.com.br/search?keyword=perfume", "plataforma": "shopee", "imagen": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=800"},
    {"url": "https://shopee.com.br/search?keyword=maquiagem", "plataforma": "shopee", "imagen": "https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=800"},
    {"url": "https://shopee.com.br/search?keyword=secador%20cabelo", "plataforma": "shopee", "imagen": "https://images.unsplash.com/photo-1522338140262-f46f5913618a?w=800"},
    {"url": "https://shopee.com.br/search?keyword=cadeira%20gamer", "plataforma": "shopee", "imagen": "https://images.unsplash.com/photo-1598550476439-6847785fcea6?w=800"},
    {"url": "https://shopee.com.br/search?keyword=mouse%20gamer", "plataforma": "shopee", "imagen": "https://images.unsplash.com/photo-1612287233002-b1d0ba1395c0?w=800"},
    {"url": "https://shopee.com.br/search?keyword=teclado%20mecanico", "plataforma": "shopee", "imagen": "https://images.unsplash.com/photo-1589578228447-e1a4e481c6c8?w=800"},
    {"url": "https://shopee.com.br/search?keyword=ferramentas", "plataforma": "shopee", "imagen": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800"},
    {"url": "https://shopee.com.br/search?keyword=brinquedos", "plataforma": "shopee", "imagen": "https://images.unsplash.com/photo-1596461404969-9ae70f2830c1?w=800"},
    {"url": "https://shopee.com.br/search?keyword=roupa%20infantil", "plataforma": "shopee", "imagen": "https://images.unsplash.com/photo-1518831959646-742c35aadd53?w=800"},
    {"url": "https://shopee.com.br/search?keyword=camisa%20masculina", "plataforma": "shopee", "imagen": "https://images.unsplash.com/photo-1490114838074-ac394823e960?w=800"},
    {"url": "https://shopee.com.br/search?keyword=vestido", "plataforma": "shopee", "imagen": "https://images.unsplash.com/photo-1483985988355-763728e1935b?w=800"},
    {"url": "https://shopee.com.br/search?keyword=liquidificador", "plataforma": "shopee", "imagen": "https://images.unsplash.com/photo-1574269909862-7e1d70bb8078?w=800"},
    {"url": "https://shopee.com.br/search?keyword=batedeira", "plataforma": "shopee", "imagen": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=800"},
    {"url": "https://shopee.com.br/search?keyword=aspirador%20po", "plataforma": "shopee", "imagen": "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=800"},
    {"url": "https://shopee.com.br/search?keyword=guarda%20roupa", "plataforma": "shopee", "imagen": "https://images.unsplash.com/photo-1484154218962-a197022b5858?w=800"},
    {"url": "https://shopee.com.br/search?keyword=cama%20box", "plataforma": "shopee", "imagen": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=800"},
    {"url": "https://shopee.com.br/search?keyword=sofa", "plataforma": "shopee", "imagen": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800"},
    {"url": "https://shopee.com.br/search?keyword=kit%20cozinha", "plataforma": "shopee", "imagen": "https://images.unsplash.com/photo-1513519245088-0e12902e5a38?w=800"},
    {"url": "https://shopee.com.br/search?keyword=panela%20pressao", "plataforma": "shopee", "imagen": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=800"},
    {"url": "https://shopee.com.br/search?keyword=suplemento", "plataforma": "shopee", "imagen": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=800"},
    {"url": "https://shopee.com.br/search?keyword=whey%20protein", "plataforma": "shopee", "imagen": "https://images.unsplash.com/photo-1593095948071-474c5cc2989d?w=800"},
    {"url": "https://shopee.com.br/search?keyword=bicicleta", "plataforma": "shopee", "imagen": "https://images.unsplash.com/photo-1517649763962-0c623266cf10?w=800"},
    {"url": "https://shopee.com.br/search?keyword=patinete%20eletrico", "plataforma": "shopee", "imagen": "https://images.unsplash.com/photo-1571068316344-75bc76f77890?w=800"},
    {"url": "https://shopee.com.br/search?keyword=caixa%20som", "plataforma": "shopee", "imagen": "https://images.unsplash.com/photo-1545454675-3531b543be5d?w=800"},
    {"url": "https://shopee.com.br/search?keyword=projetor", "plataforma": "shopee", "imagen": "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=800"},
    {"url": "https://shopee.com.br/search?keyword=camera%20seguranca", "plataforma": "shopee", "imagen": "https://images.unsplash.com/photo-1558002038-1055907df827?w=800"},
    {"url": "https://www.mercadolivre.com.br/ofertas", "plataforma": "mercadolibre", "imagen": "https://images.unsplash.com/photo-1607083206869-4c7672e72a8a?w=800"},
    {"url": "https://lista.mercadolivre.com.br/celulares-telefones", "plataforma": "mercadolibre", "imagen": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=800"},
    {"url": "https://lista.mercadolivre.com.br/notebook", "plataforma": "mercadolibre", "imagen": "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=800"},
    {"url": "https://lista.mercadolivre.com.br/smart-tv", "plataforma": "mercadolibre", "imagen": "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=800"},
    {"url": "https://lista.mercadolivre.com.br/fone-bluetooth", "plataforma": "mercadolibre", "imagen": "https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=800"},
    {"url": "https://lista.mercadolivre.com.br/air-fryer", "plataforma": "mercadolibre", "imagen": "https://images.unsplash.com/photo-1574269909862-7e1d70bb8078?w=800"},
    {"url": "https://lista.mercadolivre.com.br/geladeira", "plataforma": "mercadolibre", "imagen": "https://images.unsplash.com/photo-1574269909862-7e1d70bb8078?w=800"},
    {"url": "https://lista.mercadolivre.com.br/microondas", "plataforma": "mercadolibre", "imagen": "https://images.unsplash.com/photo-1584269909862-7e1d70bb8078?w=800"},
    {"url": "https://lista.mercadolivre.com.br/ventilador", "plataforma": "mercadolibre", "imagen": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800"},
    {"url": "https://lista.mercadolivre.com.br/liquidificador", "plataforma": "mercadolibre", "imagen": "https://images.unsplash.com/photo-1574269909862-7e1d70bb8078?w=800"},
    {"url": "https://lista.mercadolivre.com.br/tenis-masculino", "plataforma": "mercadolibre", "imagen": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800"},
    {"url": "https://lista.mercadolivre.com.br/tenis-feminino", "plataforma": "mercadolibre", "imagen": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=800"},
    {"url": "https://lista.mercadolivre.com.br/mochila", "plataforma": "mercadolibre", "imagen": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800"},
    {"url": "https://lista.mercadolivre.com.br/smartwatch", "plataforma": "mercadolibre", "imagen": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800"},
    {"url": "https://lista.mercadolivre.com.br/perfume", "plataforma": "mercadolibre", "imagen": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=800"},
    {"url": "https://lista.mercadolivre.com.br/maquiagem", "plataforma": "mercadolibre", "imagen": "https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=800"},
    {"url": "https://lista.mercadolivre.com.br/secador-cabelo", "plataforma": "mercadolibre", "imagen": "https://images.unsplash.com/photo-1522338140262-f46f5913618a?w=800"},
    {"url": "https://lista.mercadolivre.com.br/cadeira-gamer", "plataforma": "mercadolibre", "imagen": "https://images.unsplash.com/photo-1598550476439-6847785fcea6?w=800"},
    {"url": "https://lista.mercadolivre.com.br/mouse-gamer", "plataforma": "mercadolibre", "imagen": "https://images.unsplash.com/photo-1612287233002-b1d0ba1395c0?w=800"},
    {"url": "https://lista.mercadolivre.com.br/teclado-mecanico", "plataforma": "mercadolibre", "imagen": "https://images.unsplash.com/photo-1589578228447-e1a4e481c6c8?w=800"},
    {"url": "https://lista.mercadolivre.com.br/ferramentas", "plataforma": "mercadolibre", "imagen": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800"},
    {"url": "https://lista.mercadolivre.com.br/brinquedos", "plataforma": "mercadolibre", "imagen": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=800"},
    {"url": "https://lista.mercadolivre.com.br/roupa-infantil", "plataforma": "mercadolibre", "imagen": "https://images.unsplash.com/photo-1518831959646-742c35aadd53?w=800"},
    {"url": "https://lista.mercadolivre.com.br/camisa-masculina", "plataforma": "mercadolibre", "imagen": "https://images.unsplash.com/photo-1490114838074-ac394823e960?w=800"},
    {"url": "https://lista.mercadolivre.com.br/vestido", "plataforma": "mercadolibre", "imagen": "https://images.unsplash.com/photo-1483985988355-763728e1935b?w=800"},
    {"url": "https://lista.mercadolivre.com.br/batedeira", "plataforma": "mercadolibre", "imagen": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=800"},
    {"url": "https://lista.mercadolivre.com.br/aspirador-po", "plataforma": "mercadolibre", "imagen": "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=800"},
    {"url": "https://lista.mercadolivre.com.br/guarda-roupa", "plataforma": "mercadolibre", "imagen": "https://images.unsplash.com/photo-1484154218962-a197022b5858?w=800"},
    {"url": "https://lista.mercadolivre.com.br/cama-box", "plataforma": "mercadolibre", "imagen": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=800"},
    {"url": "https://lista.mercadolivre.com.br/sofa", "plataforma": "mercadolibre", "imagen": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800"},
    {"url": "https://lista.mercadolivre.com.br/kit-cozinha", "plataforma": "mercadolibre", "imagen": "https://images.unsplash.com/photo-1513519245088-0e12902e5a38?w=800"},
    {"url": "https://lista.mercadolivre.com.br/panela-pressao", "plataforma": "mercadolibre", "imagen": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=800"},
    {"url": "https://lista.mercadolivre.com.br/suplemento", "plataforma": "mercadolibre", "imagen": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=800"},
    {"url": "https://lista.mercadolivre.com.br/whey-protein", "plataforma": "mercadolibre", "imagen": "https://images.unsplash.com/photo-1593095948071-474c5cc2989d?w=800"},
    {"url": "https://lista.mercadolivre.com.br/bicicleta", "plataforma": "mercadolibre", "imagen": "https://images.unsplash.com/photo-1517649763962-0c623266cf10?w=800"},
    {"url": "https://lista.mercadolivre.com.br/patinete-eletrico", "plataforma": "mercadolibre", "imagen": "https://images.unsplash.com/photo-1571068316344-75bc76f77890?w=800"},
    {"url": "https://lista.mercadolivre.com.br/caixa-som", "plataforma": "mercadolibre", "imagen": "https://images.unsplash.com/photo-1545454675-3531b543be5d?w=800"},
    {"url": "https://lista.mercadolivre.com.br/projetor", "plataforma": "mercadolibre", "imagen": "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=800"},
    {"url": "https://lista.mercadolivre.com.br/camera-seguranca", "plataforma": "mercadolibre", "imagen": "https://images.unsplash.com/photo-1558002038-1055907df827?w=800"},
    {"url": "https://lista.mercadolivre.com.br/games", "plataforma": "mercadolibre", "imagen": "https://images.unsplash.com/photo-1612287233002-b1d0ba1395c0?w=800"},
]

LISTA_ROTACION = []
ULTIMOS_PUBLICADOS = []
MAX_ULTIMOS = 15

def convertir_enlace_shopee(url: str) -> str:
    try:
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        query["sp_atk"] = [CODIGO_AFILIADO_SHOPEE]
        new_query = urlencode(query, doseq=True)
        return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))
    except Exception:
        return f"{url}&sp_atk={CODIGO_AFILIADO_SHOPEE}" if "?" in url else f"{url}?sp_atk={CODIGO_AFILIADO_SHOPEE}"

def convertir_enlace_mercadolibre(url: str) -> str:
    try:
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        query["matt_tool"] = [CODIGO_AFILIADO_MERCADOLIBRE]
        new_query = urlencode(query, doseq=True)
        return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))
    except Exception:
        return f"{url}&matt_tool={CODIGO_AFILIADO_MERCADOLIBRE}" if "?" in url else f"{url}?matt_tool={CODIGO_AFILIADO_MERCADOLIBRE}"

def extraer_titulo_producto(url: str) -> str:
    if "shopee" in url.lower():
        return "🔥 Achadinhos Especiais da Shopee"
    else:
        return "🔥 Achados Imperdíveis do Mercado Livre"

def ya_publicado_recientemente(url: str) -> bool:
    return url in ULTIMOS_PUBLICADOS

def inicializar_rotacion() -> None:
    global LISTA_ROTACION
    LISTA_ROTACION = list(LISTA_INICIAL_REFERENCIA)
    random.shuffle(LISTA_ROTACION)
    logger.info(f"Lista inicializada con {len(LISTA_ROTACION)} elementos.")

async def extraer_imagen_real(session, url):
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=15), headers={"User-Agent": "Mozilla/5.0"}) as resp:
            html_content = await resp.text()
            m = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']', html_content, re.I)
            if m:
                img = m.group(1).replace("\\/", "/")
                if img.startswith("//"):
                    img = "https:" + img
                if img.startswith("http"):
                    return img
    except Exception as e:
        logger.warning(f"No se pudo extraer imagen real: {e}")
    return None

async def obtener_producto_de_lista(session):
    global LISTA_ROTACION, ULTIMOS_PUBLICADOS
    if not LISTA_ROTACION:
        inicializar_rotacion()
    for item in LISTA_ROTACION:
        url_base = item["url"]
        plataforma = item["plataforma"]
        if ya_publicado_recientemente(url_base):
            continue
        try:
            async with session.get(url_base, timeout=aiohttp.ClientTimeout(total=20), headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}) as resp:
                html_content = await resp.text()
                productos_encontrados = []
                if plataforma == "shopee":
                    links = re.findall(r'href=["\'](/[^"\']*-i\.[^"\']+)["\']', html_content)
                    for l in links[:15]:
                        full = f"https://shopee.com.br{l}" if l.startswith("/") else l
                        if full not in ULTIMOS_PUBLICADOS:
                            productos_encontrados.append(full)
                    if not productos_encontrados:
                        return item
                else:
                    links = re.findall(r'href=["\'](https://produto\.mercadolivre\.com\.br/[^"\']+)["\']', html_content)
                    links += re.findall(r'href=["\'](https://www\.mercadolivre\.com\.br/[^"\']*MLB[0-9]+[^"\']*)["\']', html_content)
                    for full in links[:15]:
                        if full not in ULTIMOS_PUBLICADOS:
                            productos_encontrados.append(full)
                    if not productos_encontrados:
                        return item
                if productos_encontrados:
                    elegido = random.choice(productos_encontrados)
                    return {"url": elegido, "plataforma": plataforma, "imagen": item["imagen"]}
        except Exception as e:
            logger.warning(f"Error scrapeando {url_base}: {e}")
            continue
    logger.info("Ciclo completo, reiniciando rotación...")
    ULTIMOS_PUBLICADOS.clear()
    random.shuffle(LISTA_ROTACION)
    return LISTA_ROTACION[0] if LISTA_ROTACION else None

async def bucle_publicacion_automatica(app: Application) -> None:
    global ULTIMOS_PUBLICADOS
    await asyncio.sleep(5)
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                logger.info("Buscando siguiente producto...")
                item = await obtener_producto_de_lista(session)
                if not item:
                    await asyncio.sleep(TIEMPO_ESPERA_PUBLICACION)
                    continue
                url_original = item["url"]
                plataforma = item["plataforma"]
                imagen_respaldo = item["imagen"]
                imagen_real = await extraer_imagen_real(session, url_original)
                imagen_final = imagen_real if imagen_real else imagen_respaldo

                if plataforma == "shopee":
                    enlace_afiliado = convertir_enlace_shopee(url_original)
                    hashtag = "#Achadinhos #Shopee #Ofertas #Desconto"
                    boton = "🔥 Ver Ofertas na Shopee"
                else:
                    enlace_afiliado = convertir_enlace_mercadolibre(url_original)
                    hashtag = "#Achadinhos #MercadoLivre #Ofertas #Promo"
                    boton = "🔥 Ver Ofertas no Mercado Livre"

                nombre = extraer_titulo_producto(url_original)
                texto = (
                    f"🔥 <b>{html.escape(nombre)}</b>\n\n"
                    f"⚡️ <i>Catálogo oficial con descuentos exclusivos!</i>\n\n"
                    f"🛒 <a href=\"{enlace_afiliado}\">Clique aqui para conferir</a>\n\n"
                    f"{hashtag}\n\n"
                    f"{enlace_afiliado}"
                )
                reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(boton, url=enlace_afiliado)]])
                try:
                    await app.bot.send_photo(
                        chat_id=CANAL_ID,
                        photo=imagen_final,
                        caption=texto,
                        parse_mode="HTML",
                        reply_markup=reply_markup
                    )
                    logger.info(f"Publicado con foto en {CANAL_ID}: {url_original}")
                except Exception as e:
                    logger.warning(f"Fallo foto, envio solo texto: {e}")
                    await app.bot.send_message(
                        chat_id=CANAL_ID,
                        text=texto,
                        parse_mode="HTML",
                        reply_markup=reply_markup,
                        disable_web_page_preview=False
                    )
                ULTIMOS_PUBLICADOS.append(url_original)
                while len(ULTIMOS_PUBLICADOS) > MAX_ULTIMOS * 2:
                    ULTIMOS_PUBLICADOS.pop(0)
            except Exception as e:
                logger.error(f"Error en ciclo: {e}")
            logger.info(f"Próxima en {TIEMPO_ESPERA_PUBLICACION}s")
            await asyncio.sleep(TIEMPO_ESPERA_PUBLICACION)

def main() -> None:
    app = Application.builder().token(TOKEN).build()
    inicializar_rotacion()
    async def post_init(application: Application) -> None:
        application.create_task(bucle_publicacion_automatica(application))
    app.post_init = post_init
    logger.info(f"Bot 80 productos iniciado cada {TIEMPO_ESPERA_PUBLICACION}s en {CANAL_ID}")
    app.run_polling()

if __name__ == "__main__":
    main()