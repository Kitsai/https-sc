Para rodar ambos os servidor e o cliente é recomendado utilizar um ambiente virual python. Para fazer isso é necessário ter o virtualenv.
Com ele instalado é possível rodar
```bash
virtualenv .venv
```

e então é preciso ativá-lo 
Linux:
```bash 
source .venv/bin/activate
```
Windows:
```bash
./venv/Scripts/activate
```

Com o venv ativado podemos instalar as dependencias com:
```bash
pip install -r requirements.txt
```

Por fim temos que gerar o certificado e chave privada usando o OpenSSL
Para isso temos que rodar o comando:
```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout key.pem -out cert.pem -config cert.cnf
```
