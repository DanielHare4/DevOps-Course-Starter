import os
import pytest
from time import sleep
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv
from todo_app import app
from todo_app.data.trello_items import TrelloItems

@pytest.fixture(scope='module')
def app_with_temp_board():
    # Load our real environment variables
    load_dotenv(override=True)
    
    # Create the new board & update the board id environment variable
    board_id = TrelloItems().create_test_board()
    todo, done = TrelloItems().get_todo_and_done_lists(board_id)
    os.environ['TRELLO_BOARD_ID'] = board_id
    os.environ['TRELLO_LIST_ID_TODO'] = todo
    os.environ['TRELLO_LIST_ID_DONE'] = done

    # Construct the new application
    application = app.create_app()

    # Start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    # Give the app a moment to start
    sleep(1)

    yield application

    # Tear Down
    thread.join(1)
    TrelloItems().delete_test_board(board_id)

@pytest.fixture(scope="module")
def driver():
    with webdriver.Chrome() as driver:
        yield driver

def test_task_journey(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')

    assert driver.title == 'To-Do App'

    # Go to add item page
    driver.find_element(By.XPATH, '/html/body/div/a/button').click()
    title = driver.find_element(By.XPATH, '/html/body/div/div[1]/h1').text
    assert title == 'Add Item'

    # Add an item
    search_bar = driver.find_element(By.XPATH, '/html/body/div/div[2]/div/ul/form/p[1]/input')
    search_bar.send_keys('Test New Item')
    driver.find_element(By.XPATH, '/html/body/div/div[2]/div/ul/form/p[2]/button').click()
    title = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[1]/ul/table/tbody/tr[2]/td[2]').text
    assert title == 'Test New Item'

    # Change to done
    driver.find_element(By.XPATH, '/html/body/div/div[2]/div[1]/ul/table/tbody/tr[2]/td[3]/form/button').click()
    title = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/ul/table/tbody/tr[2]/td[2]').text
    assert title == 'Test New Item'

    # Delete item
    driver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/ul/table/tbody/tr[2]/td[4]/a/button').click()
    try:
        title = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/ul/table/tbody/tr[2]/td[2]')
        assert False
    except NoSuchElementException:
        assert True
