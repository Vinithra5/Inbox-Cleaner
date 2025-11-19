# Inbox-Cleaner
Inbox Cleaner scans your Gmail inbox, picks out newsletters and promotional emails, and pulls up all the unsubscribe links in one clean dashboard — so you don’t have to open every email manually.

I built this because my inbox was messy, and this tool made it easier to stay organized.

How to Run
git clone https://github.com/Vinithra5/Inbox-Cleaner.git
cd Inbox-Cleaner

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
streamlit run app.py


Add your credentials.json (Google OAuth) to the folder before running.

Structure
app.py              # UI
inboxcleaner.py     # Gmail scanning logic
credentials.json    # OAuth (ignored on GitHub)
token.json          # Saved token (ignored)

Privacy Concerns

Your Gmail data is not stored or sent anywhere.
Everything runs locally, and you can remove access anytime from Google settings.
