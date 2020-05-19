@auth.requires_membership('Admin') #setting view for adding editing examiners
def index():
    examiners = db(db.Examiners).select()
    managers = db(db.Managers).select()
    return locals()

    
@auth.requires_membership('Admin')
def add_examiner():#modal from student page to add students
    password = 'newPassword1234'
    password_crypt = CRYPT()(password.encode('utf8'))[0]
    new_authTableid = db.auth_user.insert(  first_name=request.vars.first_name, 
                                            last_name=request.vars.last_name, 
                                            username=request.vars.officeID,
                                            email=request.vars.email, 
                                            password=password_crypt)
    db.commit()
    new_ExTableid = db.Examiners.insert(    Ex_Fname=request.vars.first_name, 
                                            Ex_Lname=request.vars.last_name,
                                            Ex_officeID=request.vars.officeID,
                                            Ex_Appid= new_authTableid,
                                            Designation=request.vars.desig,
                                            Email=request.vars.email, 
                                            Contact=request.vars.contactNo)
    db.commit()
    db.activity_log.insert(Title_entry=request.vars.first_name, referance_id=new_ExTableid,remarks="adding new examiner to system")
    db.commit()
    db.auth_membership.insert(user_id=new_authTableid, group_id=2)
    db.commit()
    redirect(URL('settings','index'))
    return locals()

@auth.requires_membership('Admin')
def add_manager():#modal from student page to add students
    password = 'newPassword1234'
    password_crypt = CRYPT()(password.encode('utf8'))[0]
    new_authTableid = db.auth_user.insert(  first_name=request.vars.first_name, 
                                            last_name=request.vars.last_name,  
                                            username=request.vars.officeID,
                                            email=request.vars.email, 
                                            password=password_crypt)
    db.commit()
    new_ExTableid = db.Managers.insert(    Mg_Fname=request.vars.first_name, 
                                            Mg_Lname=request.vars.last_name,
                                            Mg_officeID=request.vars.officeID,
                                            Mg_Appid= new_authTableid,
                                            Designation=request.vars.desig,
                                            Email=request.vars.email, 
                                            Contact=request.vars.contactNo)
    db.commit()
    db.activity_log.insert(Title_entry=request.vars.first_name, referance_id=new_ExTableid,remarks="adding new examiner to system")
    db.commit()
    db.auth_membership.insert(user_id=new_authTableid, group_id=5)
    db.commit()
    redirect(URL('settings','index'))
    return locals()

@auth.requires_membership('Admin') #fuction to block access to examiners
def Exam_blocked_login():
    db(db.auth_user.id == request.vars.block_id).update(registration_key=request.vars.block_status)
    db.commit()
    if request.vars.block_status == "blocked":
        status = "blocked"
    elif request.vars.block_status == "":
        status = "Unblocked"
    db.activity_log.insert( Title_entry="Blocked Examiner Login", 
                            referance_id=auth.user.id ,
                            remarks="{} Login to {}".format(status, request.vars.block_id))
    db.commit()
    return locals()
    
@auth.requires_membership('Admin') #fuction to block access to examiners
def Manag_blocked_login():
    db(db.auth_user.id == request.vars.block_id).update(registration_key=request.vars.block_status)
    db.commit()
    if request.vars.block_status == "blocked":
        status = "blocked"
    elif request.vars.block_status == "":
        status = "Unblocked"
    db.activity_log.insert( Title_entry="Blocked Admin Login", 
                            referance_id=auth.user.id ,
                            remarks="{} Login to {}".format(status, request.vars.block_id))
    db.commit()
    return locals()
