from flask import Flask
from myapp import app


def main():
    
    #########################################
    #########################################
    # app.run(debug=True, host='192.168.1.139', port=8000);
    app.run(debug=True, host='127.0.0.1', port=8000);


if __name__ == '__main__':
    main();

