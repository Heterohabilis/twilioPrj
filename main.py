from flask import Flask, request

from API_Sending import getPic, mailSender


app = Flask(__name__)


@app.route('/email', methods=['POST'])
def email_response():
    from_email = request.form['from']
    to_email = request.form['to']
    subject = request.form['subject']
    body = str.split(request.form['text'])[0]

    print('From:', from_email)
    print('To:', to_email)
    print('Subject:', subject)
    print('Body:', body)

    if body.isdigit():
        sol =int(body)
    else:
        sol=-1
    mailSender(to_email,from_email, sol)

    return ''


if __name__ == '__main__':
    app.run(debug=True)
