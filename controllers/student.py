@auth.requires(auth.has_membership('Management') or auth.has_membership('Admin'))
def index(): #student page student view and variables
    students = db(db.Student).select()
    locations = db(db.C_Location).select()
    courses = db(db.Course).select()
    specializations = db(db.Specialization).select()
    return locals()


@auth.requires(auth.has_membership('Management') or auth.has_membership('Admin'))
def validate_id():
    id_student = request.vars.student_id
    search_value = db(db.Student.Student_colgID == id_student).select()
    if search_value:
        status = True
    else:
        status = False
    return response.json({'status':status})


@auth.requires(auth.has_membership('Management') or auth.has_membership('Admin'))
def add_student():#modal from student page to add students
    password = 'newPassword1234'
    password_crypt = CRYPT()(password.encode('utf8'))[0]
    new_authTableid = db.auth_user.insert(  first_name=request.vars.first_name,
                                            last_name=request.vars.last_name,
                                            username=request.vars.colg_id,
                                            email=request.vars.email, 
                                            password=password_crypt)
    db.commit()
    if new_authTableid.id:
        new_studTableid =db.Student.insert( F_Name=request.vars.first_name,
                                            L_Name=request.vars.last_name,
                                            Student_appID= new_authTableid.id,
                                            Student_colgID=request.vars.colg_id,
                                            DoJ=request.vars.doj, 
                                            Email=request.vars.email, 
                                            Email2=request.vars.email2, 
                                            Contact=request.vars.contactNo, 
                                            Contact2=request.vars.contactNo2, 
                                            DoR=request.vars.dor, 
                                            Batch=None)
        db.commit()
        db.activity_log.insert( Title_entry="New Student", 
                                referance_id=auth.user.id,
                                remarks="New Student Profile Created {} {}".format(request.vars.first_name,new_studTableid.id))
        db.commit()
        db.auth_membership.insert(user_id=new_authTableid.id, group_id=4)
        db.commit()
    else:
        db.activity_log.insert( Title_entry="Error adding New Student",
                                referance_id=auth.user.id,
                                remarks="New Student Profile Created {} {}".format(request.vars.first_name,new_authTableid.errors))
        db.commit()
    redirect(URL('student','index'))
    return response.json({'status':'success'})


@auth.requires(auth.has_membership('Management') or auth.has_membership('Admin'))
def edit_Fname():#modal from student page to edit students
    ret = db(db.Student.id == request.vars.studentId).validate_and_update(F_Name=request.vars.first_name)
    db.commit()
    db.activity_log.insert(Title_entry=request.vars.first_name, referance_id=request.vars.studentId,remarks="Edit Student first name account")
    db.commit()
    redirect(URL('student','index'))
    return response.json(ret)


@auth.requires(auth.has_membership('Management') or auth.has_membership('Admin'))
def edit_Lname():#modal from student page to edit students
    ret = db(db.Student.id == request.vars.studentId).validate_and_update(L_Name=request.vars.last_name)
    db.commit()
    db.activity_log.insert(Title_entry=request.vars.last_name, referance_id=request.vars.studentId,remarks="Edit Student last name account")
    db.commit()
    redirect(URL('student','index'))
    return response.json(ret)


@auth.requires(auth.has_membership('Management') or auth.has_membership('Admin'))
def edit_doj():#modal from student page to edit students
    ret = db(db.Student.id == request.vars.studentId).validate_and_update(DoJ=request.vars.doj)
    db.commit()
    db.activity_log.insert(Title_entry=request.vars.doj, referance_id=request.vars.studentId,remarks="Edit Student doj account")
    db.commit()
    redirect(URL('student','index'))
    return response.json(ret)


@auth.requires(auth.has_membership('Management') or auth.has_membership('Admin'))
def edit_email():#modal from student page to edit students
    ret = db(db.Student.id == request.vars.studentId).validate_and_update(Email=request.vars.email)
    db.commit()
    db.activity_log.insert(Title_entry=request.vars.email, referance_id=request.vars.studentId,remarks="Edit Student email account")
    db.commit()
    redirect(URL('student','index'))
    return response.json(ret)


@auth.requires(auth.has_membership('Management') or auth.has_membership('Admin'))
def edit_email2():#modal from student page to edit students
    ret = db(db.Student.id == request.vars.studentId).validate_and_update(Email2=request.vars.email2)
    db.commit()
    db.activity_log.insert(Title_entry=request.vars.email2, referance_id=request.vars.studentId,remarks="Edit Student email2 account")
    db.commit()
    redirect(URL('student','index'))
    return response.json(ret)


@auth.requires(auth.has_membership('Management') or auth.has_membership('Admin'))
def edit_contact():#modal from student page to edit students
    ret = db(db.Student.id == request.vars.studentId).validate_and_update(Contact=request.vars.contactNo)
    db.commit()
    db.activity_log.insert(Title_entry=request.vars.contactNo, referance_id=request.vars.studentId,remarks="Edit Student contactNo account")
    db.commit()
    redirect(URL('student','index'))
    return response.json(ret)


@auth.requires(auth.has_membership('Management') or auth.has_membership('Admin'))
def edit_contact2():#modal from student page to edit students
    ret = db(db.Student.id == request.vars.studentId).validate_and_update(Contact2=request.vars.contactNo2)
    db.commit()
    db.activity_log.insert(Title_entry=request.vars.contactNo2, referance_id=request.vars.studentId,remarks="Edit Student contactNo2 account")
    db.commit()
    redirect(URL('student','index'))
    return response.json(ret)


@auth.requires(auth.has_membership('Management') or auth.has_membership('Admin'))
def edit_DOR():#modal from student page to edit students
    ret = db(db.Student.id == request.vars.studentId).validate_and_update(DoR=request.vars.dor)
    db.commit()
    db.activity_log.insert(Title_entry=request.vars.dor, referance_id=request.vars.studentId,remarks="Edit Student dor account")
    db.commit()
    redirect(URL('student','index'))
    return response.json(ret)


@auth.requires(auth.has_membership('Management') or auth.has_membership('Admin'))
def edit_birthCountry():#modal from student page to edit students
    ret = db(db.Student.id == request.vars.studentId).validate_and_update(Birth_country=request.vars.birthCountry)
    db.commit()
    db.activity_log.insert(Title_entry=request.vars.birthCountry, referance_id=request.vars.studentId,remarks="Edit Student birth Country account")
    db.commit()
    redirect(URL('student','index'))
    return response.json(ret)


@auth.requires(auth.has_membership('Management') or auth.has_membership('Admin'))
def edit_birthPlace():#modal from student page to edit students
    ret = db(db.Student.id == request.vars.studentId).validate_and_update(Birth_place=request.vars.birthPlace)
    db.commit()
    db.activity_log.insert(Title_entry=request.vars.birthPlace, referance_id=request.vars.studentId,remarks="Edit Student birth Place account")
    db.commit()
    redirect(URL('student','index'))
    return response.json(ret)


@auth.requires(auth.has_membership('Management') or auth.has_membership('Admin'))
def del_student():
    ret = db(db.Student.id == request.vars.studentId).validate_and_update(is_active=False)
    db.commit()
    app_id = db(db.Student.id == request.vars.studentId).select().first()
    db(db.auth_user.id == app_id.Student_appID ).update(registration_key="blocked")
    db.commit()
    db.activity_log.insert(Title_entry="Deactivate", referance_id=request.vars.studentId,remarks="Deactivate Student")
    db.commit()
    redirect(URL('student','index'))
    return response.json(ret)
