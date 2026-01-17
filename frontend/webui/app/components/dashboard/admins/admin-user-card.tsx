"use client"
import React from 'react'

import {
    Card,
    CardContent,
    CardHeader,
    CardTitle
} from '@/components/ui/card'

import {
    Field,
    FieldDescription,
    FieldGroup,
    FieldLabel,
    FieldSeparator,
    FieldError,
    FieldContent
} from "@/components/ui/field"

import { Input } from "@/components/ui/input"

import { Button } from '@/components/ui/button'

import { useState, useEffect } from 'react'
interface AdminUserCardProps {
    id: string,
}


import { zodResolver } from "@hookform/resolvers/zod"
import { Controller, useForm } from "react-hook-form"
import { email, z } from "zod"
// import { Phone } from 'lucide-react'
import { toast } from 'sonner'

import { useRouter } from 'next/router'
const AdminUserCard: React.FC<AdminUserCardProps> = ({ id }) => {
    // const [name, setName] = useState('');
    // const [email, setEmail] = useState('');
    // const [phone, setPhone] = useState('');
    const [isEditing, setIsEditing] = useState(false);

    const [user, setUser] = useState({
        id: id,
        name: '',
        email: '',
        phone: ''
    })
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        let isMounted = true;

        async function fetchAdmin() {
            try {
                const res = await fetch(`/api/admin/${id}`, {
                    method: 'GET',
                    headers: {
                        "Content-Type": "application/json",
                    },

                })
                if (!res.ok) throw new Error("Error while Fetching user information");
                const result = await res.json();
                console.log("result: ", result.data[0]);

                const data = result.data[0];

                if (isMounted) {
                    form.reset({
                        name: data.name,
                        email: data.email,
                        phone: data.phone
                    })
                    setUser((prevUser) => ({
                        ...prevUser, name: data.name, email: data.email, phone: data.phone
                    }));
                    // setName(data.name);
                    // setEmail(data.email);
                    // setPhone(data.phone);
                }


            } catch (err) {
                console.error("Error message: ", err);
            } finally {
                if (isMounted) {
                    setLoading(false);
                }
            }

        }

        fetchAdmin();
    }, [])

    const formSchema = z.object({
        name: z.string().min(3),
        email: z.string().trim().email(),
        phone: z.string(),
    })

    // 1. Define your form.
    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            name: "",
            email: "",
            phone: "",
            
        },
    })

    async function onSubmit(values: z.infer<typeof formSchema>) {
        // Write to update user
        // console.log("values: ", values);

        try {
            const res = await fetch("/api/admin", {
                method: "PUT",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    id: id,
                    name: values.name,
                    email: values.email,
                    phone: values.phone,
                    password: ''
                })
            }) 
            const result = await res.json();
            if (!res.ok) throw new Error("Admin user updation Error")
            toast(`${result.message}`); 
            console.log("result: ", result);
            setUser((prevUser) => ({...prevUser, name: values.name, email: values.email, phone: values.phone}))

            form.reset({
                name: values.name,
                email: values.email,
                phone: values.phone
            })
            
        } catch(error) {
            console.error("Admin user updation Error!")
            toast("Admin user updation Error!")
        }
    }

    async function adminDelete() {
        try {
            const res = await fetch("/api/admin", {
                method: "DELETE",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    id: id,
                    name: user.name,
                    email: user.email,
                    phone: user.phone,
                })
            }) 
            const result = await res.json();
            if (!res.ok) throw new Error("Admin user Deletion Error")
            toast(`${result.message}`); 
            console.log("result: ", result);
            
        } catch(error) {
            console.error("Admin user Deletion Error!")
            toast("Admin user deletion Error!")
        }
    }

    const enableEdit = (enable: boolean) => {

        const name = (document.getElementById("form-name") as HTMLInputElement);
        const email = (document.getElementById("form-email") as HTMLInputElement);
        const phone = (document.getElementById("form-phone") as HTMLInputElement);
        const editButtons = (document.getElementById("edit-buttons") as HTMLDivElement)
        const viewButtons = (document.getElementById("view-buttons") as HTMLDivElement)
        if (name && email && phone && editButtons && viewButtons) {

            if (enable) {
                
                setIsEditing(enable);
                editButtons.className = 'block';
                viewButtons.className = 'hidden';
            } else {
                
                setIsEditing(enable);
                form.reset({
                    name: user.name,
                    email: user.email,
                    phone: user.phone
                });

                editButtons.className = 'hidden';
                viewButtons.className = 'block';
            }
            
        }
    }

    
    return (
        <div className='px-10 py-10'>
            <Card>
                <CardHeader>
                    <CardTitle>UID: {id}</CardTitle>
                </CardHeader>
                <CardContent>
                    <form id="create-admin-form" onSubmit={form.handleSubmit(onSubmit)}>
                        <FieldGroup>

                            {/* Name Controller */}
                            <Controller
                                name="name"
                                control={form.control}
                                render={({ field, fieldState }) => (
                                    <Field data-invalid={fieldState.invalid}>
                                        <FieldLabel htmlFor="form-name">Name</FieldLabel>
                                        <Input
                                            {...field}
                                            id="form-name"
                                            type="text"
                                            placeholder="Enter name"
                                            
                                            aria-invalid={fieldState.invalid}
                                            // onChange={(e) => { setName(e.target.value) }}
                                            autoComplete="off"
                                            required
                                            disabled={!isEditing}
                                        />
                                        {fieldState.invalid && (
                                            <FieldError errors={[fieldState.error]} />
                                        )}

                                    </Field>
                                )}
                            />

                            {/* Email Controller */}
                            <Controller
                                name="email"
                                control={form.control}
                                render={({ field, fieldState }) => (
                                    <Field data-invalid={fieldState.invalid}>
                                        <FieldLabel htmlFor="form-email">Email</FieldLabel>
                                        <Input
                                            {...field}
                                            id="form-email"
                                            type="email"
                                            placeholder="Enter email"
                                            // value = {email}
                                            aria-invalid={fieldState.invalid}
                                            // onChange={(e) => { setEmail(e.target.value) }}
                                            autoComplete="off"
                                            required
                                            disabled={!isEditing}
                                        />
                                        {fieldState.invalid && (
                                            <FieldError errors={[fieldState.error]} />
                                        )}

                                    </Field>
                                )}
                            />

                            {/* Phone Controller */}
                            <Controller
                                name="phone"
                                control={form.control}
                                render={({ field, fieldState }) => (
                                    <Field data-invalid={fieldState.invalid}>
                                        <FieldLabel htmlFor="form-phone">Phone</FieldLabel>
                                        <Input
                                            {...field}
                                            id="form-phone"
                                            type="text"
                                            placeholder="Enter Phone"
                                            maxLength={10}
                                            // value={phone}
                                            aria-invalid={fieldState.invalid}
                                            // onChange={(e) => { setPhone(e.target.value) }}
                                            autoComplete="off"
                                            required
                                            disabled={!isEditing}
                                        />
                                        {fieldState.invalid && (
                                            <FieldError errors={[fieldState.error]} />
                                        )}

                                    </Field>
                                )}
                            />


                            



                            {/* Submit the form */}
                            <Field id="view-buttons">
                                <div className='flex space-x-1 justify-center '>
                                <Button onClick={(event) => {
                                    event.preventDefault();
                                    enableEdit(true);
                                    
                                }}>Edit</Button>
                                <Button variant={'destructive'} onClick={(event)=> {
                                    event.preventDefault();
                                    adminDelete();
                                }} >Delete</Button>
                                </div>
                            </Field>
                            <Field id="edit-buttons" className='hidden'>
                                <div className='flex space-x-1 justify-center '>
                                <Button type='submit' form="create-admin-form">Save</Button>
                                <Button variant={'destructive'} onClick={(event)=>{
                                    event.preventDefault();
                                    enableEdit(false);
                                }} >Cancel</Button>
                                </div>
                            </Field>

                        </FieldGroup>
                    </form>

                </CardContent>
            </Card>
        </div>
    )
}

export default AdminUserCard