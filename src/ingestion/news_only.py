import requests
from pygments.lexers import q

from page_configurations import custom_headers
url="https://www.davispolk.com/views/ajax?_wrapper_format=drupal_ajax&view_name=post_landing_page&view_display_id=page_3&view_args=&view_path=%2Fabout%2Fnews&view_base_path=about%2Fnews&view_dom_id=9b44c1abd7bbf13623d4c25bdc268d4b942783a74d4a08827a10827218f4aa87&pager_element=0&field_practices_target_id=All&field_industries_target_id=All&field_regions_target_id=All&keys=&field_lawyers_target_id=&field_news_category_value=All&page=0&_drupal_ajax=1&ajax_page_state%5Btheme%5D=dpw_2020&ajax_page_state%5Btheme_token%5D=&ajax_page_state%5Blibraries%5D=eJxtkVluwzAMRC8kR0EuJNDSWGVDm4ZIN3FPXyfukrb54fIwGAzIHu5oCddZDSUNLNtqsWJCIwn5jMKuLfFUMHkvms_xYQ5ZG2Jpy0xyoMU16zgLHKHMl3Q6no4xL-Y6dgZB9h9cRXuSznLj2e0_91V4qne-ozhoG5OBWn5Juym_k7NO9qj6TP5MYdB464WchFa0gCVl1TMj3XMzTRnxGUw9NYSqWgXJqca6lb_7gV7p-huOwdhx4YJEgubb7diDreYYY0-G4OustfGwxu8pvDEuFu_1MGpZBDvavjDcDJC2s6nILum-aLfTD3xDth4"
while True:
    try:
        res = requests.get(url=url, headers=custom_headers)
        res.raise_for_status()
        res_json=res_json()
    except requests.exceptions.RequestException as e:
        break


print(res.text)