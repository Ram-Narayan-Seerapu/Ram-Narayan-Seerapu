import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime
import matplotlib.pyplot as plt


class LogHandler:
    def __init__(self, log_file_path, snapshot_dir='snapshots'):
        self.log_file_path = log_file_path
        self.start_time = datetime.now()
        self.test_cases = []
        # Initialize logging
        self.logger = logging.getLogger('TestExecutionLogger')
        self.logger.setLevel(logging.DEBUG)

        # Create a rotating file handler
        self.handler = RotatingFileHandler(log_file_path, maxBytes=5 * 1024 * 1024, backupCount=2)
        self.handler.setLevel(logging.DEBUG)

        # Create a logging format
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(self.formatter)

        # Add the handler to the logger
        self.logger.addHandler(self.handler)

        # Create a directory for error snapshots if it doesn't exist
        if not os.path.exists(snapshot_dir):
            os.makedirs(snapshot_dir)
        self.snapshot_dir = snapshot_dir

        # Store the current time as the log generation time
        self.log_generation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Create or overwrite the log file
        with open(self.log_file_path, 'w') as file:
            file.write(self._generate_html_header())

    def _generate_html_header(self):
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Test Execution Log</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    width: 80%;
                    margin: auto;
                    overflow: hidden;
                }}
                header {{
                    background: #333;
                    color: #fff;
                    padding: 20px 0;
                    text-align: center;
                    border-bottom: #0779e4 3px solid;
                    position: relative;
                }}
                .log-time {{
                    position: absolute;
                    top: 20px;
                    right: 20px;
                    text-align: right;
                }}
                .log {{
                    background: #fff;
                    padding: 20px;
                    margin: 20px 0;
                    border: #ccc 1px solid;
                }}
                .log pre {{
                    white-space: pre-wrap;
                    word-wrap: break-word;
                }}
                h2, h3 {{
                    color: #2c3e50;
                    margin: 20px 0;
                    padding: 0;
                }}
                p {{
                    margin: 0;
                    padding: 0 0 10px 0;
                    font-size: 1rem;
                    color: #555;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                }}
                th, td {{
                    padding: 12px;
                    text-align: left;
                }}
                tr:nth-child(even) {{
                    background-color: #f9f9f9;
                }}
                tr:hover {{
                    background-color: #f1f1f1;
                }}
                .pass {{
                    color: green;
                    font-weight: bold;
                }}
                .failed {{
                    color: red;
                    font-weight: bold;
                }}
                .skip {{
                    color: grey;
                    font-weight: bold;
                }}
                .summary-table, .details-table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }}
                .summary-table th, .summary-table td, .details-table th, .details-table td {{
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: left;
                }}
                .summary-table th, .details-table th {{
                    background-color: #333;
                    color: white;
                }}
                .summary-chart {{
                    display: flex;
                    justify-content: center;
                    margin: 20px 0;
                }}
                .collapsible {{
                    background-color: white;
                    color: black;
                    cursor: pointer;
                    padding: 12px;
                    width: 100%;
                    border: 2px solid #ddd;
                    border-radius: 4px;
                    text-align: left;
                    outline: none;
                    font-size: 16px;
                    margin-top: 10px;
                    display: flex;
                    align-items: center;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .collapsible:hover, active  {{
                    background-color: #f7f7f7;
                }}
                .collapsible-content {{
                    padding: 0 18px;
                    display: none;
                    overflow: hidden;
                    background-color: #f1f1f1;
                }}
                .collapsible-sign {{
                    font-weight: bold;
                    font-size: 18px;
                    margin-right: 10px;
                    background-color: #ddd;
                    padding: 2px 8px;
                    border-radius: 4px;
                    display: inline-block;
                }}
                .collapsible-content.show {{
                    display: block;
                }}
                .content {{
                    padding: 0 20px;
                    display: none;
                    overflow: hidden;
                    background-color: #fafafa;
                    border-top: 1px solid #ddd;
                }}
            </style>
        </head>
        <body>
            <header>
                <div class="container">
                    <h1>Test Execution Log</h1>
                    <div class="log-time" id="log-time"></div>
                </div>
            </header>
            <div class="container">
                <section id="summary">
                    <div id="summary">
                    </div>
                </section>
                <section>
                    <h2>Test Case Details</h2>
                    <table class="details-table">
                    <thead>
                        <tr>
                            <th>Test Case</th>
                            <th>Project</th>
                            <th>Script Type</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                        <tbody id="test_cases">
                            <!-- Test case rows will be inserted here -->
                        </tbody>
                    </table>
                    <div><p></p></div>
                </section>
                <section>
                    <h2>Test Log Information</h2>
                    <div id="test_log_information">
                    </div>
                </section>
                
            </div>
            <script>
                function updateTime() {{
                    const logTimeElement = document.getElementById('log-time');
                    const generatedTime = new Date("{self.log_generation_time}");
                    const currentTime = new Date();
                    const elapsedTime = Math.floor((currentTime - generatedTime) / 1000); // in seconds

                    const hours = Math.floor(elapsedTime / 3600);
                    const minutes = Math.floor((elapsedTime % 3600) / 60);
                    const seconds = elapsedTime % 60;

                    logTimeElement.innerHTML = `Generated: {self.log_generation_time}<br>Elapsed: ${{hours}}h 
                    ${{minutes}}m ${{seconds}}s`;
                }}
                
                document.addEventListener('DOMContentLoaded', function() {{
                    updateTime();
                    setInterval(updateTime, 1000);

                    var coll = document.getElementsByClassName("collapsible");
                    for (var i = 0; i < coll.length; i++) {{
                        coll[i].addEventListener("click", function() {{
                            this.classList.toggle("active");
                            var content = this.nextElementSibling;
                            var sign = this.querySelector('.collapsible-sign');
                            if (content.style.display === "block") {{
                                content.style.display = "none";
                                sign.textContent = "+";
                            }} else {{
                                content.style.display = "block";
                                sign.textContent = "-";
                            }}
                        }});
                    }}
                }});
            </script>
        </body>
        </html>
        """

    @staticmethod
    def _generate_test_case_row(test_name, project, script_type):
        return f"""
        <tr id="{test_name}">
            <td>{test_name}</td>
            <td>{project}</td>
            <td>{script_type}</td>
            <td id="{test_name}_status" class="skip">Skip</td>
        </tr>
        """

    def add_test_case(self, test_name, project, script_type):
        self.test_cases.append({
            'name': test_name,
            'project': project,
            'script_type': script_type,
            'steps': [],
            'status': 'Skip'
        })
        with open(self.log_file_path, 'r+') as file:
            content = file.read()
            index = content.index('</tbody>')
            content = content[:index] + self._generate_test_case_row(test_name, project, script_type) + content[index:]
            file.seek(0)
            file.write(content)
            file.truncate()

    def add_test_step(self, test_name, step_number, action, detail, status, *args):
        for test_case in self.test_cases:
            if test_case['name'] == test_name:
                if args:
                    test_case['steps'].append({
                        'test_case': test_name,
                        'step_number': step_number,
                        'action': action,
                        'detail': detail,
                        'status': status,
                        'snapshot': args
                    })
                else:
                    test_case['steps'].append({
                        'test_case': test_name,
                        'step_number': step_number,
                        'action': action,
                        'detail': detail,
                        'status': status
                    })
                break

    def update_test_case_status(self, test_name, status):
        for test_case in self.test_cases:
            if test_case['name'] == test_name:
                test_case['status'] = status
                break
        with open(self.log_file_path, 'r+') as file:
            content = file.read()
            content = content.replace(f'id="{test_name}_status" class="skip">Skip',
                                      f'id="{test_name}_status" class="{status.lower()}">{status}')
            file.seek(0)
            file.write(content)
            file.truncate()

    def generate_summary(self):
        total_tests = len(self.test_cases)
        passed_tests = sum(1 for tc in self.test_cases if tc['status'].lower() == 'pass')
        failed_tests = sum(1 for tc in self.test_cases if tc['status'].lower() == 'failed')
        not_run_tests = total_tests - (passed_tests + failed_tests)

        # Generate bar chart
        labels = ['Passed', 'Failed', 'Skip']
        values = [passed_tests, failed_tests, not_run_tests]
        colors = ['green', 'red', 'gray']

        plt.bar(labels, values, color=colors)
        plt.xlabel('Test Status')
        plt.ylabel('Number of Tests')
        plt.title('Test Summary')
        plt.savefig('test_summary.png')
        plt.close()

        summary_html = f"""
        <div class="container">
                <h2>Test Summary</h2>
                <img src="test_summary.png" alt="Test Summary Bar Graph">
                <table class="summary-table">
                    <thead>
                        <tr>
                            <th>Test Status</th>
                            <th>Count</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><b>Total</b></td>
                            <td>{total_tests}</td>
                        <tr>
                            <td class="passed">Passed</td>
                            <td>{passed_tests}</td>
                        </tr>
                        <tr>
                            <td class="failed">Failed</td>
                            <td>{failed_tests}</td>
                        </tr>
                        <tr>
                            <td class="skip">Skip</td>
                            <td>{not_run_tests}</td>
                        </tr>
                    </tbody>
                </table>
        """

        with open(self.log_file_path, 'r+') as file:
            content = file.read()
            content = content.replace('<div id="summary">', f'<div id="summary">{summary_html}')
            file.seek(0)
            file.write(content)
            file.truncate()

    def log_execution_start(self, test_name):
        pass

    def log_action_result(self, test_name, step_number, action, detail, status, *args):
        self.add_test_step(test_name, step_number, action, detail, status, *args)

    def log_execution_end(self, test_name, status):
        self.update_test_case_status(test_name, status)

        with open(self.log_file_path, 'r+') as file:
            content = file.read()
            log_details_content = ""
            for tc in self.test_cases:
                if tc['name'] == test_name:
                    passed_actions = sum(1 for action in tc['steps'] if action['status'].lower() == 'pass')
                    failed_actions = sum(1 for action in tc['steps'] if action['status'].lower() == 'failed')
                    not_run_actions = sum(1 for action in tc['steps'] if action['status'].lower() == 'Skip')

                    tc_status_color = '#4CAF50' if tc['status'].lower() == 'pass' else '#f44336'
                    log_details_content += (f"<button type='button' class='collapsible'><span class='collapsible-sign'>"
                                            f"+</span> <span class='collapsible-text' style='background-color: "
                                            f"{tc_status_color}; color: white;'>{tc['name']}</span></button>")
                    log_details_content += (f"<div class='collapsible-content'><p>Summary: <b>Total:"
                                            f"</b> {passed_actions + failed_actions + not_run_actions},  "
                                            f"<b style='color:green;'>Passed:</b> {passed_actions}, "
                                            f"<b style='color:red;'>Failed:</b> {failed_actions}, "
                                            f"<b style='color:grey;'>Skip:</b> {not_run_actions}</p>")

                    for step in tc['steps']:
                        action_status_color = '#4CAF50' if step['status'].lower() == 'pass' else '#f44336'
                        log_details_content += (f"<button type='button' class='collapsible'>"
                                                f"<span class='collapsible-sign'>+</span> "
                                                f"<span style='background-color: {action_status_color}; "
                                                f"color: white;'>{step['action']}</span></button>")
                        log_details_content += "<div class='collapsible-content'>"
                        log_details_content += (f"<p>Status: <span class='status-{step['status'].lower()}'>"
                                                f"{step['status']}</span></p>")
                        log_details_content += f"<p>Details: {step['detail']}</p>"
                        if 'snapshot' in step:
                            snaps = step['snapshot']
                            for snap in snaps:
                                log_details_content += f"<img src='{snap}'>"
                        log_details_content += "</div>"

                    log_details_content += "</div>"
            content = content.replace('<div id="test_log_information">',
                                      f'<div id="test_log_information">{log_details_content}')
            file.seek(0)
            file.write(content)
            file.truncate()


if __name__ == "__main__":
    log_handler = LogHandler('log.html')

    # Simulating test case execution
    log_handler.add_test_case('MainMenuTesting', 'ABC', 'Screen Comparison')
    log_handler.add_test_case('MainMenuPlusTesting', 'ABC', 'Screen Comparison')
    log_handler.add_test_case('GuardedAccess', 'ABC', 'Text Comparison')
    log_handler.add_test_case('Prog_features', 'ABC', 'Text Comparison')
    log_handler.add_test_case('Alarm_features', 'ABC', 'Screen Comparison')
    log_handler.add_test_case('DEET', 'XYZ', 'Screen Comparison')
    log_handler.add_test_case('DEE', 'XYZ', 'Screen Comparison')

    log_handler.log_execution_start('MainMenuTesting')
    log_handler.log_action_result('MainMenuTesting', '1', 'Press Key', 'CENTER_KEY',
                                  'Pass')
    log_handler.log_action_result('MainMenuTesting', '2', 'Compare Image',
                                  'path/to/image', 'Failed', 'snapshots/error1.png')
    log_handler.log_execution_end('MainMenuTesting', 'Failed')

    log_handler.log_execution_start('GuardedAccess')
    log_handler.log_action_result('GuardedAccess', '1', 'Press Key', 'CENTER_KEY',
                                  'Pass')
    log_handler.log_action_result('GuardedAccess', '2', 'Compare Image',
                                  'path/to/image', 'Pass')
    log_handler.log_execution_end('GuardedAccess', 'Pass')

    log_handler.log_execution_start('Prog_features')
    log_handler.log_action_result('Prog_features', '1', 'Press Key', 'CENTER_KEY',
                                  'Pass')
    log_handler.log_action_result('Prog_features', '2', 'Compare Image',
                                  'path/to/image', 'Skip', 'snapshots/error.png')
    log_handler.log_execution_end('Prog_features', 'Skip')

    log_handler.log_execution_start('Alarm_features')
    log_handler.log_action_result('Alarm_features', '1', 'Press Key', 'CENTER_KEY',
                                  'Pass')
    log_handler.log_action_result('Alarm_features', '2', 'Compare Image',
                                  'path/to/image', 'Pass')
    log_handler.log_action_result('Alarm_features', '3', 'Press Key',
                                  'RIGHT_KEY', 'Pass')
    log_handler.log_execution_end('Alarm_features', 'Pass')

    log_handler.log_execution_start('MainMenuPlusTesting')
    log_handler.log_action_result('MainMenuPlusTesting', '1', 'Press Key',
                                  'CENTER_KEY', 'Pass')
    log_handler.log_action_result('MainMenuPlusTesting', '2', 'Compare Image',
                                  'path/to/image', 'Failed', 'snapshots/error.png')
    log_handler.log_execution_end('MainMenuPlusTesting', 'Pass')

    log_handler.log_execution_start('DEET')
    log_handler.log_action_result('DEET', '1', 'Press Key', 'CENTER_KEY',
                                  'Pass')
    log_handler.log_action_result('DEET', '2', 'Compare Image', 'path/to/image',
                                  'Pass')
    log_handler.log_execution_end('DEET', 'Pass')

    log_handler.log_execution_start('DEE')
    log_handler.log_action_result('DEE', '1', 'Press Key', 'CENTER_KEY',
                                  'Pass')
    log_handler.log_action_result('DEE', '2', 'Compare Image', 'path/to/image',
                                  'Failed', 'snapshots/error1.png', 'snapshots/error1.png', 'snapshots/error1.png')
    log_handler.log_execution_end('DEE', 'Failed')

    log_handler.generate_summary()