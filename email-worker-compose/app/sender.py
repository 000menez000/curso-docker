import redis
import json
import os
import psycopg2
from bottle import Bottle, request

SQL = 'INSERT INTO emails (assunto, mensagem) VALUES (%s, %s)'

class Sender(Bottle):
    def __init__(self):
        super().__init__()
        self.route('/', method='POST', callback=self.send)
        redis_host = os.getenv('REDIS_HOST', 'queue')
        self.fila = redis.StrictRedis(redis_host, port=6379, db=0)
        
        self.route('/api/test', method="GET", callback=self.test)
        self.route('/api/listar', method="GET", callback=self.listar)
        
        db_host = os.getenv('DB_HOST', 'db')
        db_user = os.getenv('DB_USER', 'postgres')
        db_name = os.getenv('DB_NAME', 'sender')
        DSN = f'dbname={db_name} user={db_user} host={db_host}'

        self.conn = psycopg2.connect(DSN)
        

    def register_message(self, assunto, mensagem):
        cur = self.conn.cursor()
        cur.execute(SQL, (assunto, mensagem))
        self.conn.commit()
        cur.close()
        
        msg = {'assunto': assunto, 'mensagem': mensagem}
        self.fila.rpush('sender', json.dumps(msg))
        
        print('Mensagem registrada!')
        
    def getAll(self, sql:str):
        cur = self.conn.cursor()
        cur.execute(sql)
        res = cur.fetchall()
        cur.close()
        
        return {'ultimas_mensagens': res}
        
    def send(self):
        assunto = request.forms.get('assunto')
        mensagem = request.forms.get('mensagem')
        
        self.register_message(assunto, mensagem)
        return f'Mensagem enfileirada ! Assunto: {assunto} Mensagem: {mensagem}'

    def test(self):
        return 'API do APP está funcionando'
    
    def listar(self):
        return self.getAll('SELECT * FROM emails ORDER BY id DESC LIMIT 100')
    
    
if __name__ == '__main__':
    sender = Sender()
    sender.run(host='0.0.0.0', port=8080, debug=True)
    