from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired

def buildButton(label):
    class Btn(FlaskForm):
        btn = SubmitField(label)
    return Btn()

class createAccountForm(FlaskForm):
    username = StringField("Account Name", validators=[InputRequired()], render_kw={"placeholder":"username"})
    createAcc = SubmitField("Create")

class depositForm(FlaskForm):
    accountName = StringField("", validators=[InputRequired()], render_kw={"placeholder":"Account"})
    amount = StringField("", validators=[InputRequired()], render_kw={"placeholder":"amount"})
    deposit = SubmitField("deposit")

class withdrawForm(FlaskForm):
    accountName = StringField("", validators=[InputRequired()], render_kw={"placeholder":"recipient"})
    amount = StringField("", validators=[InputRequired()], render_kw={"placeholder":"amount"})
    withdraw = SubmitField("withdraw")

class transferForm(FlaskForm):
    fromName = StringField("", validators=[InputRequired()], render_kw={"placeholder":"Account"})
    toName = StringField("", validators=[InputRequired()], render_kw={"placeholder":"recipient"})
    amount = StringField("", validators=[InputRequired()], render_kw={"placeholder":"amount"})
    submit = SubmitField("transfer")

class multiTransferForm(FlaskForm):
    fromName = StringField("", validators=[InputRequired()], render_kw={"placeholder":"sender"})
    toAcc1 = StringField("", render_kw={"placeholder":"Recipient"})
    toAcc2 = StringField("", render_kw={"placeholder":"Recipient"})
    toAcc3 = StringField("", render_kw={"placeholder":"Recipient"})
    toAcc4 = StringField("", render_kw={"placeholder":"Recipient"})
    toAcc5 = StringField("", render_kw={"placeholder":"Recipient"})
    amount = StringField("", validators=[InputRequired()], render_kw={"placeholder":"amount"})
    submit = SubmitField("transfer")

class optionButtons(FlaskForm):
    deposit = SubmitField("Deposit")
    withdraw = SubmitField("Withdraw")
    transfer = SubmitField("Transfer")
    multiTransfer = SubmitField("Multi Transfer")
