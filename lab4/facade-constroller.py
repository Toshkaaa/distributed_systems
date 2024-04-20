from flask import Flask, request
from facade_service import FacadeService



class FacadeController:
    def __init__(self):
        self.app = Flask(__name__)
        fasadeServ = FacadeService()
        self.FacadeService = fasadeServ

        @self.app.route('/facade-service', methods= ['POST', 'GET'])
        def __index():
            return self.handler_function()
    
    def run_flask_app(self):
        self.app.run(port=4999)  

    def handler_function(self):
        if request.method == 'POST':
            return self.FacadeService.post_req()
        else:
            return self.FacadeService.get_req()
        


if __name__ == "__main__":
    facade_controller = FacadeController()

    facade_controller.run_flask_app()
