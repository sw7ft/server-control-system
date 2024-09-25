import http.server
import socketserver
import subprocess
import os
import cgi

PORT = 8015

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # HTML form for inputting commands with predefined SSH configs and saved commands
            html_content = """
            <html>
            <head>
                <title>Run Commands</title>
                <script>
                    // Predefined SSH configurations
                    var sshConfigs = {
                        'config1': {
                            'user': '',
                            'host': '',
                            'password': '',
                            'port': ''
                        },
                        'config2': {
                            'user': '',
                            'host': '',
                            'password': '',
                            'port': ''
                        },
                        'config3': {
                            'user': 'user3',
                            'host': 'host3.example.com',
                            'password': 'password3',
                            'port': '2200'
                        },
                        'config4': {
                            'user': 'user4',
                            'host': 'host4.example.com',
                            'password': 'password4',
                            'port': '2201'
                        },
                        'config5': {
                            'user': 'user5',
                            'host': 'host5.example.com',
                            'password': 'password5',
                            'port': '2202'
                        },
                        'config6': {
                            'user': 'user6',
                            'host': 'host6.example.com',
                            'password': 'password6',
                            'port': '2203'
                        },
                        'config7': {
                            'user': 'user7',
                            'host': 'host7.example.com',
                            'password': 'password7',
                            'port': '2204'
                        },
                        'config8': {
                            'user': 'user8',
                            'host': 'host8.example.com',
                            'password': 'password8',
                            'port': '2205'
                        }
                    };

                    // Predefined saved commands
                    var savedCommands = {
                        'cmd1': 'top -b -n 1 | grep \\'load average\\'',
                        'cmd2': 'free -m | awk \\'/Mem:/ {print \\"Free Memory:\\", $4, \\"MB\\"}\\'',
                        'cmd3': 'df -h / | awk \\'NR==2 {print \\"Disk Space Free:\\", $4}\\'',
                        'cmd4': 'uptime',
                        'cmd5': 'ls -l /var/www',
                        'cmd6': 'ps aux --sort=-%mem | head -5',
                        'cmd7': 'netstat -tuln',
                        'cmd8': 'cat /etc/os-release'
                    };

                    // Function to autofill SSH configuration
                    function selectSSHConfig(configKey) {
                        var config = sshConfigs[configKey];
                        if(config) {
                            document.getElementById('user').value = config['user'];
                            document.getElementById('host').value = config['host'];
                            document.getElementById('password').value = config['password'];
                            document.getElementById('port').value = config['port'];
                        } else {
                            alert('SSH Configuration not found.');
                        }
                    }

                    // Function to autofill saved command
                    function selectSavedCommand(cmdKey) {
                        var command = savedCommands[cmdKey];
                        if(command) {
                            document.getElementById('command').value = command;
                        } else {
                            alert('Saved command not found.');
                        }
                    }

                    // Function to send command to the server
                    function sendCommand() {
                        var user = document.getElementById('user').value;
                        var host = document.getElementById('host').value;
                        var password = document.getElementById('password').value;
                        var port = document.getElementById('port').value;
                        var command = document.getElementById('command').value;

                        var xhr = new XMLHttpRequest();
                        var params = 'user=' + encodeURIComponent(user) + 
                                     '&host=' + encodeURIComponent(host) + 
                                     '&password=' + encodeURIComponent(password) +
                                     '&port=' + encodeURIComponent(port) +
                                     '&command=' + encodeURIComponent(command);
                        
                        xhr.open('POST', '/run_command', true);
                        xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
                        xhr.onreadystatechange = function() {
                            if (xhr.readyState == 4 && xhr.status == 200) {
                                document.getElementById('output').innerText = xhr.responseText;
                            }
                        };
                        xhr.send(params);
                    }
                </script>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    .section { margin-bottom: 20px; }
                    .button-group button { margin-right: 10px; margin-bottom: 5px; }
                </style>
            </head>
            <body>
                <h1>Enter SSH Details and Command</h1>

                <!-- Predefined SSH Configurations -->
                <div class="section">
                    <h2>Predefined SSH Configurations</h2>
                    <div class="button-group">
                        <button type="button" onclick="selectSSHConfig('config1')">Config 1</button>
                        <button type="button" onclick="selectSSHConfig('config2')">Config 2</button>
                        <button type="button" onclick="selectSSHConfig('config3')">Config 3</button>
                        <button type="button" onclick="selectSSHConfig('config4')">Config 4</button>
                        <button type="button" onclick="selectSSHConfig('config5')">Config 5</button>
                        <button type="button" onclick="selectSSHConfig('config6')">Config 6</button>
                        <button type="button" onclick="selectSSHConfig('config7')">Config 7</button>
                        <button type="button" onclick="selectSSHConfig('config8')">Config 8</button>
                    </div>
                </div>

                <!-- Predefined Saved Commands -->
                <div class="section">
                    <h2>Saved Commands</h2>
                    <div class="button-group">
                        <button type="button" onclick="selectSavedCommand('cmd1')">Command 1</button>
                        <button type="button" onclick="selectSavedCommand('cmd2')">Command 2</button>
                        <button type="button" onclick="selectSavedCommand('cmd3')">Command 3</button>
                        <button type="button" onclick="selectSavedCommand('cmd4')">Command 4</button>
                        <button type="button" onclick="selectSavedCommand('cmd5')">Command 5</button>
                        <button type="button" onclick="selectSavedCommand('cmd6')">Command 6</button>
                        <button type="button" onclick="selectSavedCommand('cmd7')">Command 7</button>
                        <button type="button" onclick="selectSavedCommand('cmd8')">Command 8</button>
                    </div>
                </div>

                <!-- SSH Details and Command Form -->
                <form onsubmit="event.preventDefault(); sendCommand();">
                    <label><strong>User:</strong></label>
                    <input type="text" id="user" required><br><br>

                    <label><strong>Host:</strong></label>
                    <input type="text" id="host" required><br><br>

                    <label><strong>Password:</strong></label>
                    <input type="password" id="password" required><br><br>

                    <label><strong>Port:</strong></label>
                    <input type="text" id="port" required><br><br>

                    <label><strong>Command:</strong></label>
                    <input type="text" id="command" value="top -b -n 1 | grep 'load average'" required><br><br>

                    <button type="submit">Run Command</button>
                </form>

                <h2>Command Output</h2>
                <pre id="output">Output will be shown here</pre>
            </body>
            </html>
            """

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))

    def do_POST(self):
        if self.path == '/run_command':
            try:
                # Parse POST data using cgi in Python 3.2
                content_type, pdict = cgi.parse_header(self.headers.get('Content-Type'))
                if content_type == 'application/x-www-form-urlencoded':
                    content_length = int(self.headers.get('Content-Length'))
                    post_data = self.rfile.read(content_length)
                    post_vars = cgi.parse_qs(post_data, keep_blank_values=1)

                    # Extract the parameters (decode for Python 3.2)
                    user = post_vars.get(b'user', [b''])[0].decode('utf-8')
                    host = post_vars.get(b'host', [b''])[0].decode('utf-8')
                    password = post_vars.get(b'password', [b''])[0].decode('utf-8')
                    port = post_vars.get(b'port', [b''])[0].decode('utf-8')
                    command = post_vars.get(b'command', [b''])[0].decode('utf-8')

                    # Debugging: Print received parameters
                    print("Received Parameters:")
                    print("User:", user)
                    print("Host:", host)
                    print("Password:", password)
                    print("Port:", port)
                    print("Command:", command)

                    # Build the SSH command
                    ssh_command = [
                        'sshpass', '-p', password,
                        'ssh', '-o', 'StrictHostKeyChecking=no',
                        '-p', port,
                        '%s@%s' % (user, host),
                        command
                    ]

                    # Debugging: Print the SSH command
                    print("Executing SSH Command:", ' '.join(ssh_command))

                    # Run the SSH command and capture the output
                    try:
                        output = subprocess.check_output(ssh_command, stderr=subprocess.STDOUT)
                        output = output.decode('utf-8')
                    except subprocess.CalledProcessError as e:
                        output = "Error running command:\n" + e.output.decode('utf-8')

                else:
                    output = "Unsupported Content-Type: " + content_type

            except Exception as e:
                output = "Error processing request: " + str(e)
                print("Exception during POST handling:", e)

            # Send the output back to the client
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(output.encode('utf-8'))
            return

# Set up the server for Python 3.2
try:
    httpd = socketserver.TCPServer(("", PORT), MyHandler)
    print("Serving on port", PORT)
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\nShutting down server")
    httpd.server_close()
except Exception as e:
    print("Server error:", e)
