from flask import Flask, jsonify, send_from_directory

from controllers.pod_controller import pod_blueprint
from controllers.shipment_controller import shipment_blueprint


def create_app():
    app = Flask(__name__, static_folder=None)

    app.register_blueprint(shipment_blueprint)
    app.register_blueprint(pod_blueprint)

    @app.get("/")
    def index_page():
        return send_from_directory("frontend", "index.html")

    @app.get("/delivery.html")
    def delivery_page():
        return send_from_directory("frontend", "delivery.html")

    @app.get("/api/health")
    def health_check():
        return jsonify({"status": "ok"}), 200

    return app


if __name__ == "__main__":
    app = create_app()
    """app.run(debug=True)"""
    """Para acceso mediante otros dispositivos"""
    app.run(host="0.0.0.0", port=5000, debug=True)
