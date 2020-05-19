import os
durations = ('Weekly', 'Monthly')
student_status = ('verified', 'pending','çompleted','expired')
notify_status = ('Open', 'Closed','Approved','Rejected')
notify_type = ('Announcement','Notice','Warning','Request','Message')
sch_type = ('Sub_start','Sub_end','Exam','Assignment','Session 1','Session 2','Session 3','Session 4')

 
db.define_table('Student',
                Field('F_Name','string'),
                Field('L_Name','string'),
                Field('Company','string'),
                Field('Qualification','string'),
                Field('Designation','string'),
                Field('Student_appID','reference auth_user'),
                Field('Student_colgID','string'),
                Field('DoJ','date'),
                Field('Birth_country','string'),
                Field('Birth_place','string'),
                Field('Email','string'),
                Field('Email2','string'),
                Field('Contact','string'),
                Field('Contact2','string'),
                Field('DoR','date'),
                Field('FB_ID','string'),
                Field('LinkedIn_ID','string'),
                Field('twitter_ID','string'),
                Field('PC_agreement','upload', uploadfolder=os.path.join(request.folder, 'static/entrance_docs1'),autodelete=True),
                Field('Graduation_form','upload', uploadfolder=os.path.join(request.folder, 'static/entrance_docs1'),autodelete=True),
                Field('Batch','reference Batch'),
                Field('icon_image','upload', uploadfolder=os.path.join(request.folder, 'static/student_images'),autodelete=True),
                Field('Status', requires=IS_IN_SET(student_status ), default='pending'),
                Field('Acces_exp','date'),
                auth.signature,
                format='%(F_Name)s')
                
db.define_table('Assignments',
                Field('Assignemnt_title','string'),
                Field('Batch_id','reference Batch'),
                Field('student_id','reference Student'),
                Field('course','reference Course'),
                Field('subject_assign','reference Subjects'),
                Field('FinalSubmission_date','date'),
                Field('Origianl_content','upload', uploadfolder=os.path.join(request.folder, 'static/assignemnt')),
                auth.signature,
                format='%(Assignemnt_title)s')
                
db.define_table('Assignment_content',
                Field('Assignemnt_title','reference Assignments'),
                Field('Student_ID','reference Student'),
                Field('Submission_date','datetime', default=request.now),
                Field('Assignment_file','upload', uploadfolder=os.path.join(request.folder, 'static/sub_assignemnt')),
                auth.signature,
                format='%(Assignemnt_title)s')

db.define_table('SelfStudy_material',
                Field('SelfContent_title', 'string'),
                Field('Course_id', 'reference Course'),
                Field('Spcl_id', 'reference Specialization'),
                Field('Subject_id', 'reference Subjects'),
                Field('student_id', 'reference Student'),
                Field('selfStudy_file', 'upload', uploadfolder=os.path.join(request.folder, 'static/SelfStudy')),
                auth.signature,
                format='%(Content_title)s')
 

db.define_table('Semester',
                Field('Semester_title','string'),
                Field('Batch_id','reference Batch'),
                auth.signature,
                format='%(Semester_title)s')


db.define_table('Grades',
                Field('Student_id', 'reference Student'),
                Field('Semester_id', 'reference Semester'),
                Field('Mark','integer'),
                Field('Grade','string'),
                Field('Subject', 'reference Subjects'),
                Field('Remarks', 'text'),
                auth.signature,
                )
 
db.define_table('Notifications',
                Field('set_date','datetime', default=request.now),
                Field('notif_use', requires=IS_IN_SET(notify_type)),
                Field('Topic', 'string'),
                Field('Message_n', 'string'),
                Field('Given_by', 'reference auth_user'),
                Field('Given_to_S', 'reference auth_user'),
                Field('Given_to_B', 'reference Batch'),
                Field('Given_to_ALL', default='All'),
                Field('Status', requires=IS_IN_SET(notify_status), default='Open'),
                auth.signature
                )

db.define_table('Schedule',
                Field('set_date','datetime', default=request.now),
                Field('sch_type', requires=IS_IN_SET(sch_type)),
                Field('Batch', 'reference Batch'),
                Field('class_location', 'string'),
                Field('lecturer_name', 'string'),
                Field('Subject', 'reference Subjects'),
                Field('Start_date', 'date'),
                Field('Remarks', 'string'),
                Field('lect_image','upload', uploadfolder=os.path.join(request.folder, 'static/lecturer_images')),
                Field('lect_profile','upload', uploadfolder=os.path.join(request.folder, 'static/lecturer_profile')),
                auth.signature
                )

db.define_table('Examiners',
                Field('Ex_Appid', 'reference auth_user'),
                Field('Ex_officeID', 'string'),
                Field('Ex_Fname', 'string'),
                Field('Ex_Lname', 'string'),
                Field('Email', 'string'),
                Field('Contact', 'string'),
                Field('Designation', 'string'),
                auth.signature
                ) 

db.define_table('Managers',
                Field('Mg_Appid', 'reference auth_user'),
                Field('Mg_officeID', 'string'),
                Field('Mg_Fname', 'string'),
                Field('Mg_Lname', 'string'),
                Field('Email', 'string'),
                Field('Contact', 'string'),
                Field('Designation', 'string'),
                auth.signature
                )
