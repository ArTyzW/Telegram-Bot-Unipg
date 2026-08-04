import os
from typing import Final
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, filters, ContextTypes, Application
from queue import Queue
import mysql.connector

TOKEN: Final = os.getenv("BOT_TOKEN")
BOT_USERNAME: Final = "@LezioneUnipgBot"
if not TOKEN:
    raise ValueError("ERROR: TOKEN not found! Check the .env file")
try:
    db = mysql.connector.connect(
        host='localhost',  # Insert your MySQL server host
        user="root",       # Insert your database username
        password="",       # Insert your database password
        database="telebot"
   )
    print("connection successful")
except mysql.connector.Error as err:(
    print(f"connection failed"))
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ciao e benvenuto nella nostra chat! 🎉\n"
                                    "Sono il tuo assistente virtuale e sono qui per aiutarti a esplorare le lezioni e darti l'opportunità di prenotare quelle che più ti interessano.\n"
                                    "Per iniziare, puoi:\n"
                                    "Visualizzare l'elenco delle lezioni disponibili 📚\n"
                                    "Prenotare una lezione 🗓️\n"
                                    "Fare domande sulle lezioni o sul processo di prenotazione ❓\n\n"
                                    "Per vedere i comandi digitare /aiuto \n")
async def aiuto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Benvenuto nella nostra chat! Ecco i comandi che puoi utilizzare: \n"
                                    "/login: Effettua il login per identificarti come alunno.\n"
                                    "/logout: Effettua il logout.\n"
                                    "/lista: Visualizza l'elenco delle lezioni disponibili.\n"
                                    "/prenota: Iscriviti a una lezione, se non è già al completo.\n"
                                    "/annulla_iscrizione: annulla iscrizione ad una lezione a tua scelta\n"
                                    "/visualizza_iscrizioni: lista le tue iscrizioni\n"
                                    "Effettua il login per iniziare e buon apprendimento!\n\n"
                                    "NOTA: DOPO AVER FATTO L'ACCESSO CON LA FUNZIONE /login IL MESSAGGIO "
                                    "DELL'UTENTE VERRA' CANCELLATO PER EVITARE CHE LE SUE "
                                    "CREDENZIALI POSSANO ESSERE VISTE E USATE DA NON AUTORIZZATI")
async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:  # ensure there are 2 arguments after login
        await update.message.reply_text('Usa /login <email> <password>.')
        return

    email = context.args[0] # first argument
    password = context.args[1] # second argument

    conn = db.cursor() # database cursor
    conn.execute('SELECT * FROM studente WHERE email = %s AND password = %s', (email, password)) # This query selects all fields (*) from the studente table where email and password match the provided values.
    user = conn.fetchone() # fetchone() returns the first row of the query result, if it exists. If no match is found, it returns None.
    conn.close() # cursor is closed

    if user:
        if 'logged_in_user' in context.chat_data:
            if context.chat_data['logged_in_user'] == email:
                await update.message.reply_text(f'Sei già loggato come {email}.')
            else:
                await update.message.reply_text('Devi fare il logout prima di accedere con un altro account.')
        else:
            context.chat_data['logged_in_user'] = email
            await update.message.reply_text(f'Accesso effettuato come {email}.')
    else:
        await update.message.reply_text('Credenziali non valide.')
    await update.message.delete() # delete user message to increase credentials confidentiality
async def logout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'logged_in_user' in context.chat_data: # if logged in, remove user session state from chat memory
        del context.chat_data['logged_in_user']
        await update.message.reply_text('Logout effettuato.')
    else:
        await update.message.reply_text('Prima devi effettuare il login.')
