*** Settings ***
Documentation    This suite to verify elements and do actions on Checkout page
Resource    ../keywords/checkout_page.robot

Test Setup    [Checkout Page] Go to Checkout page

Test Teardown    run keywords
    ...     Delete all cookies
    ...     Reload page

Suite Teardown    Close all browsers
*** Test Cases ***
CP07 - Check overview Checkout page
    [Tags]    high
    [Checkout Page] Verify elements displaying on page
