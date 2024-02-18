# Gerekli olan paketleri ekliyoruz.
from flask import Flask
from flask_restful import Api, Resource, reqparse
import pandas as pd

# Api nesnesini oluşturuyoruz.
app = Flask(__name__)
api = Api(app)

class Users(Resource):
    # Buradaki "get" fonksiyonu içerisine "users.csv" dosyasının okunmasını, sözlük formatına
    # çevirilmesini ve döndürülmesini yazıyoruz.

    #def get(self):
        #data = pd.read_csv('users.csv')
        #data = data.to_dict('records')
        #return {'data' : data}, 200

    # Buradaki "get" fonksiyonun içerisine "users.csv" dosyasının içerisinde
    # bulunan veri sayısına göre yanıt döndürüyoruz.

    def get(self):
        data = pd.read_csv('users.csv')
        num_users = len(data)

        if num_users == 0:
            message = "Henüz kullanıcı bulunmamaktadır."
        else:
            message = f"{num_users} kullanıcı bulunmaktadır. İşte kullanıcı verileri:"

        users_data = data.to_dict('records')
        response_data = {'message': message, 'data': users_data}

        return response_data, 200

    # "post" fonsiyonu içerisine girdilerin ayrıştırılmasını ve "users.csv" dosyasına
    # yeni bir satır olarak eklenmesini yazıyoruz.
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        parser.add_argument('age', required=True)
        parser.add_argument('city', required=True)

        args = parser.parse_args()
        data = pd.read_csv('users.csv')

        new_data = pd.DataFrame({
            'name'      : [args['name']],
            'age'       : [args['age']],
            'city'      : [args['city']]
        })

        data = data.append(new_data, ignore_index = True)
        data.to_csv('users.csv', index=False)
        return {'data' : new_data.to_dict('records')}, 201

class Name(Resource):
    def get(self,name):
        data = pd.read_csv('users.csv')
        data = data.to_dict('records')
        for entry in data:
            if entry['name'] == name :
                return {'data' : entry}, 200
        return {'message' : 'No entry found with this name !'}, 404

# Kaynak adresine yönlendirmek için "add_resource" fonksiyonunu yazıyoruz.
api.add_resource(Users, '/users')
api.add_resource(Name, '/name/<string:name>')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6767)
    app.run()
