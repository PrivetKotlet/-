from parss import sq



class chek():
    
    def chek_contact(contact):
        if len(contact) == 12 and contact[0] == "+" :
            return True
        else:
            return False

    def chek_Yk_password(password):
            password = str(password)
            if password in sq.select.get_yk_password():
                return True
            else:
                return False
    
    def chek_coffe_house_name_for_rep(id,coffe_house,mode):
        if mode == 1:
            if coffe_house == sq.select.select_coffee_house_for_chek(id):
                return False
            else:
                return True
        else:
            if coffe_house == sq.select.select_coffee_houseByID_dm(id):
                return True
            else:
                return False

        

    def chek_id(id):
        try:
            id = int(id)
            if id in sq.select.select_id():
                return True
            else:
                return False
        except ValueError as erorr:
            return False

    def chek_iddm(id):
        try:
            id = int(id)
            if id in sq.select.select_iddm():
                return True
            else:
                return False
        except ValueError as erorr:
            return False

