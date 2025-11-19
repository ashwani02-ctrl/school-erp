Build sequence

1. Super user creation flow
Needs AdminUSer Table to create user.
requirements:
name: str
email: EmailStr
phone: str = Field(max_length=15)
password: str


2. Superuser auth flow
Need email and password -> then we have the thing

3. Current User flow
4. CRUD user flow
5. CRUD Fee flow
6. CRUD Attendance flow


Flow:-
1. Super user creation
2. Authenticatin of Superuser
3. CRUD Users flow


Superuser
name: admin
password: simple
email: abhishekroka2003@gmail.com
phone: 8907654321

jwt: 
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiJmODNlZDNmNy1kNjRmLTQ3YmQtYTc1YS1iMDM5Y2EzZjFjODgiLCJyb2xlIjoiYWRtaW4ifQ.n45SpOXttSigQKamoDJnlS3M2pAzQbLK1LzAKKRnpkgPVhO9ay_5Qqo3MnJm2v-7H0s3dWxjk7Tiv2lFrVuoHPPAFElXBZzTVjaLCeCwHgR_PO857NH8Qb6_FGZNPZduDDdrreN_V1t39y8MMWlpew40cJkBR-6gxV0TD1A6c9ZbRVsd08qZgX5NvEzZRAm46hs5fwCel5PA4UDHjVkwFl4HOjv0PaATmynx80nS8sMyraZtwG7s3y0LRi_7DEywcfYIzhFA5mrbyUdWnTGzGQUP6lya38xflFA85Y2_fa-BtzDnQb40q448oKZKQ-RYtkcmmFGgQ4BGhYYPI2u5_ynshbLymZo5yuhHcPb4hXpPLAbLU0rkRacCDxGiiD-NAPzozJX7iZK-UixsXFleJEtu9NfrdC45kdcvd9TlSZATQDxCG7VyIS64yvpSuRB4qOkD_eSmN_vSGgIm6tdRlP0HV4CroKdSZ5G6jUENs8fF6DecGdODrrkv3X17L6oZ

##### CREATE TEACHER LOGIC ###########
if admin is creating a teacher, then the admin must provide school id too
if school is the creator, then,  school id will be catched.


admin jwt:
{
    "email":"abc@example.com",
    "password":"simple",
    "role":"admin"
}

eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiJkMjNkZGFlOS03YTYxLTRlYzctODY1NC05MWZlOWUzMGU0YTAiLCJyb2xlIjoiYWRtaW4ifQ.XS2doklBEJ3c2bP2szwoiZSQRgmzZsK-XhDsXw0yA_kgimSJHNIsPTUKyEgLlN6ZM92K7KsWCaslRvmO9cWi5cLB0FoI4nIbBc-kUYcyIIFWDNNZsvZbHMM1uchcaMIyThTzDeK9hN-zTE4VbPmN7ej7yOT8-nvehhsA6nr3G73aKuiiRU_hJW57-3D6OvD7Zid_ubaUu4zUiGyRtK9zjmV4B_glm7TR3LdbBa3ONxbVfHosTD0z4tAe-nxnUJJxk9gcubUQEaP9h8bOyXvBXOhss7j3BKmzr4vfSI7NZ5gJ9wyjvvfSEy2dvEdIBviTRLypLnI6nFK9fIFhX2H5SzireKoR1ZiJdRkvgEpuqsyUsjn6zNJKiOPc_a8-AwyBuVpoBMzUGwGWNknCPPnGFfIUUrDAgsKnmSkSRQDHY9qcG4OS4fHFz2xf7pETpigJ3bTwIo6X_dUKc9mhThWwKFK0yTAdOhvXHbho-ofuugQ8vqafenyvrqsdjTqUmnXX

school jwt:
{
    "email":"school@example.com",
    "password":"simple",
    "role":"school"
}

eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiI2NzllMDI0OC0zNWJlLTQ3NmUtYTc4Yy1hNWQ1Y2I2MThiYTkiLCJyb2xlIjoic2Nob29sIn0.e984zmYSGhqZkeWXLChs6HCA2KvlNmWXClUf6TAzaTerrN1DhPrZNQdiAOJQIxqtysWmbs1V3w5eYOsydkeZHC8GXUORFzTsj9071gZ4CDg4ylfTgF5TzkZXtaHRI9yJVqc-e5b_l748nzkhP8-PhKP9VfFmg5gpQAZq4KwbrBJ0TRC5RwNFXrZpGva5g_jcixUZgKJz189CPUM8Q5lT6yR5GD_b8EOeIjiKiIlZwLBnC5HhY2CIS5bPoWfJdy9sNggUQiVp7pK9UonuXVdK1sbH5YL5jPy-O7umoOk5FVdfYuOiKJDV2jXQLH52x2JFd1oWCvvCdmtWcSV2vsOTeK_FnphzVz97BGeZNvRBBLlQguapFAQ2PasIbqdqLEEYGP59nWNIYBLlyvFUfuoskCGxbvcAUpgWosvhW7A6ahD-0PAlLmFUpxapUgGR97z6HA0MGZNZTUZnAhHKbWkdJRD6Alefc1k9pkUKmXFWth24z18TkYOWnFb1330-RNRG

student jwt:

{
    "name":"student",
    "email":"student@example.com",
    "phone":"2908765431",
    "school_id":"679e024835be476ea78ca5d5cb618ba9",
    "classsection_id":"1b29662ef7f04fb0bc2e81dbb3655bb7"
    
}




{
    "email":"student1@example.com",
    "password":"simple",
    "role":"student"
}

WHILE CREATING SCHOOL user
1. make crud method to get classsection reecord from db, like we do for get_user_by_id
2. make classseciton to be a part, while creating a student user, because while deleting the classsection user, it will also delete a student user by CASCADE effect!


CRUD for classsection created, now working on Attendance.