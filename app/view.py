import json
from aiohttp import web
import datetime

from models import Users, Notifications
from alchemyInstruments import AsyncAlchemyInstruments
from sqlalchemy.ext.asyncio import create_async_engine

from crypto import Crypto
from settings import URI


class UsersApi(web.View):
    def __init__(self, request):
        super().__init__(request)
        engine = create_async_engine(URI)
        self.users = AsyncAlchemyInstruments(Users, engine)

    def autentification(self, user_pas: str, input_pas: str):
        return True if user_pas == input_pas else False

    def id_problem(self):
        return {'result': "You requrst don't consist user_id"}

    def passwords_problem(self):
        return {'result': 'Entered passwords are different'}

    def autentification_problem(self):
        return {'result': 'Wrong password entered'}

    def not_user(self):
        return {'result': 'User not found'}

    async def get(self):
        user_id = self.request.match_info.get('user_id')
        users = await self.users.get_entry(int(user_id) if user_id else None)
        if users:
            res = [item.to_dict() for item in users]
        else:
            res = self.not_user()
        return web.json_response(res)

    async def post(self):
        byts = await self.request.read()
        dec = byts.decode(encoding='UTF-8')
        pars = json.loads(dec)

        if pars['password'] == pars['confirm-password']:
            pas = Crypto.cryptor(pars['password'])
            res = await self.users.add_entry(name=pars['name'],
                                             mail=pars['e-mail'],
                                             password=pas
                                             )
        else:
            res = self.passwords_problem()
        return web.json_response(res)

    async def patch(self):
        user_id = self.request.match_info.get('user_id')
        user = await self.users.get_entry(int(user_id))

        if user:
            byts = await self.request.read()
            dec = byts.decode(encoding='UTF-8')
            pars = json.loads(dec)
            input_pas = Crypto.cryptor(pars['password'])
            new_pas = Crypto.cryptor(pars['new_password'])

            if self.autentification(user[0].password, input_pas):
                res = await self.users.update_entry(id=int(user_id),
                                                    name=pars['name'],
                                                    mail=pars['e-mail'],
                                                    password=new_pas
                                                    )
            else:
                res = self.autentification_problem()
        else:
            res = self.not_user()

        return web.json_response(res)

    async def delete(self):
        user_id = self.request.match_info.get('user_id')
        user = await self.users.get_entry(int(user_id))

        if user:
            byts = await self.request.read()
            dec = byts.decode(encoding='UTF-8')
            pars = json.loads(dec)
            input_pas = Crypto.cryptor(pars['password'])

            if self.autentification(user[0].password, input_pas):
                res = await self.users.delete_entry(int(user_id))
            else:
                res = self.autentification_problem()

        else:
            res = self.not_user()

        return web.json_response(res)


class NoteApi(web.View):
    def __init__(self, request):
        super().__init__(request)
        engine = create_async_engine(URI)
        self.note = AsyncAlchemyInstruments(Notifications, engine)
        self.user = AsyncAlchemyInstruments(Users, engine)

    def autentification(self, user_pas: str, input_pas: str):
        return True if user_pas == input_pas else False

    def id_problem(self):
        return {'result': "You requrst don't consist user_id"}

    def passwords_problem(self):
        return {'result': 'Entered passwords are different'}

    def autentification_problem(self):
        return {'result': 'Wrong password entered'}

    def not_note(self):
        return {'result': 'Note not found'}

    def not_user(self, name, mail):
        return {'result': f'User {name} with e-mail {mail} not found'}

    async def get(self):
        note_id = self.request.match_info.get('note_id')
        notes = await self.note.get_entry(int(note_id) if note_id else None)
        if notes:
            res = [item.to_dict() for item in notes]
        else:
            res = self.not_note()
        return web.json_response(res)

    async def post(self):
        byts = await self.request.read()
        dec = byts.decode(encoding='UTF-8')
        pars = json.loads(dec)
        owner = pars['owner']
        mail = pars['e-mail']
        password = pars['password']
        title = pars['title']
        desc = pars['description']

        user = await self.user.find_entry(name=owner, mail=mail)
        if user:
            if self.autentification(user.password, Crypto.cryptor(password)):
                res = await self.note.add_entry(title=title,
                                                description=desc,
                                                date=str(datetime.datetime.now()),
                                                owner_id=user.id
                                                )
            else:
                res = self.autentification_problem()
        else:
            res = self.not_user(user.name, user.mail)
        return web.json_response(res)

    async def patch(self):
        note_id = self.request.match_info.get('note_id')
        note = await self.note.get_entry(int(note_id))
        if note:
            byts = await self.request.read()
            dec = byts.decode(encoding='UTF-8')
            pars = json.loads(dec)
            owner = pars['owner']
            mail = pars['e-mail']
            password = Crypto.cryptor(pars['password'])
            title = pars['title']
            desc = pars['description']

            user = await self.user.find_entry(name=owner, mail=mail)

            if user:
                if self.autentification(user.password, password):
                    res = await self.note.update_entry(id=int(note_id),
                                                       title=title,
                                                       description=desc,
                                                       date=str(datetime.datetime.now()),
                                                       owner_id=user.id
                                                       )
                else:
                    res = self.autentification_problem()
            else:
                res = self.not_user(user.name, user.mail)
        else:
            res = self.not_note()
        return web.json_response(res)

    async def delete(self):
        note_id = self.request.match_info.get('note_id')
        note = await self.user.get_entry(int(note_id))
        if note:
            byts = await self.request.read()
            dec = byts.decode(encoding='UTF-8')
            pars = json.loads(dec)
            owner = pars['owner']
            mail = pars['e-mail']
            password = Crypto.cryptor(pars['password'])

            user = await self.user.find_entry(name=owner, mail=mail)
            if user:
                if self.autentification(user.password, password):
                    res = await self.note.delete_entry(int(note_id))
                else:
                    res = self.autentification_problem()
            else:
                res = self.not_user(owner, mail)
        else:
            res = self.not_note()
        return web.json_response(res)
