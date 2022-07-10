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
    accountName = StringField("To", validators=[InputRequired()], render_kw={"placeholder":"Account Name"})
    amount = StringField("Amount", validators=[InputRequired()], render_kw={"placeholder":"wei"})
    deposit = SubmitField("deposit")

class withdrawForm(FlaskForm):
    accountName = StringField("To", validators=[InputRequired()], render_kw={"placeholder":"Account Name"})
    amount = StringField("Amount", validators=[InputRequired()], render_kw={"placeholder":"wei"})
    withdraw = SubmitField("withdraw")

class transferForm(FlaskForm):
    fromName = StringField("From", validators=[InputRequired()], render_kw={"placeholder":"Account Name"})
    toName = StringField("To", validators=[InputRequired()], render_kw={"placeholder":"Account Name"})
    amount = StringField("Amount", validators=[InputRequired()], render_kw={"placeholder":"wei"})
    transfer = SubmitField("transfer")

class multiTransferForm(FlaskForm):
    fromName = StringField("From", validators=[InputRequired()], render_kw={"placeholder":"Account Name"})
    toAcc1 = StringField("To", render_kw={"placeholder":"Recipient"})
    toAcc2 = StringField("To", render_kw={"placeholder":"Recipient"})
    toAcc3 = StringField("To", render_kw={"placeholder":"Recipient"})
    toAcc4 = StringField("To", render_kw={"placeholder":"Recipient"})
    toAcc5 = StringField("To", render_kw={"placeholder":"Recipient"})
    amount = StringField("Amount", validators=[InputRequired()], render_kw={"placeholder":"wei"})
    mulTransfer = SubmitField("transfer")

class optionButtons(FlaskForm):
    deposit = SubmitField("Deposit")
    withdraw = SubmitField("Withdraw")
    transfer = SubmitField("Transfer")
    multiTransfer = SubmitField("Multi Transfer")
