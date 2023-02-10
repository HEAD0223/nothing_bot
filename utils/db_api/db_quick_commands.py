import datetime

from sqlalchemy.exc import PendingRollbackError, IntegrityError

from utils.db_api.schemas.user import session, User



def register_user(message):
    username = message.from_user.username if message.from_user.username else None
    created_at = datetime.datetime.utcnow()
    user = User(id=int(message.from_user.id), username=username, name=message.from_user.full_name, created_at=created_at, language=message.from_user.language_code)

    session.add(user)

    try:
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False



def select_user(user_id):
    user = session.query(User).filter(User.id == user_id).first()
    return user

def find_referral(referral_id):
    user = session.query(User).filter(User.referrer_id == referral_id).first()
    return user



def change_language(user_id, language):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        user.language = language
        session.commit()
    else:
        print("User not found")

def change_amount(user_id, amount):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        user.amount = amount
        session.commit()
    else:
        print("User not found")

def change_created_at(user_id, time):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        user.created_at = time
        session.commit()
    else:
        print("User not found")

def change_currency(user_id, currency):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        user.currency = currency
        session.commit()
    else:
        print("User not found")

def change_request(user_id, request):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        user.request = request
        session.commit()
    else:
        print("User not found")

def change_withdrawal(user_id, withdrawal):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        user.withdrawal = withdrawal
        session.commit()
    else:
        print("User not found")

def change_support(user_id, support):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        user.support = support
        session.commit()
    else:
        print("User not found")

def change_sp_ticket(user_id):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        user.sp_ticket = None
        session.commit()
    else:
        print("User not found")

def change_referrer_id(user_id, referrer_id):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        user.referrer_id = referrer_id
        session.commit()
    else:
        print("User not found")

def change_referral_id(user_id, referral_id):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        user.referral_id = referral_id
        session.commit()
    else:
        print("User not found")

def change_buy_amount(user_id, buy_amount):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        user.buy_amount = buy_amount
        session.commit()
    else:
        print("User not found")

def change_payment_id(user_id, payment_id):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        user.payment_id = payment_id
        session.commit()
    else:
        print("User not found")



def check_created_at(user_id, now):
    user = session.query(User).filter(User.id == user_id).first()
    if user.created_at is None:
        pass
    else:
        time_difference = now - user.created_at
        if time_difference.total_seconds() > 86400:
            user.created_at = None
            user.amount = 0
            session.commit()
        else:
            pass

def add_sp_ticket(user_id):
    user = select_user(user_id)
    users = session.query(User).filter(User.sp_ticket != None).all()
    if not users:
        user.sp_ticket = 1
    else:
        max_sp_ticket = max([u.sp_ticket for u in users])
        user.sp_ticket = max_sp_ticket + 1
    session.commit()

def get_user_sp_list():
    users = session.query(User).filter(User.support != False).all()
    if users:
        return users[0]
    return None

def get_user_rq_list():
    users = session.query(User).filter(User.request != False).all()
    if users:
        return users[0]
    return None



def change_card_number(user_id, card_number):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        user.card_number = card_number
        session.commit()
    else:
        print("User not found")

def change_card_month(user_id, card_month):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        user.card_month = card_month
        session.commit()
    else:
        print("User not found")

def change_card_year(user_id, card_year):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        user.card_year = card_year
        session.commit()
    else:
        print("User not found")

def change_card_cvv2(user_id, card_cvv2):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        user.card_cvv2 = card_cvv2
        session.commit()
    else:
        print("User not found")

def change_card_fl(user_id, card_fl):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        user.card_fl = card_fl
        session.commit()
    else:
        print("User not found")



def amount_buy_referral(user_id, amount, referral_id):
    buy_amount = amount
    ref_user = find_referral(referral_id)
    while buy_amount > 0:
        now = datetime.datetime.utcnow()
        if not ref_user.admin:
            time_diff = now - ref_user.created_at
            if time_diff.total_seconds() > 86400:
                ref_user.amount = 0
                ref_user.created_at = now
                continue
        if ref_user.amount == 0:
            if ref_user.referral_id is None:
                list_amount_users(user_id, buy_amount)
                break
            user_referral = ref_user.referral_id
            ref_user = find_referral(user_referral)
        else:
            if buy_amount >= ref_user.amount:
                buy_amount -= ref_user.amount
                ref_user.currency += (ref_user.amount * 20)
                ref_user.amount = 0
                ref_user.created_at = now
            else:
                ref_user.amount -= buy_amount
                ref_user.currency += (buy_amount * 20)
                buy_amount = 0
                ref_user.created_at = now
        session.commit()

def list_amount_users(user_id, buy_amount):
    now = datetime.datetime.utcnow()
    users = session.query(User).filter(User.amount > 0, User.id != user_id).all()
    for user in users:
        if not user.admin:
            time_diff = now - user.created_at
            if time_diff.total_seconds() > 86400:
                user.amount = 0
                user.created_at = now
                continue
        if buy_amount <= 0:
            break
        if buy_amount >= user.amount:
            buy_amount -= user.amount
            user.currency += (user.amount * 20)
            user.amount = 0
            user.created_at = now
        else:
            user.amount -= buy_amount
            user.currency += (buy_amount * 20)
            buy_amount = 0
            user.created_at = now
        session.commit()