from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Provide the path to chromedriver.exe
chrome_service = Service('C:\\Users\\jyesh\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe')

# Initialize the Chrome WebDriver using the Service object
driver = webdriver.Chrome(service=chrome_service)

# Now you can navigate to your desired URL
driver.get("https://www.menulog.com.au/restaurants-burger-urge-salisbury/menu")

# Locate all sections by their common data-test-id attribute
sections = driver.find_elements(By.CSS_SELECTOR, '[data-test-id="menu-category-item"]')

# Loop through each section
for section_index, section in enumerate(sections):
    # Extract the section title (optional)
    section_title_element = section.find_element(By.CSS_SELECTOR, '[data-test-id="menu-category-heading"]')
    section_title = section_title_element.text.strip() if section_title_element else f"Section {section_index + 1}"
    
    print(f"Section: {section_title}")
    print("=" * 50)
    
    # Find all menu items within this section
    menu_items = section.find_elements(By.CSS_SELECTOR, '[data-test-id="menu-item"]')

    # Loop through each menu item and extract the relevant data
    for item_index, item in enumerate(menu_items):
        name = item.find_element(By.CSS_SELECTOR, '[data-test-id="menu-item-name"]').text.strip()
        description_elements = item.find_elements(By.CSS_SELECTOR, '[data-test-id="menu-item-description"]')
        description = ' '.join([desc.text.strip() for desc in description_elements])

        # Scroll the item into view to trigger lazy loading
        ActionChains(driver).move_to_element(item).perform()

        # Extract the image URL
        img_elements = item.find_elements(By.CSS_SELECTOR, 'div.c-menuItems-imageContainer img')
        if img_elements:
            img_element = img_elements[0]
            # Wait for the image to have a non-empty src attribute
            WebDriverWait(driver, 10).until(
                lambda d: img_element.get_attribute('src') and 'data:' not in img_element.get_attribute('src')
            )
            img_url = img_element.get_attribute('src')
        else:
            img_url = 'No Image Available'

        price = item.find_element(By.CSS_SELECTOR, 'p.c-menuItems-price').text.strip()

        print(f"  Item {item_index + 1}:")
        print(f"    Name: {name}")
        print(f"    Image URL: {img_url}")
        print(f"    Description: {description}")
        print(f"    Price: {price}")
        
        print("-" * 50)
    
    print("\n")

# Close the browser after the task is complete
driver.quit()
