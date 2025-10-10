import connexion
app = connexion.FlaskApp(__name__, specification_dir='./')
app.add_api('open_api_connexion.yaml')
app.run(port=5002)
