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
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiJlOGY0ZmVjZS1lNmZiLTQxMzgtYTdmOS0xYjRhMjIzYWVhMDciLCJyb2xlIjoiYWRtaW4ifQ.TcYL5nJ8PUnvJ9TMpY7kWoNJrIo8I4F1qIyMNRH7mZbh2dZSZ8ub4ben1uiDILTgVGGZoxhGP_kcnkudJkCbcCvVxFCS0ndyJ0vYEHiUaKvr4GMndb0oojjwY2oSM7yqcWzrHBHRYDJxANCVQX_rAt7uCppDUVtM0bbPGKXvYNqi-9gRa_iZDo_SWw_EcWm5b7UWXzrOR13gX39l8gEbip7FPqGxkHeQ0bLzpyYhbJAPNHNE-nSe08uc3-Rp9LTW55G-5sOsioMmwe357Vn6pt_KMzEHOBgTiHkNTWsflm_wqYoEfCzQuapCrxz9dRuFCbIEtDCZ18304i9VPgBedynliKaODmBN-ngPnNgF4fhQD6c5uGpSOjjkFkDj3Q2a9WIQn5NCjz26CK0A7mHw6ZsHfyqkMLelHaHzX1OSGcYtzYhzRK8luWSD_D23u-SDDtMAdahzAQ4aC35BVaqpuAeTnIzvmvc1GhoyMvXgRhf3-gren79_Z5lyKV0Q_wvI