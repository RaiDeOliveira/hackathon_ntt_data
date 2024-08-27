import asyncio
import websockets
import logging

class WebSocketClient:
    _instance = None

    def __new__(cls, url: str):
        if cls._instance is None:
            cls._instance = super(WebSocketClient, cls).__new__(cls)
            cls._instance._initialize(url)
        return cls._instance

    def _initialize(self, url: str):
        if not hasattr(self, "initialized"):
            self.url = url
            self.last_message = None
            self.connected = False
            self.initialized = True  # Marca como inicializado

    async def connect(self):
        """
        Conecta ao WebSocket e escuta continuamente as mensagens.
        """
        try:
            async with websockets.connect(self.url) as websocket:
                self.connected = True
                logging.info(f"Conectado ao WebSocket: {self.url}")
                async for message in websocket:
                    self.last_message = message
                    logging.info(f"Mensagem recebida: {message}")
        except Exception as e:
            logging.exception(f"Erro no WebSocket: {str(e)}")
        finally:
            self.connected = False
            logging.info("Conexão WebSocket fechada.")

    def get_last_message(self):
        """
        Retorna a última mensagem recebida pelo WebSocket.
        """
        return self.last_message


# Função para retornar uma instância única (Singleton) de WebSocketClient
def get_websocket_client(url: str = "ws://localhost:8000/ws") -> WebSocketClient:
    return WebSocketClient(url)
