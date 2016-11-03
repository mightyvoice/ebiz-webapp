from myapp import app


def main():
    # 192.168 .2 .56
    # app.run(debug=False, host='127.0.0.1', port=8000);
    app.run(debug=False, host='192.168.2.56', port=8000);


if __name__ == '__main__':
    main();

