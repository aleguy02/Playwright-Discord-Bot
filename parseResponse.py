import json

def parse_response(response):
    start_index = response.find("{")
    end_index = response.rfind("}") + 1
    response = json.loads(response[start_index:end_index])  # fix this at some point, sometimes it gets the endindex wrong
    summary = response["summary"]
    terms_as_string = ""
    i = 1
    for item in response["key_terms"]:
        terms_as_string += (f"{i}. {item["term"]}: {item["explanation"]}\n")
        i += 1
    
    return summary, terms_as_string