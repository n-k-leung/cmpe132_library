# CMPE 132 Library

This is a web-based system that runs on Flask and SQLAlchemy. It is to preform primary user enrollement, authentication, and authorization for a fictionous library, called SJSUL. This is designed for the SJSU CMPE 132 class project.


## Dependencies
There are multiple dependances that this code needs. They are listed in the dependecies.txt file.

## Instructions
Follow the steps listed below to run the code:
1. ``git clone https://github.com/n-k-leung/cmpe132_library.git``
2. ``cd cmpe132_library``
3. ``pip3 install -r dependencies.txt``
4. ``python3 run.py``

## Roles and Their Functions
Guest: can reserve books
Student: can reserve books and tech
Professor: can reserve books and tech
Staff: can reserve/unreserve books, add books, delete books, reserve/unreserve tech, add tech, delete tech
Admin: can approve of users roles, demote users to guest role, reserve/unreserve books, add books, delete books, reserve/unreserve tech, add tech, delete tech


## Important Notes
There are five possible roles a user can be: student, professor, staff, admin, and guest.

When a new user registers, they are automatically set to have the role of a guest. Only after the admin approves of their registration under a different role (i.e. student, professor, staff, or admin) can the new user have thier desired role.

There are three accounts that have been already made to test the code:
1. admin account-- role:admin, username: aad, email:aad@sjsu.com, password: aad
1. guest account-- role:guest, username: ggs, email:ggs@sjsu.com, password: 123
1. student account-- role:student, username: sst, email:sst@sjsu.com, password: 123

Some sample books and tech were added for demostration
