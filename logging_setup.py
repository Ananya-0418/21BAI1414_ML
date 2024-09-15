import logging

def setup_logging(app):
    logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    @app.before_first_request
    def setup_loggers():
        
        pass
