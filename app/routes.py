from flask import render_template, redirect, url_for, send_from_directory, request, flash
from app import app
from app.forms import (
    buildButton,
    createAccountForm,
    optionButtons,
    depositForm,
    withdrawForm,
    transferForm,
    multiTransferForm
)
import os
from brownie import *
from scripts.scripts import (
    get_account,
    balanceDAI,
    depositDAI,
    withdrawDAI,
    transferDAI,
    multiTransferDAI,
    createAccount
)
from web3 import Web3


# Using brownie as a python package
p = project.load('.')
p.load_config()
network.connect('rinkeby')

accounts = []
user_account = get_account()

#Route for storing static items
def static_dir(path):
    return send_from_directory('static', path)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    button = buildButton("Start Banking")
    title = "SCB 10X BANK"
    if button.btn.data:
        return redirect(url_for('banking'))
    return render_template("index.html", button=button, title=title)

@app.route('/banking', methods=['GET', 'POST'])
def banking():
    create = buildButton("Create Account")
    form = createAccountForm()
    
    deForm = depositForm()
    trForm = transferForm()
    wiForm = withdrawForm()
    mTForm = multiTransferForm()

    options = optionButtons()
    
    title = user_account.address

    if form.createAcc.data and form.validate_on_submit():
        
        username = form.username.data
        status = createAccount(username, user_account)
        if status:
            accounts.append(username)
            flash("Account created!")
            

    if deForm.submit.data and deForm.validate_on_submit():
        amount = deForm.amount.data
        accountName = deForm.accountName.data

        status = depositDAI(amount, accountName, user_account)
        
        if status:
            flash("Deposit Success!")
            

    if trForm.submit.data and trForm.validate_on_submit():
        amount = trForm.amount.data
        fromName = trForm.fromName.data
        toName = trForm.toName.data

        status = transferDAI(amount, fromName, toName, user_account)
        if status:
            flash("Transfer Success!")
            

    if wiForm.submit.data and wiForm.validate_on_submit():
        
        amount = wiForm.amount.data
        accountName = wiForm.accountName.data

        status = withdrawDAI(amount, accountName, user_account)
        if status:
            flash("Withdraw Success!")
            

    if mTForm.submit.data and mTForm.validate_on_submit():
        amount = mTForm.amount.data
        fromName = mTForm.fromName.data

        to_name_arr = [
            mTForm.toAcc1.data,
            mTForm.toAcc2.data,
            mTForm.toAcc3.data,
            mTForm.toAcc4.data,
            mTForm.toAcc5.data,
        ]

        to_name_arr = [account for account in to_name_arr if account == "" ]

        status = multiTransferDAI(amount, fromName, to_name_arr, user_account)
        if status:
            flash("Transfer Success!")
            

    return render_template(
        "banking.html", 
        create=create, 
        form=form,
        accounts=[(account, balanceDAI(account)) for account in accounts],
        title = title,
        options = options,
        deForm = deForm,
        trForm = trForm,
        wiForm = wiForm,
        mTForm = mTForm
    )

