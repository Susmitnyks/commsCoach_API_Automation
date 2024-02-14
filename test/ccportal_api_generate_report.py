import subprocess

def test_generate_allure_report():
    allure_results_directory = "C:\\Users\\SusmitSurwade\\PycharmProjects\\commsCoach_API_Automation\\test\\allure_results"

    # Run the allure serve command
    subprocess.run(["allure", "serve", allure_results_directory])
