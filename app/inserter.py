from app.models import Church

def init_church():
    mb = Church(name='Miłosierdzia Bożego')
    mb.save()
    f = Church(name='św. Faustyny')
    f.save()

