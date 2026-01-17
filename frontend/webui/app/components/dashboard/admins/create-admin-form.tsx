"use client"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
    CardFooter
} from "@/components/ui/card"
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
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"

// import { useState } from "react"


import Cookies from 'js-cookie';

import {
    Form,
    FormControl,
    FormDescription,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form"


import { toast } from "sonner"

import { zodResolver } from "@hookform/resolvers/zod"
import { Controller, useForm } from "react-hook-form"
import { z } from "zod"


const roles = ["admin", "school", "teacher"]
const formSchema = z.object({
    name: z.string().min(3),
    email: z.email(),
    phone: z.string().max(10),
    // password: z.string()

})

// import { useRouter } from "next/navigation"



export function CreateAdminForm({
    className,
    ...props
}: React.ComponentProps<"div">) {
    // const router = useRouter();

    // 1. Define your form.
    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            name: "",
            email: "",
            phone: "",
            // password: ""
        },
    })

    // 2. Define a submit handler.
    async function onSubmit(values: z.infer<typeof formSchema>) {

        toast("You submitted the following values:", {
            description: (
                <pre className="bg-code text-code-foreground mt-2 w-[320px] overflow-x-auto rounded-md p-4">
                    <code>{JSON.stringify(values, null, 2)}</code>
                </pre>
            ),
            position: "top-center",
            classNames: {
                content: "flex flex-col gap-2",
            },
            style: {
                "--border-radius": "calc(var(--radius)  + 4px)",
            } as React.CSSProperties,
        });

        const token = Cookies.get("token");
        // toast(`token: ${token}`);

        try {
            const res = await fetch("/api/admin", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorisation": `Bearer ${token}`
                },
                body: JSON.stringify(values),
            });

            const result = await res.json();
            

            if (res.status == 500) {
                toast.error(`${result.message}`, { position: "top-center" });
            } 
            else if (!res.ok) { 
                throw new Error("Admin Creation failed") 
            }
            else {
                toast("Admin User Created!");
            }

            // const result = await res.json();
            // console.log("Login success:", result);
            // Cookies.set("token", result.token, { path: '/' });
            // router.push("/dashboard");
            // Redirect or store token here
        } catch (err) {
            console.error("Login error:", err);
        }

    }




    return (
        <div className={cn("flex flex-col gap-6 px-10 py-10", className)} {...props}>
            <Card>
                <CardHeader className="text-center">
                    <CardTitle className="text-xl">Create Admin Form</CardTitle>
                </CardHeader>
                <CardContent>
                    {/* <Form {...form}> */}
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
                                            // onChange={(e) => { setEmail(e.target.value) }}
                                            autoComplete="off"
                                            required
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
                                            aria-invalid={fieldState.invalid}
                                            // onChange={(e) => { setEmail(e.target.value) }}
                                            autoComplete="off"
                                            required
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
                                            aria-invalid={fieldState.invalid}
                                            // onChange={(e) => { setEmail(e.target.value) }}
                                            autoComplete="off"
                                            required
                                        />
                                        {fieldState.invalid && (
                                            <FieldError errors={[fieldState.error]} />
                                        )}

                                    </Field>
                                )}
                            />


                            {/* Password Controller */}
                            {/* <Controller
                                name="password"
                                control={form.control}
                                render={({ field, fieldState }) => (
                                    <Field data-invalid={fieldState.invalid}>
                                        <div className="flex">

                                            <FieldLabel htmlFor="form-password">Password</FieldLabel>

                                        </div>
                                        <div className="flex space-x-1">

                                            <Input
                                                {...field}
                                                id="form-password"
                                                type="password"
                                                placeholder="Enter password"
                                                required
                                            />
                                            <Button onClick={(event) => {
                                                event.preventDefault();
                                                passwordGenerator(16);
                                                }}>
                                                    Generate
                                                    </Button>
                                        </div>
                                        {fieldState.invalid && (
                                            <FieldError errors={[fieldState.error]} />
                                        )}

                                    </Field>
                                )}
                            /> */}



                            {/* Submit the form */}
                            <Field>
                                <Button type="submit" form="create-admin-form">Submit</Button>

                            </Field>
                        </FieldGroup>
                    </form>

                </CardContent>
            </Card>
            {/* <FieldDescription className="px-6 text-center">
        By clicking continue, you agree to our <a href="#">Terms of Service</a>{" "}
        and <a href="#">Privacy Policy</a>.
      </FieldDescription> */}
        </div >
    )
}
