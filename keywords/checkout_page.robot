*** Settings ***
Library    SeleniumLibrary
Library    BuiltIn
Library    ./../commonweb.py

*** Variables ***
${btn_login}                                //button[.='Log in']
${btn_continue_shopping_loc}                //button[.='Continue shopping']
${ip_email_address_loc}                     //input[@name='email-address']
${ip_order_number_loc}                      //input[@name='order-number']
${link_contact_loc}                         //*[.='Contact us']
${element_sidebar_checkout_loc}             (//div[@class='sidebar scoped checkout'])[2]
${element_policy_list_loc}                  (//div/ul[@class='policy-list'])[1]
${element_information_loc}                  (//div[@class='section__content'])[1]

*** Keywords ***
[Checkout Page] Go to Checkout page
    Start Chrome Browser    url=https://plusbase-auto.onshopbase.com/orders/c84801000f904b86adbd50e5fe1ff1c8
    Maximize Browser Window
    Wait Until Keyword Succeeds    60s      1s      page should contain     Log in to view all order details

[Checkout Page] Verify elements displaying on page
    page should contain     Log in to view all order details
    page should contain     You can find your order number in the receipt you received via email.
    page should contain element     ${ip_email_address_loc}
    page should contain element     ${ip_order_number_loc}
    page should contain element     ${btn_login}
    page should contain element     ${btn_continue_shopping_loc}
    page should contain element     ${element_sidebar_checkout_loc}
    page should contain element     ${element_policy_list_loc}
    page should contain element     ${element_information_loc}
    page should contain element     ${link_contact_loc}
