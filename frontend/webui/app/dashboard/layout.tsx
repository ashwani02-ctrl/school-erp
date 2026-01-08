// "use client"
import DashboardSidebarProvider from "./DashboardSidebarProvider"

import AppSidebarNew from "../components/dashboard/app-sidebar-new"

// import {
//     Breadcrumb,
//     BreadcrumbItem,
//     BreadcrumbLink,
//     BreadcrumbList,
//     BreadcrumbPage,
//     BreadcrumbSeparator,
// } from "@/components/ui/breadcrumb"
// import { Separator } from "@/components/ui/separator"
// import {
//     SidebarInset,
//     SidebarProvider,
//     SidebarTrigger,
// } from "@/components/ui/sidebar"


// import { useEffect, useState } from "react"
// import Cookies from "js-cookie"


export default function DashboardLayout({
    children,
}: {
    children: React.ReactNode
}) {

    // const [profile, setProfile] = useState({
    //     name: "shadcn",
    //     email: "m@example.com",
    //     avatar: "/avatar.svg",
    //     fallbackText: "AR",
    //     role: "student"
    // });

    // type Role = "admin" | "school" | "teacher" | "student";

    // const navMainMenus = (role: Role) => {
    //     const menuMapping = {
    //         'admin': ["Admins", "Schools", "Teachers", "Students", "Attendance", "Fees"],
    //         'school': ["Teachers", "Students", "Attendance", "Fees"],
    //         'teacher': ["Teachers", "Attendance"],
    //         'student': ["Students", "Attendance", "Fees"],
    //     }

    //     return menuMapping[role].map(title => ({
    //         title,
    //         url: "#",
    //         isActive: false,
    //     }));

    // }

    // useEffect(() => {
    //     async function getProfile() {
    //         const token = Cookies.get("token");
    //         console.log(`token: ${token}`)
    //         console.log(`${process.env.NEXT_PUBLIC_BASEURL}`);
    //         const res = await fetch(`${process.env.NEXT_PUBLIC_BASEURL}/profile`, {
    //             method: "POST",
    //             credentials: "include",
    //             headers: {
    //                 "Content-Type": "application/json",
    //                 "Authorization": `Bearer ${token} `
    //             }
    //         });
    //         const data = await res.json();
    //         console.log(data.data);
    //         setProfile(prev => ({
    //             ...prev,
    //             name: data.data.username,
    //             email: data.data.email,
    //             role: data.data.role
    //         }));
    //     }
    //     getProfile();
    // }, []);

    // const sidebarData = {
    //     user: profile,

    //     navMain: [
    //         {
    //             title: "Menu",
    //             url: "#",
    //             items: navMainMenus(profile.role as Role),
    //         },
    //     ],
    // }
    return (
        <>
        <DashboardSidebarProvider>
            <p className="text-center">This is layout text. </p>
            <section>{children}</section>
        </DashboardSidebarProvider>
        
        </>
    )
}