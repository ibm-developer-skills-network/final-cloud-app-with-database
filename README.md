# ER diagram for a sample online course database
![ER diagram](https://github.com/ibm-developer-skills-network/gwmom-cad7-django-orm/blob/master/images/orm.png)
Models:
- `User`, base user model
    * id (PK)
    * first_name
    * last_name
    * dob
- `Learner`, Inherited from `User`. `Many-To-Many` relationship 
with `Course` through `Enrollment`
    * occupation
    * social_link
    * usr_ptr_id (PK and FK)
- `Instructor`, Inherited from `User`. `Many-To-Many` relationship 
with `Course`
    * full_time
    * total_learners
    * usr_ptr_id (PK and FK)
- `Course`, `Many-To-Many` relationship with `Learner` and 
`Instructor`. `One-To-Many` relationship with `Project`
    * id (PK)
    * name
    * description
- `Project`. `Many-To-One` relationship with `Course`
    * id (PK)
    * name
    * grade
    * course_id (FK)
- `Enrollment`, as a look-up table for `Course` and `Learner` with
extra enrollment information
    * id (PK)
    * course_id (FK)
    * learner_id (FK)
    * date_enrolled
    * mode

More details about model definitions can be found in `data/models.py`

A sample course would look like this:
```
Course: Cloud Application Development with Database,Develop and deploy application on cloud
Course instructors: <QuerySet [<Instructor: Yan, Luo, True, 30050>, <Instructor: Joy, Li, False, 10040>]>
Course learners: <QuerySet [<Learner: James, Smith, data_scientist, https://www.linkedin.com/james/>, <Learner: Mary, Smith, dba, https://www.facebook.com/mary/>]>
Course project: Object-relational mapping project
```