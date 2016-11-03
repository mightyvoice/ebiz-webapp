from myapp import app


def main():
    app.run(debug=False, host='192.168.2.56', port=8000);


if __name__ == '__main__':
    main();

