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
def reset_password():
    password = 'newPassword1234'
    password_crypt = CRYPT()(password.encode('utf8'))[0]
    app_id = db(db.Student.id == request.vars.studentId).select().first()
    ret = db(db.auth_user.id == app_id.Student_appID).validate_and_update(password=password_crypt)
    db.commit()
    if ret.errors:
        db.activity_log.insert(Title_entry="Failed Password Reset",
                               referance_id=auth.user.id,
                               remarks="Password reset for {} failed due to {}".format(Student_colgID, ret.errors))
        db.commit()
    else:
        db.activity_log.insert(Title_entry="Password Reset",
                               referance_id=auth.user.id,
                               remarks="Password reset to default for {} reset to {}".format(app_id.Student_colgID, password_crypt))
        db.commit()
        redirect(URL('student','index'))
        session.flash = T("Password Reset Complete for {} {}".format(app_id.F_Name, app_id.Student_colgID))
    return response.json(ret)


@auth.requires(auth.has_membership('Management') or auth.has_membership('Admin'))
def edit_Fname():#modal from student page to edit students
    ret = db(db.Student.id == request.vars.studentId).validate_and_update(F_Name=request.vars.first_name)
    db.commit()
    db.activity_log.insert(Title_entry="Edit Student first name account", 
                           referance_id=auth.user.id,
                           remarks="Edited {} first name to {}".format(request.vars.studentId, request.vars.first_name))
    db.commit()
    redirect(URL('student','index'))
    return response.json(ret)


@auth.requires(auth.has_membership('Management') or auth.has_membership('Admin'))
def edit_Lname():#modal from student page to edit students
    ret = db(db.Student.id == request.vars.studentId).validate_and_update(L_Name=request.vars.last_name)
    db.commit()
    db.activity_log.insert(Title_entry="Edit Student last name account", 
                           referance_id=auth.user.id,
                           remarks="Edit {} last name to {}".format(request.vars.studentId, request.vars.last_name))
    db.commit()
    redirect(URL('student','index'))
    return response.json(ret)


@auth.requires(auth.has_membership('Management') or auth.has_membership('Admin'))
def edit_doj():#modal from student page to edit students
    ret = db(db.Student.id == request.vars.studentId).validate_and_update(DoJ=request.vars.doj)
    db.commit()
    db.activity_log.insert(Title_entry="Edit Student DoJ", 
                           referance_id=auth.user.id,
                           remarks="Edit {} doj to {}".format(request.vars.studentId,request.vars.doj ))
    db.commit()
    redirect(URL('student','index'))
    return response.json(ret)


@auth.requires(auth.has_membership('Management') or auth.has_membership('Admin'))
def edit_email():#modal from student page to edit students
    ret = db(db.Student.id == request.vars.studentId).validate_and_update(Email=request.vars.email)
    db.commit()
    db.activity_log.insert(Title_entry="Edit Student Email", 
                           referance_id=auth.user.id,
                           remarks="Edit {} email to {}".format(request.vars.studentId, request.vars.emai))
    db.commit()
    redirect(URL('student','index'))
    return response.json(ret)


@auth.requires(auth.has_membership('Management') or auth.has_membership('Admin'))
def edit_email2():#modal from student page to edit students
    ret = db(db.Student.id == request.vars.studentId).validate_and_update(Email2=request.vars.email2)
    db.commit()
    db.activity_log.insert(Title_entry="Edit Student EMail2", 
                           referance_id=auth.user.id,
                           remarks="Edit {} email2 to {}".format(request.vars.studentId, request.vars.email2))
    db.commit()
    redirect(URL('student','index'))
    return response.json(ret)


@auth.requires(auth.has_membership('Management') or auth.has_membership('Admin'))
def edit_contact():#modal from student page to edit students
    ret = db(db.Student.id == request.vars.studentId).validate_and_update(Contact=request.vars.contactNo)
    db.commit()
    db.activity_log.insert(Title_entry="Edit Student ContactNo.", 
                           referance_id=auth.user.id,
                           remarks="Edit {} contactNo to {}".format(request.vars.studentId, request.vars.contactNo))
    db.commit()
    redirect(URL('student','index'))
    return response.json(ret)


@auth.requires(auth.has_membership('Management') or auth.has_membership('Admin'))
def edit_contact2():#modal from student page to edit students
    ret = db(db.Student.id == request.vars.studentId).validate_and_update(Contact2=request.vars.contactNo2)
    db.commit()
    db.activity_log.insert(Title_entry="Edited Student Contactno2", 
                           referance_id=auth.user.id,
                           remarks="Edit {} contactNo2 to {}".format(request.vars.studentId, request.vars.contactNo2))
    db.commit()
    redirect(URL('student','index'))
    return response.json(ret)


@auth.requires(auth.has_membership('Management') or auth.has_membership('Admin'))
def edit_DOR():#modal from student page to edit students
    ret = db(db.Student.id == request.vars.studentId).validate_and_update(DoR=request.vars.dor)
    db.commit()
    db.activity_log.insert(Title_entry="Edited Student DoR", 
                           referance_id=auth.user.id,
                           remarks="Edit {} dor to {}".format(request.vars.studentId, request.vars.dor))
    db.commit()
    redirect(URL('student','index'))
    return response.json(ret)


@auth.requires(auth.has_membership('Management') or auth.has_membership('Admin'))
def edit_birthCountry():#modal from student page to edit students
    ret = db(db.Student.id == request.vars.studentId).validate_and_update(Birth_country=request.vars.birthCountry)
    db.commit()
    db.activity_log.insert(Title_entry="Edited Birthcountry", 
                           referance_id=auth.user.id,
                           remarks="Edited {} birthcountry to {}".format(request.vars.studentId, request.vars.birthCountry))
    db.commit()
    redirect(URL('student','index'))
    return response.json(ret)


@auth.requires(auth.has_membership('Management') or auth.has_membership('Admin'))
def edit_birthPlace():#modal from student page to edit students
    ret = db(db.Student.id == request.vars.studentId).validate_and_update(Birth_place=request.vars.birthPlace)
    db.commit()
    db.activity_log.insert(Title_entry="Edited birthplace", 
                           referance_id=auth.user.id,
                           remarks="Edit {} birthplace to {}".format(request.vars.studentId, request.vars.birthPlace))
    db.commit()
    redirect(URL('student','index'))
    return response.json(ret)


@auth.requires(auth.has_membership('Management') or auth.has_membership('Admin'))
def del_student():
    ret = db(db.Student.id == request.vars.studentId).validate_and_update(is_active=False)
    db.commit()
    app_id = db(db.Student.id == request.vars.studentId).select().first()
    authret = db(db.auth_user.id == app_id.Student_appID ).validate_and_update(registration_key="blocked")
    db.commit()
    if ret.errors:
        er_msg = ret.errors
    else:
        er_msg = "no errors"
    if authret.errors:
        auther_msg = authret.errors
    else:
        auther_msg = "no auth errors"
    db.activity_log.insert(Title_entry="Deactivate", referance_id=auth.user.id,remarks="Deactivate Student with auth {} and  {}".format(auther_msg, er_msg))
    db.commit()
    redirect(URL('student','index'))
    return response.json(ret)
