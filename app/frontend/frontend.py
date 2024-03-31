from datetime import datetime

import pandas as pd
import requests
import streamlit as st
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu

base_url = "http://backend:4321"

usernames = []
passwords = []
stock_lists = {}
user_ids = []


def first_init():

    first_user = requests.put(base_url + "/users/new/?" + "user_email=a@a.com&password=1234")

    res = requests.get(base_url + "/stock/index/snp500/latest/")
    print(res.json())

def update_cred():
    NO_PROXY = {
        'no': 'pass',
    }
    all_users = requests.get(base_url + "/db/users/all", proxies=NO_PROXY)

    credentials = {"usernames": {}}

    usernames.clear()
    passwords.clear()
    stock_lists.clear()
    for j in all_users.json():
        usernames.append(j["email"])
        passwords.append(j["password"])
        stock_lists[j["email"]] = j["stocks"]
        user_ids.append((j["_id"]))
    names = usernames.copy()

    for un, name1, pw in zip(usernames, names, passwords):
        user_dict = {"name": name1, "password": pw}
        credentials["usernames"].update({un: user_dict})
    return credentials


def one_min_passed(time_one: datetime, time_two: datetime):
    res = time_two - time_one
    sec = res.total_seconds()
    one_min = 60
    return sec > one_min


with st.sidebar:
    selected = option_menu(
        menu_title="Stocky",
        options=["Home", "SnP500"]
    )
first_init()
if selected == "Home":
    st.title('Welcome to :violet[Stocky]📈')

    authenticator = stauth.Authenticate(credentials=update_cred(), cookie_name="stocky_yummy", cookie_key="yum-yum", cookie_expiry_days=30)

    # not logged in
    if not st.session_state["authentication_status"]:
        choice = st.radio("", key="login_choice", options=["Login", "Signup"], horizontal=True)

        if choice == "Login":

            name, authentication_status, username = authenticator.login(fields={'Form name': 'Login',
                                                                                'Username': 'Email Address 📧',
                                                                                'Password': 'Password 🤫',
                                                                                'Login': 'Profit 💰'})
        elif choice == "Signup":
            email = st.text_input("Email Address📧")
            password = st.text_input("Password🤫", type="password")
            signup_button = st.button("Profit💰")
            if signup_button:
                data = {"user_email": email, "password": password}

                r = requests.put(base_url + "/users/new/", params=data, headers={"Content-Type": "application/json"})
                if r:
                    st.popover("You have been registered!")
                    update_cred()
                    choice = "Login"

    # logged in
    if st.session_state["authentication_status"]:
        authenticator.logout()
        st.write(f'Welcome *{st.session_state["name"]}*')
        symbol = st.text_input("Enter Stock Symbol")
        if st.button("Check Latest Price"):
            res = requests.get(base_url + f"/stock/{symbol}")
            if res:
                data = res.json()
                st.markdown(f"""
                * Symbol: {data["symbol"]}
                * Price: {str(data["price"]) + "$"}
                * Market Capitalization: {str(data["market_cap"]) + "$"}
                * Timestamp: {data["timestamp"]}
                """)
            else:
                st.write("Invalid Symbol - Try NVDA 😉")

        # display my stocks
        if st.session_state["authentication_status"]:
            my_stocks = stock_lists[st.session_state["username"]]
            the_stock = st.text_input("Enter Symbol to add to my stocks")
            add_to_my_stocks_btn = st.button("Add to my Stocks")

            if add_to_my_stocks_btn:
                check_valid_stock = requests.get(base_url + "/stock/" + the_stock)
                if check_valid_stock.status_code == 200:
                    my_stocks.append(the_stock)
                    update_db_request = requests.post(base_url + "/db/stocks/add/",
                                                      params={
                                                          "unique_id": user_ids[
                                                              usernames.index(st.session_state["username"])],
                                                          "symbol": the_stock})
                else:
                    st.popover("Invalid Symbol :thumbsdown:")

            stock_to_delete = st.text_input(
                'enter a Stock To delete')
            delete_btn = st.button("DELETE")
            if delete_btn:
                delete_request = requests.delete(base_url + "/db/stock/delete?user_id=" + user_ids[
                    usernames.index(st.session_state["username"])] + "&"
                                                 + "symbol=" + stock_to_delete)

                if delete_request:
                    if stock_to_delete in my_stocks:
                        my_stocks.remove(stock_to_delete)

            company_names = []
            company_symbol = []
            prices = []

            # update_cred()
            for i in list(dict.fromkeys(my_stocks)):
                stock_request = requests.get(base_url + "/stock/" + i)
                stock_request_data = stock_request.json()
                if stock_request:
                    # company_names.append(stock_request_data["name"])
                    company_symbol.append(stock_request_data["symbol"])
                    prices.append(stock_request_data["price"])

            st.header(":rainbow[My Stocks]")
            d = {"Symbol": company_symbol, "Price": prices}
            df = pd.DataFrame(data=d)
            styled_df = df.style.format({
                "price": "${:.2f}"  # Format price as currency
            })
            st.table(styled_df)

        st.header("Latest Stories")
        latest_stories_text = st.text_input("Symbol Latest stories")
        latest_stories_btn = st.button("Let's read🕵️")

        st.subheader(latest_stories_text)
        titles = []
        descriptions = []
        if latest_stories_btn:
            stories_req = requests.get(base_url + "/stock/news/" + latest_stories_text)
            stories_req_data = stories_req.json()
            if stories_req:

                if not stories_req_data["stories"]:
                    st.subheader("No News - Check Symbol:point_up_2:")
                else:
                    for story in stories_req_data["stories"]:

                        titles.append(story["title"])
                        try:
                            descriptions.append(story["description"])
                        except KeyError:
                            descriptions.append("NA")

                    d = {"Title": titles, "description": descriptions}
                    df = pd.DataFrame(data=d)
                    st.table(df)



    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')

if selected == "SnP500":
    st.title('Welcome to :red[S&P500- Top 10]💎🙌')

    full_url = base_url + f"/stock/index/snp500/latest/"
    res = requests.get(full_url)
    now = datetime.now()
    if res:
        data = res.json()
        now = datetime.now()

        company_names = []
        company_symbol = []
        prices = []
        for i in data["table"]:
            company_names.append(i["name"])
            company_symbol.append(i["symbol"])
            prices.append(i["price"])
        d = {"Company Name": company_names, "Symbol": company_symbol, "Price": prices}
        df = pd.DataFrame(data=d)
        styled_df = df.style.format({
            "price": "${:.2f}"  # Format price as currency
        })
        st.table(styled_df)
        st.write(data["time"])
    else:
        st.write(res)
