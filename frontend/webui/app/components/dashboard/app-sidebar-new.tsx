import React from 'react'
import { useState } from 'react'

import { Button } from '@/components/ui/button';

import {
  Avatar,
  AvatarImage,
  AvatarFallback
} from '@radix-ui/react-avatar';

import Image from 'next/image';

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

  const handleClick = (key: string) => {
    console.log("key is: ", key);
    setActive(key);
  }

  const sidebarMenuItems = [
    {
      key: "admins",
      name: "Admins"
    },
    {
      key: "schools",
      name: "Schools"
    },
    {
      key: "teachers",
      name: "Teachers"
    },
    {
      key: "students",
      name: "Students"
    },
    {
      key: "attendance",
      name: "Attendance"
    },
    {
      key: "fee-plan",
      name: "Fee Plan"
    },
    {
      key: "fee-record",
      name: "Fee Record"
    }
  ]

  const user = {
    name: "ABC",
    avatar: "https://images.unsplash.com/photo-1492633423870-43d1cd2775eb?&w=128&h=128&dpr=2&q=80",
    // avatar: "abc.jpg",
    email: "abc@email.com"
  }

  type MenuItem = {
    key: string
    name: string
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
                    onClick={() => handleClick(menu.key)}
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
          variant={"destructive"}>Logout</Button>
      </SidebarFooter>
    </Sidebar>

  )
}

