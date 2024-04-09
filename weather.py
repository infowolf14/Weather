from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/favicon.ico':
            self.send_response(404)
            self.end_headers()
            return

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        with open('index.html', 'r') as file:
            html_content = file.read()

        self.wfile.write(html_content.encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            data = json.loads(post_data.decode('utf-8'))
            print("Received data:", data)

            date = data.get('date', '')

            if not date:
                prediction = "Please enter date."
            else:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": "You will be provided with a date. You are to predict the weather in Lagos, Nigeria for that date. You should tell the maximum and minimum temperatures for that day and if it will rain or not. Don't talk too much, just be straight to the point and say the predicted weather"
                        },
                        {
                            "role": "user",
                            "content": f"{date}"
                        }
                    ],
                    temperature=0.1,
                    max_tokens=100,
                    top_p=1
                )
                prediction = response.choices[0].message.content

        except Exception as e:
            print("Error:", e)
            prediction = "Error occurred while generating prediction."

        # Ensure prediction is serializable
        if not isinstance(prediction, str):
            prediction = str(prediction)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        response_data = json.dumps({"prediction": prediction})
        self.wfile.write(response_data.encode('utf-8'))

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting server...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print('Stopping server...')

if __name__ == '__main__':
    run()
    
