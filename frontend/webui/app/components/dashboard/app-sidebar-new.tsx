"use client"
import React from 'react'
import { useState } from 'react'
import { useRouter } from 'next/navigation';

import { Button } from '@/components/ui/button';

import {
  Avatar,
  AvatarImage,
  AvatarFallback
} from '@radix-ui/react-avatar';

import Cookies from "js-cookie"

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarHeader,
  SidebarGroupContent,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton
} from "@/components/ui/sidebar"

export default function AppSidebarNew() {
  const [active, setActive] = useState<string | null>(null);

  

  const sidebarMenuItems = [
    {
      key: "admins",
      name: "Admins",
      url: "/dashboard/admins"
    },
    {
      key: "schools",
      name: "Schools",
      url: "/dashboard/schools"
    },
    {
      key: "teachers",
      name: "Teachers",
      url: "/dashboard/teachers"
    },
    {
      key: "students",
      name: "Students",
      url: "/dashboard/students"
    },
    {
      key: "attendance",
      name: "Attendance",
      url: "/dashboard/attendance"
    },
    {
      key: "fee-plan",
      name: "Fee Plan",
      url: "/dashboard/feeplan"
    },
    {
      key: "fee-record",
      name: "Fee Record",
      url: "/dashboard/feerecord"
    }
  ]

  const handleClick = (key: string, url: string) => {
    console.log("key is: ", key);
    setActive(key);
    router.push(url);
  }

  const router = useRouter();
  const logout = () => {
    Cookies.remove("token");
    router.refresh();
    
  }

  const user = {
    name: "ABC",
    avatar: "https://images.unsplash.com/photo-1492633423870-43d1cd2775eb?&w=128&h=128&dpr=2&q=80",
    // avatar: "abc.jpg",
    email: "abc@email.com"
  }

  type MenuItem = {
    key: string
    name: string
    url: string
  }

  return (

    <Sidebar className='bg-blue-950'>
      <SidebarHeader>
        <div className=''>
          <h1 className='text-center text-wrap text-3xl font-bold'>Admin Panel</h1>
          {/* h-8 w-8 */}
          <div className=' '>
            <Avatar className=" size-36 flex mx-16 lg:mx-12">
              <AvatarImage className='rounded-full grayscale  ' src={user.avatar} alt={user.name} />
              {/* <Image 
                    src="/avatar.svg"
                    alt={user.name}
                    width={24}
                    height={24}
                    className='h-6 w-6 object-cover object-center rounded-full'
                  /> */}
              <AvatarFallback className="flex items-center justify-center rounded-lg ">CN</AvatarFallback>
            </Avatar>
          </div>
          <p className='text-center'>{user.name}</p>
        </div>
      </ SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupContent>
            <SidebarMenu>
              {sidebarMenuItems.map((menu: MenuItem) => (
                <SidebarMenuItem key={menu.key} >
                  <SidebarMenuButton
                    isActive={active === menu.key}
                    onClick={() => handleClick(menu.key, menu.url)}
                    variant={"outline"}
                    className='justify-center'

                  >
                    {menu.name}
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}



            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter >
        <Button
          variant={"destructive"} onClick={logout}>Logout</Button>
      </SidebarFooter>
    </Sidebar>

  )
}

