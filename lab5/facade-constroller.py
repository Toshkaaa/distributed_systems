from flask import Flask, request
from facade_service import FacadeService
import consul

consul_client = consul.Consul(
    host='localhost',
    port=8500,
)


class FacadeController:

    __port = 4999

    def __init__(self):
        self.app = Flask(__name__)
        fasadeServ = FacadeService()
        self.FacadeService = fasadeServ

        self.register_service_in_consul()
    
        @self.app.route('/facade-service', methods= ['POST', 'GET'])
        def __index():
            return self.handler_function()
    
    def run_flask_app(self):
        self.app.run(port=self.__port)  


    def register_service_in_consul(self):
        consul_client.agent.service.register(service_id=f"facade_service:{str(self.__port)}", name='facade_service', 
            address='127.0.0.1', port=self.__port,
            check={'service_id': f"facade_service:{str(self.__port)}", 'name': 'facade_service',
                'tcp': f'127.0.0.1:{str(self.__port)}',
                'Interval': '5s', 'timeout': '2s'})


    def handler_function(self):
        if request.method == 'POST':
            return self.FacadeService.post_req()
        else:
            return self.FacadeService.get_req()
        


if __name__ == "__main__":

    facade_controller = FacadeController()

    facade_controller.run_flask_app()
