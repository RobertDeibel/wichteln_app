from datetime import datetime, timedelta
import utils
from wichteln import db, Wichtel, send_mails, app



DEADLINE = datetime(2018, 12 ,3)
has_wichtel = db.session.query(Wichtel.wichtel).first()[0] != None



if datetime.now() > DEADLINE :
    if not has_wichtel:
        names = [name[0] for name in db.session.query(Wichtel.name).all()]
        emails = [email[0] for email in db.session.query(Wichtel.email).all()]
        utils.save_name_email(names, emails)
        zip_wich_mess_mail = utils.find_wichtel()
        wichtel = []
        message = []
        emails = []
        for zipped in zip_wich_mess_mail:
            wichtel.append(zipped[0])
            message.append(zipped[1])
            emails.append(zipped[2])

        for wicht,beschenkter in zip(Wichtel.query.all(), wichtel):
            wicht.wichtel = beschenkter

        db.session.commit()

        with app.app_context():
            send_mails(message, emails)

