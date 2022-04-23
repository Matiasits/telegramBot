from logging import Filter
from urllib import request
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from newsapi import NewsApiClient

#Crear un archivo env.py para guardar nuestras credenciales
from env import NEWS_API_KEY, BOT_TOKEN

#Creamos la intefaz con la API de Noticas.
newsapi = NewsApiClient(api_key=NEWS_API_KEY)


def start(update, context):
    # Configuramos el comando start para enviar un mensaje de bienvenida
    update.message.reply_text('Bienvenido, escribe algo para comenzar a buscar noticias.')


def help(update, context):
    # Configuramos el comando help para enviar un mensaje con instrucciones
    update.message.reply_text('Hola escriba algunas palabras clave para empezar a buscar noticias en la web.')

def echo(update, context):
    all_articles = newsapi.get_everything(
        #q va a ser el texto que queremos buscar, en este caso lo que introdujo el usuario
        q=update.message.text,
        #sources son los medios en los que queremos buscar, en la documentación aparecen todos
        sources='bbc-news,the-verge,abc-news-au,bbc-sport,bloomberg,crypto-coins-news,engadget,espn,national-geographic',
        #definimos también el lenguaje y ordenamos por relevancia
        language='en',
        sort_by='relevancy'
        )
    # Puede darse el caso de que obtengamos cientos de resultados, y seria incómodo para el usuario tener tantas noticias así que nos quedamos con las últimas 3 y las mandamos
    for i in all_articles['articles'][:3]:
        update.message.reply_text("%s\n\n%s" % (i['source']['name'], i['url']))
    # En caso de que no se encuentren resultados le avisamos al usuario
    if len(all_articles['articles']) == 0:
        update.message.reply_text('No se han encontrado noticias relacionadas. Intente simplificar lo que desea con palabras clave.')

def main():
    # Creamos el Updater y le pasamos el token de nuestro bot. Este se encargará de manejar las peticiones de los usuarios.
    updater = Updater(BOT_TOKEN, use_context=True)

    # Obtenemos el Dispatcher para crear los comandos
    dp = updater.dispatcher
    # Creamos el comando /start y definimos que se ejecute este mismo método
    dp.add_handler(CommandHandler("start", start))
    # Creamos el comando /help y definimos que se ejecute el método help
    dp.add_handler(CommandHandler("help", help))   

    dp.add_handler(MessageHandler(Filters.text, echo))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()