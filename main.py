import os
from flask import Flask, request

from homeworker import get_summary

app = Flask('Homeworker')


@app.route('/getSummary', methods=['POST'])
def return_summary():
    if request.method == 'POST':

        body = request.get_json()

        parameters = {
            'topic': 'Sponge Bob', 'lang_to_search': 'en',
            'num_sentences': 6, 'num_references': 3
        }

        try:
            if 'topic' not in body:
                return set_response(400, 'The parameter "topic" is mandatory')
        except:
            body = request.form.to_dict()
            if 'topic' not in body:
                return set_response(400, 'The parameter "topic" is mandatory')

        parameters['topic'] = body['topic']

        optional_parameters = ['lang_to_search',
                               'num_sentences', 'num_references']
        for param in optional_parameters:
            if param in body:
                if param == 'lang_to_search':
                    parameters[param] = body[param]
                else:
                    parameters[param] = int(body[param])

        if parameters['lang_to_search'] == 'en':
            try:
                response = get_summary(**parameters)
            except:
                try:
                    parameters['lang_to_search'] = 'es'
                    response = get_summary(**parameters)
                except:
                    return set_response(404, 'Content not found.')
        else:
            try:
                response = get_summary(**parameters)
            except:
                try:
                    parameters['lang_to_search'] = 'en'
                    response = get_summary(**parameters)
                except:
                    return set_response(404, 'Content not found.')

        return set_response(200, 'Successfully generated summary.', nome_do_conteudo='content', conteudo=response)
    else:
        return set_response(400, 'Unsupported request method')


def set_response(status, mensagem, nome_do_conteudo=False, conteudo=False):
    response = {}
    response['status'] = status
    response['mensagem'] = mensagem

    if nome_do_conteudo and conteudo:
        response[nome_do_conteudo] = conteudo

    return response


def main():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()
