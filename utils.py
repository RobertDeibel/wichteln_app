import sys, os, random

EMAILS = {}
NAMES = []
WICHTEL = {}


def save_name_email(names, emails):
    for name, email in zip(names, emails):
	    EMAILS[name] = email
	    NAMES.append(name)

def find_wichtel():
    found = False
    while not found:
        found = find_wichtel_helper()
    return found

def find_wichtel_helper():
	temp = NAMES.copy()
	for name in NAMES:
		names = temp.copy()
		try:
			names.remove(name)
		except ValueError:
			pass
		try:
			choice = random.choice(names)
		except:
			return False
		temp.remove(choice)
		WICHTEL[name] = choice

	return _deliver()


def _deliver():
    result = []
    for name in NAMES:
        result.append(_send(name))
    return result

def _send(name):
	message = 'Hallo '+name+', dein Wichtel ist '+WICHTEL[name]+'.\nLass dir was einfallen!'
	return WICHTEL[name], message, EMAILS[name]

if __name__ =='__main__':
    save_name_email(['rob','denise','leo','julian'],['test@bla.com','bla@loeffel.de','vegan@gemuese.co.uk','lulatsch@lang.nl'])

    print(find_wichtel())
    print(WICHTEL)

