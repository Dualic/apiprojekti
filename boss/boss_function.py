def boss_wants_to_know(func_data):
    import json
    import requests

    request_json = func_data.get_json(silent=True)
    print("func_data on", func_data)
    print("request_json on", request_json)

    messages = request_json["input"]
    print("Messages on", messages)
    
    eka_message = messages[0]
    print("eka_message on", eka_message)
    ekan_message = eka_message["message"]
    print("eka_message['message'] on", ekan_message)

    aika = ekan_message["publishTime"]
    print("aika on", aika)

    publish_time = []

    for sisus in messages:
        publish_time.append(sisus["message"]["publishTime"])

    print("ajat", publish_time) 
    #muutetaan lista stringiksi, että kelpaa workflowlle palautettavaksi (mm. string ja dict kelpaisivat)
    list_to_string = " "
    string_times = list_to_string.join(publish_time)
        
    return string_times