from flask import Flask
from signin import sign
from dash import dash
main=Flask(__name__)
main.secret_key="aigenstory"
main.register_blueprint(sign)
main.register_blueprint(dash)
if __name__ == "__main__":
    main.run(debug=True)