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