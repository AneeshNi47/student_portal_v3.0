import os
durations = ('Weekly', 'Monthly')
batch_status = ('active','deactive')
degree_status = ('Documents Submitted','Documents Rejected','Applied','Recieved','Collected')

db.define_table('C_Location',
                Field('location_Name','string'),
                auth.signature,
                format='%(location_Name)s')

db.define_table('Course',
                Field('Course_Name','string'),
                auth.signature,
                format='%(Course_Name)s')

db.define_table('Specialization',
                Field('specialization_Name','string'),
                auth.signature,
                format='%(specialization_Name)s')

db.define_table('Subjects',
                Field('Subject_Name','string'),
                Field('Subject_Course','reference Course'),
                Field('Subject_Specialization','reference Specialization'),
                auth.signature,
                format='%(Subject_Name)s')

db.define_table('Batch',
                Field('Batch_title','string'),
                Field('Batch_Location','reference C_Location'),
                Field('Batch_type',requires=IS_IN_SET(durations)),
                Field('Batch_Course','reference Course'),
                Field('Batch_Specialisation','reference Specialization'),
                Field('Students_no', 'string'),
                auth.signature,
                format='%(Batch_title)s')
 
db.define_table('Content_material',
                Field('Content_title', 'string'),
                Field('Subject_name', 'reference Subjects'),
                Field('Batch_id', 'reference Batch'),
                Field('Content_file', 'upload', uploadfolder=os.path.join(request.folder, 'static/content'),autodelete=True),
                auth.signature,
                format='%(Content_title)s')


db.define_table('activity_log',
                Field('Entry_date','datetime', default=request.now),
                Field('Title_entry', 'string'),
                Field('referance_id','string'),
                Field('remarks', 'text'),
                auth.signature
             )
                  
db.define_table('Degree_file',
                Field('student_id','reference auth_user'),
                Field('batch_id', 'reference Batch'),
                Field('status', requires=IS_IN_SET(degree_status)),
                Field('PC_agreement','upload', uploadfolder=os.path.join(request.folder, 'static/entrance_docs1')),
                Field('Graduation_form','upload', uploadfolder=os.path.join(request.folder, 'static/entrance_docs1')),
                Field('Docs_date','date'),
                Field('applied_date',  'date'),
                Field('collected_date',  'date'),
                auth.signature
                )
