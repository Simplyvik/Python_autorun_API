from robocorp.tasks import task
import json
from robocorp import browser, workitems
import requests
import os

item = None


@task
def producer_store_object_for_response():
    # Get input data from wi or file
    if os.getenv("CONTROL_ROOM"):
        item = workitems.inputs.current
        json_string_data = item.payload

    else:
        with open("task_process.json", encoding="utf-8") as file:
            json_string_data = json.load(file)
    # Get data from json payload
    href_response, file_name = process_json(json_string_data)
    # Store the result from tasklist in file or wi file
    store_response_in_work_item_or_file(href_response, item, file_name)


def process_json(json_string):
    data = json_string

    proc_id = data["Proc_id"]
    proc_name = data["Proc_name"]
    Proc_description = data["Proc_description"]

    page = browser.page()
    for task in data["Tasklist"]:
        task_id = task["Task_ID"]
        title = task["Title"]
        command = task["Command"]
        delay_start = task["Delay_start"]
        on_true = task["On_true"]
        on_false = task["On_false"]
        parameters = task["Parameters"]
        if command == "GoToPage":
            print("Open page " + parameters["Url"])
            browser.goto(url=parameters["Url"])
        elif command == "ClickOnSelector":
            print("click selector " + parameters["Selector"])
            selector_text = parameters["Selector"]
            page.click(f'text="{selector_text}"')
        elif command == "FindSelector":
            print("Find selector")
            find_text = parameters["Key_input"]
            element = page.query_selector(f'text="{find_text}"')
            href = element.get_attribute("href")
            href = "https://www.travsport.se" + href
        elif command == "SaveLinkAs":
            print("SaveLinkAs")
            file_name = find_text + ".pdf"
            href_response = requests.get(href)

        print("Last task")
    return href_response, file_name


def store_response_in_work_item_or_file(href_response, item, file_name):
    with open(f"{file_name}", "wb") as f:
        f.write(href_response.content)
    if os.getenv("CONTROL_ROOM"):
        # workitem = workitems.inputs.current
        # Attach a file to the work item
        item.add_file(file_name)
        # Save the work item
        item.save()
        item.done()
