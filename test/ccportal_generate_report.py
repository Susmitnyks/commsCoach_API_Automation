import os


def test_report():
    os.system("allure generate --single-file allure-results")