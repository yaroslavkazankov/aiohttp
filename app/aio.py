from aiohttp import web
from view import UsersApi, NoteApi


app = web.Application()


app.add_routes([web.get('/users/', UsersApi),
                web.get('/users/{user_id}', UsersApi),
                web.post('/users/', UsersApi),
                web.patch('/users/{user_id}', UsersApi),
                web.delete('/users/{user_id}', UsersApi),
                web.get('/note/', NoteApi),
                web.get('/note/{note_id}', NoteApi),
                web.post('/note/',  NoteApi),
                web.patch('/note/{note_id}', NoteApi),
                web.delete('/note/{note_id}', NoteApi)
                ]
               )

web.run_app(app, port=9090)
