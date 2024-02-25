from flask import Blueprint, request

dian_methods = Blueprint("dian_methods", __name__)

@dian_methods.post("/api/v1/scrape_dian_information")
def get_information_from_dane():

    return None