async def lista(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check connection and cursor status
    if db is None:
        await update.message.reply_text("Connessione al database non riuscita.")
        return
    if 'logged_in_user' not in context.chat_data:
        await update.message.reply_text('Effettua il login prima di poter prenotare.')
        return
    conn = db.cursor() # create cursor

    try:# executes a query across multiple tables in the database to retrieve information
        conn.execute('''                                        
            SELECT 
                lezioni.nome_lezione,
                data_lezione.G_settimana AS giorno,
                data_lezione.ora AS ora,
                aula_fisica.capienza AS classe_capienza,
                corso.nome_corso,
                docenti.nome AS professore_nome,
                docenti.cognome AS professore_cognome,
                docenti.email AS professore_email,
                data_lezione.id_data,
                aula_fisica.id_aula,
                COUNT(prenotazioni.id_prenotazione) AS numero_persone_presenti
            FROM 
                lezioni
            JOIN 
                corso ON lezioni.id_corso = corso.id_corso
            JOIN 
                docenti ON lezioni.id_docente = docenti.id_docente
            JOIN 
                data_lezione ON lezioni.id_lezione = data_lezione.id_lezione
            JOIN 
                aula_fisica ON data_lezione.id_aula = aula_fisica.id_aula
            LEFT JOIN 
                prenotazioni ON data_lezione.id_data = prenotazioni.id_data
            GROUP BY 
                lezioni.nome_lezione,
                data_lezione.G_settimana,
                data_lezione.ora,
                aula_fisica.capienza,
                corso.nome_corso,
                docenti.nome,
                docenti.cognome,
                docenti.email,
                data_lezione.id_data,
                aula_fisica.id_aula
            ORDER BY 
                data_lezione.id_data;
        ''')

        results = conn.fetchall()

        if results:
            response = "Lezioni disponibili:\n\n"
            for row in results: # output formatting
                lezione_nome, giorno, ora, classe_capienza, corso_nome, professore_nome, \
                    professore_cognome, professore_email, id_data, id_aula, numero_persone_presenti = row
                response += (f"ID Lezione: {id_data}\n"
                             f"Lezione: {lezione_nome}\n"
                             f"Giorno: {giorno}\n"
                             f"Ora: {ora}\n"
                             f"Capienza Classe: {classe_capienza} su 2\n"
                             f"Corso: {corso_nome}\n"
                             f"Professore: {professore_nome} {professore_cognome}\n"
                             f"Email Professore: {professore_email}\n"
                             f"ID Aula: {id_aula}\n"
                             f"Persone Prenotate: {numero_persone_presenti}\n\n")
        else:
            response = "Non ci sono lezioni disponibili al momento."

        await update.message.reply_text(response)

    except mysql.connector.Error as e:
        print(f"Errore durante l'esecuzione della query: {e}")
        await update.message.reply_text("Si è verificato un errore durante la lettura delle lezioni.")

    finally:
        if conn:
            conn.close()
async def prenota(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if the user is logged in
    if 'logged_in_user' not in context.chat_data:
        await update.message.reply_text('Effettua il login prima di poter prenotare.')
        return

    try:
        id_data = int(context.args[0])
        matricola = int(context.args[1])
    except (IndexError, ValueError):
        await update.message.reply_text('/prenota <id_lezione> <matricola>')
        return

    conn = db.cursor()

    try:
        # Check if the user is registered (you could skip this step if already verified during login)
        conn.execute('SELECT * FROM studente WHERE matricola = %s', (matricola,))
        user = conn.fetchone()

        if not user:
            await update.message.reply_text('Matricola non registrata. Impossibile effettuare la prenotazione.')
            conn.close()
            return

        # Check if the lesson with the specified id_data exists and check room capacity
        conn.execute('''
            SELECT 
                lezioni.nome_lezione,
                aula_fisica.capienza,
                COUNT(prenotazioni.id_prenotazione) AS numero_prenotazioni
            FROM 
                data_lezione
            JOIN 
                lezioni ON data_lezione.id_lezione = lezioni.id_lezione
            JOIN 
                aula_fisica ON data_lezione.id_aula = aula_fisica.id_aula
            LEFT JOIN 
                prenotazioni ON data_lezione.id_data = prenotazioni.id_data
            WHERE 
                data_lezione.id_data = %s
            GROUP BY 
                data_lezione.id_lezione;
        ''', (id_data,))

        result = conn.fetchone()

        if not result:
            await update.message.reply_text('Lezione non trovata o non è possibile prenotare per questa lezione.')
            conn.close()
            return

        lezione_nome, capienza, numero_prenotazioni = result

        if numero_prenotazioni >= capienza:
            await update.message.reply_text('La classe è piena, non è possibile prenotarsi per questa lezione.')
        else:
            # Check if the student already has a reservation for this lesson
            conn.execute('''
                SELECT * FROM prenotazioni WHERE matricola = %s AND id_data = %s;
            ''', (matricola, id_data))
            prenotazione_esistente = conn.fetchone()

            if prenotazione_esistente:
                await update.message.reply_text('Hai già una prenotazione per questa lezione.')
            else:
                try:
                    # Insert the reservation
                    conn.execute('''
                        INSERT INTO prenotazioni (matricola, id_data)
                        VALUES (%s, %s);
                    ''', (matricola, id_data))
                    db.commit()
                    await update.message.reply_text('Prenotazione effettuata con successo.')
                except mysql.connector.Error as err:
                    await update.message.reply_text(f'Errore durante la prenotazione: {err}')

    except mysql.connector.Error as err:
        await update.message.reply_text(f'Errore durante l\'accesso al database: {err}')

    finally:
        conn.close()
async def annulla_prenotazione(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'logged_in_user' not in context.chat_data:
        await update.message.reply_text('Devi effettuare il login per annullare una prenotazione.')
        return

    try:
        id_data = int(context.args[0])
        matricola = int(context.args[1])
    except (IndexError, ValueError):
        await update.message.reply_text('Uso: /annulla_prenotazione <id_lezione> <matricola>')
        return

    conn = db.cursor()
    try:
        # Check if student ID matches the logged-in user
        email_utente_loggato = context.chat_data['logged_in_user']
        conn.execute('SELECT matricola FROM studente WHERE email = %s', (email_utente_loggato,))
        utente = conn.fetchone()

        if not utente or utente[0] != matricola:
            await update.message.reply_text('Non puoi annullare una prenotazione per questa matricola.')
            return

        # Check if reservation exists
        conn.execute('SELECT * FROM prenotazioni WHERE id_data = %s AND matricola = %s', (id_data, matricola))
        prenotazione = conn.fetchone()

        if not prenotazione:
            await update.message.reply_text('Non esiste una prenotazione con questi dati.')
            return

        # Cancel reservation
        conn.execute('DELETE FROM prenotazioni WHERE id_data = %s AND matricola = %s', (id_data, matricola))
        db.commit()
        await update.message.reply_text('Prenotazione annullata con successo.')

    except mysql.connector.Error as e:
        print(f"Errore durante l'esecuzione della query: {e}")
        await update.message.reply_text("Si è verificato un errore durante l'annullamento della prenotazione.")

    finally:
        if conn:
            conn.close()
async def visualizza_iscrizioni(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'logged_in_user' not in context.chat_data:
        await update.message.reply_text('Devi effettuare il login per visualizzare le tue iscrizioni.')
        return

    conn = db.cursor()
    try:
        # Retrieve student ID of the logged-in user
        email_utente_loggato = context.chat_data['logged_in_user']
        conn.execute('SELECT matricola FROM studente WHERE email = %s', (email_utente_loggato,))
        utente = conn.fetchone()

        if not utente:
            await update.message.reply_text('Errore nel recupero delle informazioni utente.')
            return

        matricola = utente[0]

        # Retrieve user reservations
        conn.execute('''
            SELECT 
                lezioni.nome_lezione,
                data_lezione.G_settimana AS giorno,
                data_lezione.ora AS ora,
                aula_fisica.id_aula AS id_aula,
                corso.nome_corso,
                docenti.nome AS professore_nome,
                docenti.cognome AS professore_cognome,
                docenti.email AS professore_email,
                data_lezione.id_data
            FROM 
                prenotazioni
            JOIN 
                data_lezione ON prenotazioni.id_data = data_lezione.id_data
            JOIN 
                lezioni ON data_lezione.id_lezione = lezioni.id_lezione
            JOIN 
                corso ON lezioni.id_corso = corso.id_corso
            JOIN 
                docenti ON lezioni.id_docente = docenti.id_docente
            JOIN 
                aula_fisica ON data_lezione.id_aula = aula_fisica.id_aula
            WHERE 
                prenotazioni.matricola = %s
            ORDER BY 
                data_lezione.G_settimana, data_lezione.ora;
        ''', (matricola,))

        results = conn.fetchall()

        if results:
            response = "Le tue prenotazioni:\n\n"
            for row in results:
                lezione_nome, giorno, ora, id_aula, corso_nome, professore_nome, professore_cognome, professore_email, id_data = row
                response += (f"Lezione: {lezione_nome}\n"
                             f"Giorno: {giorno}\n"
                             f"Ora: {ora}\n"
                             f"Aula: {id_aula}\n"
                             f"Corso: {corso_nome}\n"
                             f"Professore: {professore_nome} {professore_cognome}\n"
                             f"Email Professore: {professore_email}\n"
                             f"ID Lezione: {id_data}\n\n")
        else:
            response = "Non hai prenotazioni al momento."

        await update.message.reply_text(response)

    except mysql.connector.Error as e:
        print(f"Errore durante l'esecuzione della query: {e}")
        await update.message.reply_text("Si è verificato un errore durante il recupero delle prenotazioni.")

    finally:
        if conn:
            conn.close()
async def errore(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} ha causato {context.error}')


if __name__ == '__main__':
    print('Avviando il bot...')
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("aiuto", aiuto))
    app.add_handler(CommandHandler("login", login))
    app.add_handler(CommandHandler("logout", logout))
    app.add_handler(CommandHandler("lista", lista))
    app.add_handler(CommandHandler("prenota", prenota))
    app.add_handler(CommandHandler("annulla_prenotazione", annulla_prenotazione))
    app.add_handler(CommandHandler("visualizza_iscrizione", visualizza_iscrizioni))


    #errors
    app.add_error_handler(errore)
    print('inizializzando...')
    app.run_polling(poll_interval=3)